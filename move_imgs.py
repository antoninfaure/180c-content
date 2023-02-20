import os
import shutil
from os import path

src = path.join('.', 'crieur')
dest = path.join('.', 'temp')

if path.exists(dest):
    shutil.rmtree(dest)
os.makedirs(dest)

shutil.copytree(src, dest, dirs_exist_ok=True)

for root, directories, files in os.walk(dest, topdown=False):
    for name in files:
        file_path = path.join(root, name)
        _, ext = path.splitext(file_path)
        if (name != 'config_crieur.json'):
            if (ext == '.json'):
                os.remove(file_path)
            else:
                parent = path.dirname(path.dirname(file_path))
                shutil.move(file_path, path.join(parent, name))
    for name in directories:
        if (name == 'images'):
            os.rmdir(path.join(root, name))