from pathlib import Path

from environs import Env

from comics_functions import fetch_random_comics
from vk_api_functions import get_wall_upload_server, \
                             upload_photo_to_server, post_on_wall


IMAGES_DIR = 'media/'


def main():
    Path(IMAGES_DIR).mkdir(parents=True, exist_ok=True)
    env = Env()
    env.read_env()
    group_id = env.int('VK_GROUP_ID')
    vk_token = env.str('VK_API_TOKEN')
    img_path, comics_sign = fetch_random_comics(IMAGES_DIR)
    try:
        upload_url = get_wall_upload_server(group_id, vk_token)
        vk_server_data = upload_photo_to_server(
            img_path,
            upload_url,
            group_id,
            vk_token
        )
        post_on_wall(vk_server_data, group_id, vk_token, comics_sign)
    finally:
        Path.unlink(img_path)


if __name__ == '__main__':
    main()
