import requests
from fake_useragent import UserAgent

# Username and password for a Metaculus.com account
# Account must have been created via email, not Google or FB
USERNAME = "Matthew_Barnett"
PASSWORD = "J#%QD&O&W9ms,.9"

ua = UserAgent()
main_session = requests.Session()
main_session.headers.update({'User-Agent': ua.firefox})

# Necessary to avoid CSRF token errors?
main_session.get('https://www.metaculus.com/')

# Logging in
def login(u, p):
    global main_session, pandemic_session
    main_session.post('https://www.metaculus.com/api2/accounts/login/', data={'username': u, 'password': p})

login(USERNAME, PASSWORD)
