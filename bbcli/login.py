from urllib import request
import os
from dotenv import load_dotenv
from RequestData import RequestData
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
    response = process_auth(session, request_data)
    scrape_process_auth(response, request_data)
    response = post_auth_saml_SSO(session, request_data)

    write_to_session_data(session)


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
        'has_js': '0',
        'inside_iframe': '0',
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
    auth_method_id = 'PhoneAppNotification'
    hpg_request_id = response.headers['x-ms-request-id']

    request_data.data = '{"AuthMethodId":"PhoneAppNotification","Method":"BeginAuth","ctx":"' + \
        ctx + '","flowToken":"' + flowtoken + '"}'


def begin_auth(session, request_data):

    if auth_method_id == 'PhoneAppNotification':
        begin_phone_app_auth(session, request_data)
    # elif auth_method_id == 'OneWaySMS':
    #     # begin_sms_auth(session, request_data)
    # else:
        # begin_security_key_auth(session, request_data)


def begin_phone_app_auth(session, request_data):
    response = session.post(
        'https://login.microsoftonline.com/common/SAS/BeginAuth', data=request_data.data)

    j = json.loads(response.text)
    app_auth_wait(session, request_data, j['CorrelationId'], j['FlowToken'])


def app_auth_wait(session, request_data, client_request_id, flow_token):
    global flowtoken

    request_data.data = '{"Method":"EndAuth","SessionId":"' + session_id + '","FlowToken":"' + \
        flow_token + '","Ctx":"' + ctx + \
        '","AuthMethodId":"PhoneAppNotification","PollCount":1}'
    request_data.headers = {
        'client-request-id': client_request_id,
    }

    for tries in range(10):
        response = session.post(
            'https://login.microsoftonline.com/common/SAS/EndAuth', data=request_data.data, headers=request_data.headers)
        j = json.loads(response.text)
        if j['Success'] == True:
            print('User accepted')
            flowtoken = j['FlowToken']
            break
        request_data.data = '{"Method":"EndAuth","SessionId":"' + session_id + '","FlowToken":"' + \
            j['FlowToken'] + '","Ctx":"' + ctx + \
            '","AuthMethodId":"PhoneAppNotification","PollCount":' + \
            str(tries + 1) + '}'
        print('User still havent authorized')
        time.sleep(2)


def process_auth(session, request_data):
    request_data.data = {
        'type': '22',
        'request': ctx,
        'mfaAuthMethod': 'PhoneAppNotification',
        'canary': canary,
        'login': login_username,
        'flowToken': flowtoken,
        'hpgrequestid': hpg_request_id,
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


def write_to_session_data(session):
    BB_ROUTER = session.cookies['BbRouter']
    bb_router_values = BB_ROUTER.split(',')
    xsrf = bb_router_values[len(bb_router_values) - 1].split(':')
    xsrf_value = xsrf[1]

    f = open('.env', 'a')
    f.write("BB_ROUTER=" + BB_ROUTER + "\n")
    f.write("XSRF=" + xsrf_value + "\n")
    f.close()


if __name__ == "__main__":
    load_dotenv()
    login()
