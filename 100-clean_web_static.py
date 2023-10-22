#!/usr/bin/python3
"""
Module: 2-do_clean.py
Function: do_clean
Cleans up old versions of web_static on the server.
"""
from fabric.api import *

# Define remote hosts and user
env.hosts = ['54.237.53.109', '34.229.69.210']
env.user = "ubuntu"


def do_clean(number=0):
    """
    Clean up old versions of web_static on the server.

    Args:
        number (int, optional): Number of versions to keep. Defaults to 0.

    Returns:
        None
    """

    number = int(number)

    if number == 0:
        number = 2
    else:
        number += 1

    local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(number))
    path = '/data/web_static/releases'
    run('cd {} ; ls -t | tail -n +{} | xargs rm -rf'.format(path, number))
