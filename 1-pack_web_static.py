#!/usr/bin/python3
"""
Fabric script to genereate tgz archive
execute: fab -f 1-pack_web_static.py do_pack
"""

from fabric.api import local
from datetime import datetime
from os.path import isdir

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    
    All files in the folder web_static must be added to the final archive.
    All archives must be stored in the folder versions (the function creates this folder if it doesn’t exist).
    The name of the archive created is web_static_<year><month><day><hour><minute><second>.tgz.
    
    Returns:
        str: The archive path if the archive has been correctly generated, otherwise None.
    """
    # Create versions folder if it doesn't exist
    if not isdir("versions"):
        local("mkdir -p versions")

    # Generate the archive name
    now = datetime.now()
    archive_name = "web_static_{}.tgz".format(now.strftime("%Y%m%d%H%M%S"))

    # Create the archive
    result = local("tar -czvf versions/{} web_static".format(archive_name))

    # Return the archive path if creation was successful, otherwise None
    if result.succeeded:
        return "versions/{}".format(archive_name)
    else:
        return None
