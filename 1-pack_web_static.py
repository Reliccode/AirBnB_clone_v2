#!/usr/bin/python3
""" Function that compress a folder """
from datetime import datetime
from fabric.api import local
import os


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
