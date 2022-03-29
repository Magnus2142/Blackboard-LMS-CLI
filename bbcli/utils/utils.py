from datetime import datetime 
from typing import Dict, List
from requests import Session
import html2text


def check_valid_key(obj, key) -> bool:
	# print("the keys are", obj.keys())
	if key not in obj.keys():
		print(f'The key: \"{key}\" is not in the object')
		return False
	else:
		return True

def check_response(response) -> bool:
	invalid_statuscodes = [401, 403, 404]
	if response.status_code in invalid_statuscodes:
		print(response.json()['status'])
		print(response.json()['message'])
		return False 
	else: 
		return True

def check_valid_date(cookies) -> bool:
    tmp = cookies['BbRouter']
    start = int(tmp.find('expires')) + len('expires') + 1
    end = int(tmp.find(','))
    timestmp = int(tmp[start : end])
    print(timestmp)
    expires = datetime.fromtimestamp(timestmp)
    now = datetime.now()
    if expires >= now:
        return True
    else: 
        return False


def set_cookies(session: Session, cookies: List):
	for cookie in cookies:
    	 session.cookies.set(cookie['name'], cookie['value'])


def set_headers(session: Session, headers: List):
	for header in headers:
		session.headers.update(header)


def html_to_text(html_data: str):
	to_text = html2text.HTML2Text()
	return to_text.handle(html_data)