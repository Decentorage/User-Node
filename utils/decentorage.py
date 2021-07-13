import requests
from .settings import Settings
settings = Settings()


def user_login(username, password):
    response = requests.post(settings.host_url + settings.client_url_prefix + 'signin',
                             json={
                                'username': username,
                                'password': password
                                })
    if response.status_code == 200:     # Login succeeded => save token
        result = response.json()
        token = result['token']
        cache_file = open(settings.cache_filename, 'w')
        cache_file.write(token)
    else:  # Login failed
        raise Exception(response.text)


def get_user_files(token):
    if token:
        response = requests.get(settings.host_url + settings.client_url_prefix + 'getFiles'
                                , headers={"token": token})
        if response.status_code == 200:
            return response.json()
        else:
            return settings.redirect_to_login
    else:  # Get user files.
        return settings.redirect_to_login
