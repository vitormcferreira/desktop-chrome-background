import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

from PIL import Image

GOOGLE_BACKGROUND_FILE_PATH = Path(
    '/home/vitor/.config/google-chrome/Default/background.jpg')
LOG_FILE_NAME = Path('/home/vitor/my-daemons/my-logs.log')


def log_error(msg):
    now = datetime.astimezone(datetime.now())
    with open(LOG_FILE_NAME, 'a') as log:
        log.write(
            f'[{now}] desktop-chrome-background: {msg}"\n'
        )


def get_background_file_path():
    # retorna o caminho da imagem no formato 'file:///path/to/image.ext'
    background_image_dconf_path = subprocess.run(
        ['gsettings', 'get', 'org.gnome.desktop.background', 'picture-uri'],
        capture_output=True,
        text=True
    ).stdout
    
    # remove as aspas e 'file://'
    background_image_path = background_image_dconf_path[8:-2]
    # escapa os caracteres %xx pelos seus equivalentes
    # Por exemplo: espaços são substituídos por %xx em 
    # background_image_dconf_path.
    path = unquote(background_image_path)

    return path


def convert_background_to_jpg(background_path):
    with Image.open(background_path) as img:
        # Converte para RGB pois é preciso para a conversão para JPEG
        img.convert('RGB').save(background_path, 'JPEG')


def save_log(background_image_path, new_background_image_path):
    now = datetime.astimezone(datetime.now())

    with open(LOG_FILE_NAME, 'a') as log:
        log.write(
            f'[{now}] desktop-chrome-background: "{background_image_path}" '
            f'copy to "{new_background_image_path}"\n'
        )


def main():
    background_image_path = get_background_file_path()

    try:
        shutil.copy(background_image_path, GOOGLE_BACKGROUND_FILE_PATH)
        convert_background_to_jpg(GOOGLE_BACKGROUND_FILE_PATH)
    except Exception as e:
        log_error(e.args)
    else:
        save_log(background_image_path, GOOGLE_BACKGROUND_FILE_PATH)


if __name__ == '__main__':
    main()
