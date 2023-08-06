import os, re, shutil


def transfer_notebooks(root):
    for dirname, _, files in os.walk(root):
        for file in files:
            if re.search(".ipynb$", file):
                doc = os.path.join(dirname, file)
                dest = dirname.replace('content', 'docs')
                shutil.copy(doc, dest)
