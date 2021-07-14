import requests
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
        if response.status_code == 200:  # Login succeeded => save token
            result = response.json()
            token = result['token']
            cache_file = open(settings.cache_file, 'w')
            cache_file.write(token)
        else:  # Login failed
            raise Exception(response.text)
    except:
        raise Exception(settings.server_not_responding)


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


def create_contract(contract_details):
    try:
        token = settings.token
        if token:
            response = requests.post(settings.host_url + settings.client_url_prefix + 'createContract',
                                     headers={"token": token},
                                     json={
                                         'filename': contract_details['filename'],
                                         'download_counts': contract_details['download_counts'],
                                         'file_size': contract_details['file_size'],
                                         'duration': contract_details['duration'],
                                         'segments_count': contract_details['segments_count'],
                                         'segment': contract_details['segment']
                                     })
            if response.status_code == 200:
                return True
            else:
                return settings.redirect_to_login
        else:  # Get user files.
            return settings.redirect_to_login
    except:
        raise Exception(settings.server_not_responding)
