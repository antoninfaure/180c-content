import os
import shutil
from os import path

# Move crieur
src = path.join('.', 'crieur')
dest = path.join('.', 'static/crieur')

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

# Move articles
src = path.join('.', 'articles/images')
dest = path.join('.', 'static/images/articles')

if path.exists(dest):
    shutil.rmtree(dest)
os.makedirs(dest)

shutil.copytree(src, dest, dirs_exist_ok=True)

for file_path in os.listdir(dest):
    # check if current path is a file
    if (not os.path.isfile(os.path.join(dest, file_path))):
        os.rmdir(path.join(dest, file_path))