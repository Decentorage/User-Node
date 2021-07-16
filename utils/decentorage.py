import requests
import json
helper = None


def init_decentorage(helper_obj):
    global helper
    helper = helper_obj

# TODO: implement login redirect


def user_login(username, password):
    try:
        response = requests.post(helper.host_url + helper.client_url_prefix + 'signin',
                                 json={
                                     'username': username,
                                     'password': password
                                 })
    except:
        raise Exception(helper.server_not_responding)
    if response.status_code == 200:  # Login succeeded => save token
        result = response.json()
        token = result['token']
        cache_file = open(helper.cache_file, 'w')
        cache_file.write(token)
    else:  # Login failed
        raise Exception(response.text)


def get_price(contract_details):
    try:
        token = helper.token
        if token:
            response = requests.get(helper.host_url + helper.client_url_prefix + 'getPrice',
                                    params={
                                        "download_count": contract_details['download_count'],
                                        "duration_in_months": contract_details['duration_in_months'],
                                        "file_size": contract_details['file_size']
                                    },
                                    headers={"token": token})
            if response.status_code == 200:
                return response.json()['price']
            else:
                return helper.redirect_to_login
        else:  # Get user files.
            return helper.redirect_to_login
    except:
        raise Exception(helper.server_not_responding)


def get_user_files():
    try:
        token = helper.token
        if token:
            response = requests.get(helper.host_url + helper.client_url_prefix + 'getFiles',
                                    headers={"token": token})
            if response.status_code == 200:
                return response.json()
            else:
                return helper.redirect_to_login
        else:  # Get user files.
            return helper.redirect_to_login
    except:
        raise Exception(helper.server_not_responding)


def get_user_state():
    try:
        token = helper.token
        if token:
            response = requests.get(helper.host_url + helper.client_url_prefix + 'getState',
                                    headers={"token": token})
            if response.status_code == 200:
                return response.json()['state']
            else:
                return helper.redirect_to_login
        else:  # Get user files.
            return helper.redirect_to_login
    except:
        raise Exception(helper.server_not_responding)


def create_file(contract_details):
    try:
        token = helper.token
        if token:
            response = requests.post(helper.host_url + helper.client_url_prefix + 'createFile',
                                     headers={"token": token},
                                     json=json.dumps(contract_details))
            if response.status_code == 200:
                return True
            elif response.status_code == 409:
                raise Exception("This file already stored.")
            else:
                return False
        else:  # Get user files.
            return False
    except:
        raise Exception(helper.server_not_responding)


def get_pending_file_info():
    try:
        token = helper.token
        if token:
            response = requests.get(helper.host_url + helper.client_url_prefix + 'getFileInfo',
                                    headers={"token": token})
            if response.status_code == 200:
                return response.json()
            else:
                return helper.redirect_to_login
        else:  # Get user files.
            return helper.redirect_to_login
    except:
        raise Exception(helper.server_not_responding)
