import os
from setuptools import setup

def install_deps():
    default = open('reqirements.txt', 'r').readlines()
    new_pkgs = []
    for resource in default:
        if 'git+ssh' in resource or 'git+https' in resource:
            pass
        else:
            new_pkgs.append(resource.strip())
    return new_pkgs

pkgs = install_deps()

setup(
    name='Cardealershipbot',
    version = '0.1',
    description='Bot-shop',
    url = 'https://github.com/MrFlava/cardealershipbotv2',
    author = 'MrFlava',
    packages=["src"],
    install_requires=pkgs,
    python_requires='>3.6.0',)
if not os.path.exists('logs'):
    os.mkdir('logs')
