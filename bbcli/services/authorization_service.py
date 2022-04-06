from urllib import request
import os
from dotenv import load_dotenv
from bbcli.entities.RequestData import RequestData
import requests
import json
from bs4 import BeautifulSoup
import time
from getpass import getpass

ctx = ''
session_id = ''
canary = ''
auth_method_id = ''
hpg_request_id = ''
flowtoken = ''
login_username = ''
otc = None


def login():
    print("Logging in...")
# TODO: Let user choose between feide log in or ID-gate
    feide_login()

# -------------------- FEIDE LOGIN PART -------------------- #


def feide_login():
    session = requests.Session()
    request_data = RequestData()

    scrape_login_page(session, request_data)
    response = post_login_request(session, request_data, get_credentials())
    scrape_login_response(response, request_data)
    response = post_adfs_request(session, request_data)
    scrape_adfs_response(response, request_data)
    response = post_microsoft_login(session, request_data)
    scrape_microsoft_login_response(response, request_data)

    begin_auth(session, request_data)
    response = process_auth(session, request_data, otc)
    scrape_process_auth(response, request_data)
    post_auth_saml_SSO(session, request_data)

    write_to_env_data(session)
    print('Login successful!')


def get_credentials():
    # TODO: Give user an option to save their username and password
    # so they don't have to write their login everytime they want to login
    username = getpass("Username: ")
    password = getpass()

    credentials = {
        'username': username,
        'password': password
    }

    return credentials


def scrape_login_page(session, request_data):
    html = session.get('http://innsida.ntnu.no/blackboard')
    soup = BeautifulSoup(html.text, 'lxml')
    auth_state = soup.find('input', {'name': 'AuthState'})['value']

    request_data.params = (
        ('org', 'ntnu.no'),
        ('AuthState', auth_state)
    )


def post_login_request(session, request_data, credentials):
    request_data.data = {
        'feidename': credentials['username'],
        'password': credentials['password']
    }
    global login_username
    login_username = credentials['username']

    return session.post('https://idp.feide.no/simplesaml/module.php/feide/login', params=request_data.params, data=request_data.data)


def scrape_login_response(response, request_data):
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        samlResponse = soup.find(
            'input', {'name': 'SAMLResponse'})['value']
        relayState = soup.find(
            'input', {'name': 'RelayState'})['value']
    except TypeError:
        raise TypeError("Username or password is wrong...")
    else:
        request_data.data = {
            'SAMLResponse': samlResponse,
            'RelayState': relayState
        }


def post_adfs_request(session, request_data):
    return session.post('https://adfs.ntnu.no/adfs/ls/', data=request_data.data)


def scrape_adfs_response(response, request_data):
    soup = BeautifulSoup(response.text, 'lxml')

    wa = soup.find('input', {'name': 'wa'})['value']

    wresult = soup.find('input', {'name': 'wresult'})['value']
    wctx = soup.find('input', {'name': 'wctx'})['value']

    request_data.data = {
        'wa': wa,
        'wresult': wresult,
        'wctx': wctx
    }


def post_microsoft_login(session, request_data):
    return session.post(
        'https://login.microsoftonline.com/login.srf', data=request_data.data)


def scrape_microsoft_login_response(response, request_data):
    soup = BeautifulSoup(response.text, 'lxml')

    script_tag = soup.find('script')
    # Remove certaint parts of the script content to be able to use json.loads
    script_tag = script_tag.contents[0][20:len(script_tag.contents[0]) - 7]
    script_content = json.loads(script_tag)

    global ctx
    global session_id
    global canary
    global auth_method_id
    global hpg_request_id

    ctx = script_content['sCtx']
    flowtoken = script_content['sFT']
    session_id = script_content['sessionId']
    canary = script_content['canary']
    auth_methods = script_content['arrUserProofs']
    auth_method_id = find_default_auth_method(auth_methods)
    print(auth_method_id)
    if(auth_method_id == None):
        auth_method_id = choose_auth_method(auth_methods)
    hpg_request_id = response.headers['x-ms-request-id']

    request_data.data = {
        "AuthMethodId": auth_method_id,
        "Method": "BeginAuth",
        "ctx": ctx,
        "flowToken": flowtoken
    }
    request_data.data = json.dumps(request_data.data)


def find_default_auth_method(auth_methods):
    for auth_method in auth_methods:
        if auth_method['isDefault'] == True:
            return auth_method['authMethodId']


def choose_auth_method(auth_methods):
    print('Choose auth method:\n')
    choice = 1
    for auth_method in auth_methods:
        print(str(choice) + ". " + auth_method['authMethodId'])
        choice += 1

    user_input = input()
    return auth_methods[int(user_input) - 1]['authMethodId']


def begin_auth(session, request_data):
    global type

    if auth_method_id == 'PhoneAppNotification':
        begin_phone_app_auth(session, request_data)
    elif auth_method_id == 'OneWaySMS' or auth_method_id == 'PhoneAppOTP':
        begin_one_time_code_auth(session, request_data)


def begin_phone_app_auth(session, request_data):
    response = session.post(
        'https://login.microsoftonline.com/common/SAS/BeginAuth', data=request_data.data)

    j = json.loads(response.text)
    app_auth_wait(session, request_data, j['CorrelationId'], j['FlowToken'])


def begin_one_time_code_auth(session, request_data):
    global otc
    global flowtoken

    response = session.post(
        'https://login.microsoftonline.com/common/SAS/BeginAuth', data=request_data.data)

    SMS_code = input('Enter code: ')
    otc = SMS_code
    j = json.loads(response.text)

    request_data.data = {
        'AdditionalAuthData': SMS_code,
        'AuthMethodId': auth_method_id,
        'Ctx': j['Ctx'],
        'FlowToken': j['FlowToken'],
        'Method': 'EndAuth',
        'PollCount': 1,
        'SessionId': session_id
    }
    request_data.headers = {
        'client-request-id': j['CorrelationId']
    }

    data = json.dumps(request_data.data)

    response = session.post(
        'https://login.microsoftonline.com/common/SAS/EndAuth', data=data, headers=request_data.headers)
    j = json.loads(response.text)
    flowtoken = j['FlowToken']


def app_auth_wait(session, request_data, client_request_id, flow_token):
    global flowtoken

    request_data.data = {
        "Method": "EndAuth",
        "SessionId": session_id,
        "FlowToken": flow_token,
        "Ctx": ctx,
        "AuthMethodId": auth_method_id,
        "PollCount": 1
    }
    request_data.headers = {
        'client-request-id': client_request_id,
    }

    data = json.dumps(request_data.data)

    for tries in range(10):
        response = session.post(
            'https://login.microsoftonline.com/common/SAS/EndAuth', data=data, headers=request_data.headers)
        j = json.loads(response.text)
        if j['Success'] == True:
            print('User accepted')
            flowtoken = j['FlowToken']
            break
        request_data.data = {
            "Method": "EndAuth",
            "SessionId": session_id,
            "FlowToken": j['FlowToken'],
            "Ctx": ctx,
            "AuthMethodId": auth_method_id,
            "PollCount": str(tries + 1)
        }
        data = json.dumps(request_data.data)
        print('User still havent authorized')
        time.sleep(2)


def process_auth(session, request_data, otc=None):

    request_data.data = {
        'request': ctx,
        'mfaAuthMethod': auth_method_id,
        'canary': canary,
        'login': login_username,
        'flowToken': flowtoken,
        'hpgrequestid': hpg_request_id,
        'otc': otc
    }

    return session.post('https://login.microsoftonline.com/common/SAS/ProcessAuth', data=request_data.data)


def scrape_process_auth(response, request_data):
    soup = BeautifulSoup(response.text, 'lxml')

    saml_response = soup.find('input', {'name': 'SAMLResponse'})['value']

    request_data.data = {
        'SAMLResponse': saml_response
    }


def post_auth_saml_SSO(session, requets_data):
    return session.post(
        'https://ntnu.blackboard.com/auth-saml/saml/SSO', data=requets_data.data)


def write_to_env_data(session):
    BB_ROUTER = session.cookies['BbRouter']
    bb_router_values = BB_ROUTER.split(',')
    xsrf = bb_router_values[len(bb_router_values) - 1].split(':')
    xsrf_value = xsrf[1]

    enviroment_path = f'{os.path.dirname(os.path.abspath(__file__))}/../'

    f = open(f'{enviroment_path}.env', 'w')
    f.write(f'BB_ROUTER={BB_ROUTER}\n')
    f.write(f'XSRF={xsrf_value}\n')
    f.write(f'BB_USERNAME={login_username}\n')
    f.close()


if __name__ == "__main__":
    load_dotenv()
    login()
