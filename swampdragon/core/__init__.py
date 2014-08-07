from django.core.management import call_command
import sys
from os.path import abspath, dirname, join
from os import path
import os


def _add_swampdragon_to_installed_apps(settings):
    installed_apps_start = -1
    installed_apps_end = -1
    for i in range(0, len(settings)):
        if settings[i].decode().startswith('INSTALLED_APPS'):
            installed_apps_start = i
            break
    if installed_apps_start == -1:
        raise Exception('no installed apps found')

    for i in range(installed_apps_start, len(settings)):
        if ')' in settings[i].decode():
            installed_apps_end = i
            break
    swampdragon = '    \'swampdragon\',\n'.encode('utf-8')
    settings.insert(installed_apps_end, swampdragon)
    return settings


def run():
    args = sys.argv
    if len(args) is 1:
        print('no command selected')
        return
    if 'startproject' in args:
        if len(args) < 3:
            print('supply a project name')
            return
        start_project(args[2])


def start_project(project_name):
    call_command('startproject', project_name)
    root = dirname(dirname(abspath(__file__)))
    template_dir = path.join(root, 'app_templates')
    settings_template = path.join(template_dir, 'sd_settings.py')

    current_dir = os.getcwd()
    project_settings_file = path.join(path.join(path.join(current_dir, project_name), project_name), 'settings.py')
    with open(settings_template, 'rb') as template_file:
        socket_settings = template_file.readlines()

    with open(project_settings_file, 'rb') as settings_file:
        settings = settings_file.readlines()
    settings = _add_swampdragon_to_installed_apps(settings)
    settings += socket_settings

    with open(project_settings_file, 'wb') as settings_file:
        settings_file.writelines(settings)
