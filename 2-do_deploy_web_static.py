#!/usr/bin/python3
"""
Function: do_deploy
Compresses and deploys a folder to web servers.
"""

from datetime import datetime
from fabric.api import *
import shlex
import os

env.hosts = ['54.237.53.109', '34.229.69.210']
env.user = "ubuntu"


def do_deploy(archive_path):
    """
    Compresses and deploys the web_static folder to the web servers.

    Args:
        archive_path (str): The path to the archive file to be deployed.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Extract archive name from path
        name = archive_path.split("/")[-1]

        # Create release and temporary paths
        wname = name.replace('.', ' ')
        wname = shlex.split(wname)
        wname = wname[0]
        releases_path = "/data/web_static/releases/{}/".format(wname)
        tmp_path = "/tmp/{}".format(name)

        # Upload archive
        put(archive_path, "/tmp/")

        # Create directories, extract, and cleanup
        run("mkdir -p {}".format(releases_path))
        run("tar -xzf {} -C {}".format(tmp_path, releases_path))
        run("rm {}".format(tmp_path))
        run("mv {}web_static/* {}".format(releases_path, releases_path))
        run("rm -rf {}web_static".format(releases_path))
        run("rm -rf /data/web_static/current")

        # Create symbolic link
        run("ln -s {} /data/web_static/current".format(releases_path))
        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed:", str(e))
        return False
