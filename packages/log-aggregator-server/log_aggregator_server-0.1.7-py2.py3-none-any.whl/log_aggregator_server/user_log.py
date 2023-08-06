import os
import shutil


def sys_log(path):
    try:
        file_path = path + '/syslog'
        shutil.copy('/var/log/syslog', file_path)
    except FileNotFoundError:
        print('No syslog found. Skip syslog aggregation.')


def ros_log(path):
    try:
        ros_path = os.environ['HOME']
        folder_path = path + '/latest'
        shutil.copytree(ros_path + '/.ros/log/latest', folder_path, symlinks=True)
    except FileNotFoundError:
        print('No ros log found. Skip ros log aggregation.')
