#!/usr/bin/python3
""" Function that deploys """
from datetime import datetime
from fabric.api import *
import os
import shlex


env.hosts = ['54.237.53.109', '34.229.69.210']
env.user = "ubuntu"


def deploy():
    """ Compresses and deploys the web_static folder to the web servers"""
    try:
        archive_path = do_pack()
    except Exception as e:
        print("Deployment failed:", str(e))
        return False

    return do_deploy(archive_path)


def do_pack():
    """
    Compresses the contents of the web_static folder into a .tgz archive.
    Returns the archive path if successful, None otherwise.
    """
    try:
        if not os.path.exists("versions"):
            local('mkdir versions')
        t = datetime.now()
        f = "%Y%m%d%H%M%S"
        archive_path = 'versions/web_static_{}.tgz'.format(t.strftime(f))
        local('tar -cvzf {} web_static'.format(archive_path))
        return archive_path
    except Exception as e:
        # Printing the error - Debugging purposes
        print(f"An error occured: {str(e)}")
        return None


def do_deploy(archive_path):
    """ Compresses and deploys the web_static folder to the web servers. """
    if not os.path.exists(archive_path):
        return False
    try:
        name = archive_path.replace('/', ' ')
        name = shlex.split(name)
        name = name[-1]

        wname = name.replace('.', ' ')
        wname = shlex.split(wname)
        wname = wname[0]

        releases_path = "/data/web_static/releases/{}/".format(wname)
        tmp_path = "/tmp/{}".format(name)

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(releases_path))
        run("tar -xzf {} -C {}".format(tmp_path, releases_path))
        run("rm {}".format(tmp_path))
        run("mv {}web_static/* {}".format(releases_path, releases_path))
        run("rm -rf {}web_static".format(releases_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(releases_path))
        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed:", str(e))
        return False
