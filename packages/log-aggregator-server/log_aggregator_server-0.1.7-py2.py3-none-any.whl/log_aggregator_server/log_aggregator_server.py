# -*- coding: utf-8 -*-
from datetime import datetime
import os
import threading
import tarfile
import shutil

from .process import process_log
from .system import system_log
from .user_log import sys_log, ros_log


def log_aggregator():

    home_path = os.environ['HOME']

    working_folder = datetime.now().strftime("%Y%m%d%H%M%S")
    log_folder = os.path.join(home_path, working_folder)
    os.makedirs(log_folder)

    process_thread = threading.Thread(target=process_log, args=(log_folder, ))
    system_thread = threading.Thread(target=system_log, args=(log_folder, ))
    ros_log_thread = threading.Thread(target=sys_log, args=(log_folder, ))
    sys_log_thread = threading.Thread(target=ros_log, args=(log_folder, ))

    process_thread.start()
    system_thread.start()
    ros_log_thread.start()
    sys_log_thread.start()

    process_thread.join()
    system_thread.join()
    ros_log_thread.join()
    sys_log_thread.join()

    # tar_ball
    os.chdir(home_path)
    with tarfile.open(log_folder + '.tar.gz', "w:gz") as tar_handle:
        tar_handle.add(working_folder)

    tar_handle.close()

    # delete folder
    shutil.rmtree(log_folder)
