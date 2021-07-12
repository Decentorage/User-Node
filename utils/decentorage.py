import requests
from .settings import Settings
settings = Settings()


def client_login(username, password):
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
