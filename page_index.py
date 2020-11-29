import os
import fnmatch
import shutil
import zipfile
import re

path = input('path: ')
file = input('epub name (without .epub): ')

path_file = os.path.join(path, file)
shutil.copy(path_file + '.epub', path_file + '.zip')
with zipfile.ZipFile(path_file + '.zip', 'r') as zip_ref:
    zip_ref.extractall(path_file)
    
path_html = os.path.join(path_file, 'html')
path_image = os.path.join(path_file, 'image')
html_list = [fn for fn in os.listdir(path_html) if re.match(r'\d+\.html', fn)]

for fh in html_list:
    with open(os.path.join(path_html, fh), encoding='UTF-8') as f_html:
        string_html = ''.join(f_html.readlines())
        image_fn = re.search(r'\.\./image/vol\.moe-\d+\.jpg', string_html).group()
        image_order = 'cq_' + fh.split('.')[0] + '.jpg'
        shutil.move(os.path.join(path_image, image_fn), os.path.join(path_image, image_order)) 

os.remove(path_file + '.zip')