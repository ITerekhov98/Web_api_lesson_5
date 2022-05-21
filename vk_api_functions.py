import requests

VK_API_VERSION = '5.131'


class VkApiError(requests.HTTPError):
    pass


def catch_vk_api_error(response):
    if 'error' in response.keys():
        raise VkApiError(
            f"error_code: {response['error']['error_code']}",
            response['error']['error_msg'],
        )


def get_wall_upload_server(group_id, access_token):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    post_data = {
        'group_id': group_id,
        'access_token': access_token,
        'v': VK_API_VERSION
    }
    response = requests.post(url, data=post_data)
    response.raise_for_status()
    serialized_response = response.json()
    catch_vk_api_error(serialized_response)
    return serialized_response['response']['upload_url']


def upload_photo_to_server(img_path, upload_url, group_id, access_token):
    with open(img_path, 'rb') as file:
        files = {'photo': file}
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        serialized_response = response.json()
        catch_vk_api_error(serialized_response)
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    post_data = {
        'group_id': group_id,
        'photo': serialized_response['photo'],
        'server': serialized_response['server'],
        'hash': serialized_response['hash'],
        'access_token': access_token,
        'v': VK_API_VERSION
    }
    response = requests.post(url, data=post_data)
    response.raise_for_status()
    vk_server_data = response.json()
    catch_vk_api_error(vk_server_data)
    return {
        'owner_id': vk_server_data['response'][0]['owner_id'],
        'media_id': vk_server_data['response'][0]['id']
    }


def post_on_wall(vk_server_data, group_id, access_token, text):
    url = 'https://api.vk.com/method/wall.post'
    post_data = {
        'owner_id': -group_id,
        'from_group': 1,
        'attachments': 'photo{}_{}'.format(
            vk_server_data['owner_id'],
            vk_server_data['media_id'],
            ),
        'message': text,
        'access_token': access_token,
        'v': VK_API_VERSION
    }
    response = requests.post(url, data=post_data)
    response.raise_for_status()
    catch_vk_api_error(response.json())
