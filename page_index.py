import os
import shutil
import zipfile
import re
import subprocess

from config import Config


def unzip_from_epub(path, origin_filename):
    short_filename = re.search(r'\[(\w+)]Vol_.*', origin_filename).group()

    origin_path_file = os.path.join(path, origin_filename)
    path_filename = os.path.join(path, short_filename)
    shutil.copy(origin_path_file + '.epub', path_filename + '.zip')
    with zipfile.ZipFile(path_filename + '.zip', 'r') as zip_ref:
        zip_ref.extractall(path_filename)
    return path_filename


def rename_image_name_inorder(path_filename):
    path_html = os.path.join(path_filename, 'html')
    path_image = os.path.join(path_filename, 'image')
    html_list = [fn for fn in os.listdir(path_html)
                 if re.match(r'\d+\.html', fn)]

    try:
        for fh in html_list:
            with open(os.path.join(path_html, fh), encoding='UTF-8') as f_html:
                string_html = ''.join(f_html.readlines())
                image_fn = re.search(
                    r'\.\./image/(vol(?:\.moe)?)-\d+\.(?:jpg|png)',
                    string_html
                ).group()
                image_order = 'cq_' + fh.split('.')[0] + '.jpg'
                shutil.move(os.path.join(path_image, image_fn),
                            os.path.join(path_image, image_order))
    except AttributeError:
        print('Something wrong with regular expression!!')
        raise
    finally:
        os.remove(path_filename + '.zip')


def kindle_comic_converter(path_filename):
    subprocess.run(
        [Config.kcc_c2e_path,
         f'--output={path_filename}.cbz',
         '--profile=KoGHD',
         '--format=CBZ',
         '-u', '-s',
         f'{path_filename}/image']
    )


if __name__ == '__main__':
    input_path = input('path: ')
    file_list = []
    while filename := input('\nepub name (without .epub): '):
        absolute_filename = unzip_from_epub(input_path, filename)
        file_list.append(absolute_filename)

    for file in file_list:
        rename_image_name_inorder(file)
        kindle_comic_converter(file)
        shutil.rmtree(absolute_filename)
