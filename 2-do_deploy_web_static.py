#!/usr/bin/python3
"""
Distributes an archive to my web servers,
using the function do_deploy
"""
from fabric.api import *
from datetime import datetime
import os

env.hosts = ['100.26.247.104', '34.224.16.213']
env.warn_only = True


def do_pack():
    '''
    Generates a tgz archive from the
    contents of the web_static folder
    '''
    try:
        local('mkdir -p versions')
        datetime_format = '%Y%m%d%H%M%S'
        archive_path = 'versions/web_static_{}.tgz'.format(
            datetime.now().strftime(datetime_format))
        local('tar -cvzf {} web_static'.format(archive_path))
        print('web_static packed: {} -> {}'.format(archive_path,
              os.path.getsize(archive_path)))
    except:
        return None



def do_deploy(archive_path, ssh_key, username):
    """
    Distributes an archive to the web servers
    """

    env.key_filename = ssh_key
    env.user = username

    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the temporary folder on the server
        put(archive_path, "/tmp/")

        # Extract the filename from the archive path
        archive_filename = archive_path.split('/')[-1]
        archive_folder = archive_filename.split('.')[0]

        # Create the destination directory for the archive files
        run("mkdir -p /data/web_static/releases/{}/".format(archive_folder))

        # Uncompress the archive into the destination directory
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive_filename, archive_folder))

        # Delete the uploaded archive
        run("rm /tmp/{}".format(archive_filename))

        # Move the files to the final location
        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(archive_folder, archive_folder))

        # Remove the empty web_static directory
        run("rm -rf /data/web_static/releases/{}/web_static".format(archive_folder))

        # Delete the old symbolic link (if exists)
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(archive_folder))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Deployment failed: {}".format(e))
        return False


def parse_arguments():
    parser = argparse.ArgumentParser(description='Distribute an archive to web servers.')
    parser.add_argument('archive_path', type=str, help='Path to the archive')
    parser.add_argument('ssh_key', type=str, help='SSH key file path')
    parser.add_argument('username', type=str, help='SSH username')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    do_deploy(args.archive_path, args.ssh_key, args.username)
