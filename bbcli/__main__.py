"""RP To-Do entry point script."""
# rptodo/__main__.py

import os
from dotenv import load_dotenv
from bbcli import cli, __app_name__, login
from datetime import datetime

load_dotenv()
cookies = {'BbRouter' : os.getenv("BB_ROUTER")}

def check_valid_date() -> bool:
    tmp = cookies['BbRouter']
    start = int(tmp.find('expires')) + len('expires') + 1
    end = int(tmp.find(','))
    timestmp = int(tmp[start : end])
    print(timestmp)
    expires = datetime.fromtimestamp(timestmp)
    now = datetime.now()
    if expires > now:
        return True
    else: 
        return False

def main():
    if check_valid_date() == False:
        login()

    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()