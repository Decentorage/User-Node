import requests
import json
import os
helper = None


def init_decentorage(helper_obj):
    """
    This function initializes decentorage module.
    :param helper_obj: instance of the helper object.
    """
    global helper
    helper = helper_obj


def user_login(username, password):
    """
    This function is used to do client login.
    :param username: username of the client.
    :param password: password of the client.
    :return: return response to the client.
    """
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


def get_price(contract_details, ui):
    """
    This function is used to get the price of a specific contract details.
    :param contract_details: dictionary holds the contract details.
    :param ui: ui object
    :return: price
    """
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
        else:  # Get user files.
            worker_error_page("Please Login again", "", ui, ui.login_page)
            return False
    except:
        worker_error_page("Error", helper.server_not_responding, ui)
        response = False
        return False
    finally:
        if response:
            if response.status_code == 200:
                return response.json()['price']
            else:
                worker_error_page("Please Login again", "", ui, ui.login_page)
                return False


def get_user_files(ui):
    """
    This function returns user stored files in decentorage to download them.
    :param ui: ui object.
    :return:user stored files.
    """
    try:
        token = helper.token
        if token:
            response = requests.get(helper.host_url + helper.client_url_prefix + 'getFiles',
                                    headers={"token": token})
        else:  # Get user files.
            worker_error_page("Please Login again", "", ui, ui.login_page)
            return False
    except:
        worker_error_page("Error", helper.server_not_responding, ui)
        response = False
        return False
    finally:
        if response:
            if response.status_code == 200:
                return response.json()
            else:
                worker_error_page("Please Login again", "", ui, ui.login_page)
                return False


def get_user_state(ui):
    """
    This function gets the user current state
    :param ui: ui object
    :return: state
    """
    try:
        token = helper.token
        if token:
            response = requests.get(helper.host_url + helper.client_url_prefix + 'getState',
                                    headers={"token": token})
        else:  # Get user files.
            worker_error_page("Please Login again", "", ui, ui.login_page)
            return False
    except:
        worker_error_page("Error", helper.server_not_responding, ui)
        response = False
        return False
    finally:
        if response:
            if response.status_code == 200:
                return response.json()['state']
            else:
                worker_error_page("Please Login again", "", ui, ui.login_page)
                return False


def create_file(contract_details, ui):
    """

    :param contract_details: the details of the contract of a specific file.
    :param ui: ui object.
    :return: True if file is created successfully and false if any problem occurred.
    """
    try:
        token = helper.token
        if token:
            response = requests.post(helper.host_url + helper.client_url_prefix + 'createFile',
                                     headers={"token": token},
                                     json=json.dumps(contract_details))
        else:  # Get user files.
            worker_error_page("Please Login again", "", ui, ui.login_page)
            return False
    except:
        worker_error_page("Error", helper.server_not_responding, ui)
        response = False
        return False
    finally:
        if response:
            if response.status_code == 201:
                return True
            elif response.status_code == 409:
                worker_error_page("Error", "This file already stored.", ui)
                return False
            else:
                ui.stackedWidget.setCurrentWidget(ui.upload_main_page)
                return False


def get_pending_file_info(ui):
    """
    This function gets pending file information
    :param ui:
    :return: information
    """
    try:
        token = helper.token
        if token:
            response = requests.get(helper.host_url + helper.client_url_prefix + 'getFileInfo',
                                    headers={"token": token})
        else:
            worker_error_page("Please Login again", "", ui, ui.login_page)
            response = False
            return False
    except:
        worker_error_page("Error", helper.server_not_responding, ui)
        return False
    finally:
        if response:
            if response.status_code == 200:
                return response.json()
            else:
                worker_error_page("Please Login again", "", ui, ui.login_page)
                return False


def shard_done_uploading(shard_id, audits, ui):
    """
    This function is called when the shard is uploaded at the host.
    :param shard_id: the shard id that is uploaded.
    :param audits: the audits of this shard.
    :param ui: ui object.
    """
    try:
        token = helper.token
        if token:
            response = requests.post(helper.host_url + helper.client_url_prefix + 'shardDoneUploading',
                                     json={
                                            "shard_id": os.path.basename(shard_id),
                                            "audits": audits
                                        },
                                     headers={"token": token})
        else:  # Get user files.
            worker_error_page("Please Login again", "", ui, ui.login_page)
            return False
    except:
        worker_error_page("Error", helper.server_not_responding, ui)
        response = False
        return False
    finally:
        if response:
            if response.status_code == 200:
                return True
            else:
                worker_error_page("Please Login again", "", ui, ui.login_page)
                return False


def file_done_uploading(ui):
    """
    This function is called when the file is uploaded as a whole.
    :param ui: ui object.
    """
    try:
        token = helper.token
        if token:
            response = requests.get(helper.host_url + helper.client_url_prefix + 'fileDoneUploading',
                                    headers={"token": token})
    except:
        worker_error_page("Error", helper.server_not_responding, ui)
        response = False
        return False
    finally:
        if response:
            if response.status_code == 200:
                return True
            else:
                worker_error_page("Please Login again", "", ui, ui.login_page)
                return False


def start_download(filename, ui):
    """
    This function is called when the user wants to download a file.
    :param filename: the name of the file that will be downloaded.
    :param ui: ui object.
    :return: information needed when downloading shards.
    """
    try:
        token = helper.token
        if token:
            response = requests.post(helper.host_url + helper.client_url_prefix + 'startDownload',
                                     json={
                                        "filename": filename
                                     },
                                     headers={"token": token})
        else:  # Get user files.
            worker_error_page("Please Login again", "", ui, ui.login_page)
            return False
    except:
        worker_error_page("Error", helper.server_not_responding, ui)
        response = False
        return False
    finally:
        if response:
            if response.status_code == 200:
                return response.json()["segments"]
            elif response.status_code == 404 or response.status_code == 405:
                worker_error_page("Error", response.text(), ui)
                return False
            else:
                worker_error_page("Please Login again", "", ui, ui.login_page)
                return False


def worker_error_page(title, body, gui, target=None):
    """
    Function that show errors to the user.
    :param title: title of the error.
    :param body: body of the error.
    :param gui: gui object.
    :param target: target page.
    """
    gui.error_body.setText(body)
    gui.error_title.setText(title)
    if target:
        gui.error_source_page = target
        try:
            # Remove cached file
            gui.error_source_page = gui.login_page
            os.remove(helper.cache_file)
        except:
            print("No cache file")
    else:
        gui.error_source_page = gui.stackedWidget.currentWidget()
    gui.stackedWidget.setCurrentWidget(gui.error_page)
