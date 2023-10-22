#!/usr/bin/env python3
"""
Fabric script to generate a .tgz archive from the web_static folder.
"""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Compresses the contents of the web_static folder into a .tgz archive.
    Returns the archive path if successful, None otherwise.
    """
    try:
        current_time = datetime.now()
        archive_name = "web_static_{}.tgz".format(
            current_time.strftime("%Y%m%d%H%M%S"))
        local("mkdir -p versions")
        local("tar -czvf versions/{} web_static".format(archive_name))
        archive_path = os.path.join("versions", archive_name)
        return archive_path

    except Exception as e:
        return None
