import os
from datetime import datetime
import shutil
import subprocess
from urllib.parse import unquote
from PIL import Image


BASE_GOOGLE_DIR = '/home/vitor/.config/google-chrome/Default/'
LOG_FILE_NAME = '/home/vitor/.meus-logs.log'


def log_error(msg):
    now = datetime.astimezone(datetime.now())
    with open(LOG_FILE_NAME, 'a') as log:
        log.write(
            f'[{now}] desktop-chrome-background: {msg}"\n'
        )


def get_background_files_path():
    background_image_dconf_path = subprocess.run(
        ['gsettings', 'get', 'org.gnome.desktop.background', 'picture-uri'],
        capture_output=True,
        text=True
    ).stdout

    background_image_path = unquote(background_image_dconf_path[8:-2])
    _, file_ext = os.path.splitext(background_image_path)

    new_background_image_path = os.path.join(
        BASE_GOOGLE_DIR, f'background{file_ext}')

    return background_image_path, new_background_image_path


def convert_background_to_jpg(background_path):
    file_name, _ = os.path.splitext(background_path)
    # O arquivo deve estar no formato .jpg
    new_background_path = file_name + '.jpg'

    with Image.open(background_path) as img:
        # Converte para RGB pois é preciso para a conversão para JPEG
        img.convert('RGB').save(new_background_path, 'JPEG')


def save_log(background_image_path, new_background_image_path):
    now = datetime.astimezone(datetime.now())

    with open(LOG_FILE_NAME, 'a') as log:
        log.write(
            f'[{now}] desktop-chrome-background: "{background_image_path}" '
            f'copy to "{new_background_image_path}"\n'
        )


def main():
    background_image_path, new_background_image_path = get_background_files_path()

    try:
        shutil.copy(background_image_path, new_background_image_path)
        convert_background_to_jpg(new_background_image_path)
    except Exception as e:
        log_error(e.args)
    else:
        save_log(background_image_path, new_background_image_path)


if __name__ == '__main__':
    main()
