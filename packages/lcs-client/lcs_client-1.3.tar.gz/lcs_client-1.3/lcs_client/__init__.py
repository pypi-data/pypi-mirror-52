'''
This is intended to be a serverside client to help with hackru services that biggie back
on lcs login ang user data
'''

from datetime import datetime
from dateutil.parser import parse
from functools import wraps

import requests

LCS_URL_ROOT = 'https://api.hackru.org'
def set_root_url(url):
    '''sets root url. defaults to `https://api.hackru.org`'''
    # this is annoying but gets the autogen docs to work
    global LCS_ROOT_URL
    LCS_ROOT_URL = url

TESTING = False
def set_testing(testing):
    '''weather or not to use test endpoint, defaults to `False`'''
    # this is annoying but gets the autogen docs to work
    global TESTING
    TESTING = testing

class User:
    '''
    a user object to easily call other endpoints on behalf of a user
    constructor logs the user and gets a handle. requires you to pass a token OR a password
    '''
    def __init__(self, email, password=None, token=None):
        if not password and not token:
            raise Exception('must provide token or password to login')

        self.email = email
        if password:
            full_token = login(email, password)
            self.token = full_token['token']

        if token:
            validate_token(email, token)
            self.token = token

    def profile(self):
        '''call lcs to get the user's profile'''
        return get_profile(self.email, self.token)

    def dm_link_for(self, other_user):
        '''get a dm link for another user's slack __NOT IMPLMIMENTED YET__'''
        return get_dm_for(self.email, self.token, other_user)

class ResponseError(Exception):
    '''error with an attached http Response'''
    def __init__(self, response):
        self.response = response
        if response.status_code == 200:
            self.status_code = response.json()['statusCode']
        else:
            self.status_code = response.status_code

    def __str__(self):
            return 'status: %d response: %s' % (self.status_code, self.response.json())

class InternalServerError(ResponseError):
    @staticmethod
    def check(response):
        if response.status_code >= 500 or response.json().get('statusCode', 0) >= 500:
            raise InternalServerError(response)

class RequestError(ResponseError):
    '''ideally you shouldn't receve this. there was an issue with the input to the api'''
    @staticmethod
    def check(response):
        if response.status_code == 400 or response.json()['statusCode'] == 400:
            raise RequestError(response)

class CredentialError(RequestError):
    '''there was an issue login in with that credential, or a token is invalid'''
    @staticmethod
    def check(response):
        if response.status_code == 403 or response.json()['statusCode'] == 403:
            raise CredentialError(response)

def check_response(response):
    InternalServerError.check(response)
    RequestError.check(response)
    CredentialError.check(response)

_login_hooks = []
def on_login(f):
    '''
    decorator. call the decorated function whenever we find a new user
    use case: get their profile and update local db.
    function should take in the user object as the first param
    
    ```python
    @lcs_client.on_login
    def your_func(user_profile):
        # updating the user profile or something
    ```
    '''
    global _login_hooks
    _login_hooks += [f]
    return f

def call_login_hooks(user_profile):
    for hook in _login_hooks:
        hook(user_profile)

_token_cache = {}
# cache of tokens for quickly checking validate and determining if something
# counts as a login. if we validate a token we haven't seen before, it qualifies
# as a login

def validate_token(email, token):
    '''validates an lcs token and email pair'''
    if token in _token_cache:
        # if we've already seen the token we can just check the expiration
        expiration = parse(_token_cache[token]['valid_until'])
    else:
        # else we need to check with lcs and call login hooks
        data = {'email': email, 'token': token}
        response = post('/validate', json=data)

        check_response(response)
        result = response.json()
        user_profile = result['body']
        # find the token we have in the user's profile
        token_object = [tok for tok in user_profile['auth'] if tok['token'] == token][0]
        _token_cache[token] = token_object
        call_login_hooks(user_profile)

        return token_object

def login(email, password):
    '''gets a token for a user'''
    data = {'email': email, 'password': password}
    response = post('/authorize', json=data)

    check_response(response)
    result = response.json()
    token_object = result['body']['auth']

    # insert into cache and call login hooks
    _token_cache[token_object['token']] = token_object
    call_login_hooks(get_profile(email, token_object['token']))

    return token_object

def get_profile(email, token, auth_email=None):
    '''
    gets the profile of a user. add auth_email if you are looking at the users profile
    from a different account
    '''
    if not auth_email:
        auth_email = email

    data = {'email': email, 'token': token, 'auth_email': auth_email,
            'query': {'email': email}}
    response = post('/read', json=data)

    check_response(response)
    return response.json()['body'][0]

def get_dm_for(email, token, other_user):
    '''
    get a dm link to talk with another user on slack. __NOT YET IMPLEMENTED__
    '''
    raise Exception('not yet implemented')

def base_url():
    '''get the lcs base url'''
    if TESTING:
        return LCS_URL_ROOT + '/dev'
    else:
        return LCS_URL_ROOT + '/prod'

def get(endpoint, *args, **kwargs):
    '''does get request to lcs endpoint'''
    return requests.get(base_url() + endpoint, *args, **kwargs)

def post(endpoint, *args, **kwargs):
    '''does post request to lcs endpoint'''
    return requests.post(base_url() + endpoint, *args, **kwargs)

#TODO write tests
#TODO Gen documentation
