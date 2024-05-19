#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static folder
and distributes an archive to web servers
"""

from fabric.api import env, put, run, local
from datetime import datetime
from os.path import exists, isdir

env.hosts = ['100.24.74.236', '52.3.241.18']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    
    All files in the folder web_static must be added to the final archive.
    All archives must be stored in the folder versions (the function creates this folder if it doesn’t exist).
    The name of the archive created is web_static_<year><month><day><hour><minute><second>.tgz.
    
    Returns:
        str: The archive path if the archive has been correctly generated, otherwise None.
    """
    if not isdir("versions"):
        local("mkdir -p versions")
    now = datetime.now()
    archive_name = "web_static_{}.tgz".format(now.strftime("%Y%m%d%H%M%S"))
    result = local("tar -czvf versions/{} web_static".format(archive_name))
    if result.succeeded:
        return "versions/{}".format(archive_name)
    else:
        return None

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    
    Args:
        archive_path (str): The path to the archive file
    
    Returns:
        bool: True if all operations were successful, otherwise False
    """
    if not exists(archive_path):
        return False

    try:
        # Upload archive to /tmp/ directory of web server
        put(archive_path, '/tmp/')
        
        # Extract archive name and folder name
        filename = archive_path.split('/')[-1]
        folder_name = filename.split('.')[0]
        
        # Create target directory
        run('mkdir -p /data/web_static/releases/{}/'.format(folder_name))
        
        # Uncompress the archive
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(filename, folder_name))
        
        # Delete the archive from web server
        run('rm /tmp/{}'.format(filename))
        
        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')
        
        # Create a new symbolic link
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(folder_name))
        
        return True
    except Exception as e:
        print(e)
        return False

# Deploy the specified archive
if __name__ == "__main__":
    archive_path = "versions/web_static_20240519104758.tgz"
    if do_deploy(archive_path):
        print("Deployment succeeded")
    else:
        print("Deployment failed")
