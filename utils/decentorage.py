import requests
import json
settings = None


def init_decentorage(settings_obj):
    global settings
    settings = settings_obj


def user_login(username, password):
    try:
        response = requests.post(settings.host_url + settings.client_url_prefix + 'signin',
                                 json={
                                     'username': username,
                                     'password': password
                                 })
    except:
        raise Exception(settings.server_not_responding)
    if response.status_code == 200:  # Login succeeded => save token
        result = response.json()
        token = result['token']
        cache_file = open(settings.cache_file, 'w')
        cache_file.write(token)
    else:  # Login failed
        raise Exception(response.text)


def get_user_files():
    try:
        token = settings.token
        if token:
            response = requests.get(settings.host_url + settings.client_url_prefix + 'getFiles',
                                    headers={"token": token})
            if response.status_code == 200:
                return response.json()
            else:
                return settings.redirect_to_login
        else:  # Get user files.
            return settings.redirect_to_login
    except:
        raise Exception(settings.server_not_responding)


def get_user_state():
    try:
        token = settings.token
        if token:
            response = requests.get(settings.host_url + settings.client_url_prefix + 'getState',
                                    headers={"token": token})
            if response.status_code == 200:
                return response.json()['state']
            else:
                return settings.redirect_to_login
        else:  # Get user files.
            return settings.redirect_to_login
    except:
        raise Exception(settings.server_not_responding)


def create_file(contract_details):
    try:
        token = settings.token
        if token:
            response = requests.post(settings.host_url + settings.client_url_prefix + 'createFile',
                                     headers={"token": token},
                                     json=json.dumps(contract_details))
            if response.status_code == 200:
                return True
            else:
                return settings.redirect_to_login
        else:  # Get user files.
            return settings.redirect_to_login
    except:
        raise Exception(settings.server_not_responding)

# TODO: Get price
