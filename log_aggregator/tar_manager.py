import colors
import distutils
from distutils.dir_util import copy_tree
import os
from os.path import expanduser
import pycurl



from shutil import copyfile, rmtree
import socket
import tarfile
import time

def prepare_file_list(found_file_list):
    """
    Some path are relative, we make them absolute
    :param found_file_list: list of paths
    :return: The input list with only absolute paths
    """
    real_path = []
    for element in found_file_list:
        real_path.append(expanduser(element))
    print real_path

    return real_path


def generate_filename():
    """
    Generate the name of the tar file
    :return: the name string
    """
    name = time.strftime("%y.%m.%d_%H.%M.%S")
    name += "_" + socket.gethostname()
    return name

def gen_cpu_usage():
    os.system("top -n4 -b -c > " + "~/cpu_usage")

def prepare_tar(file_list):
    """

    :param file_list:
    :return:
    """
    gen_cpu_usage()
    file_list.append(expanduser("~/cpu_usage"))
    name = generate_filename()
    folder_to_tar_path = expanduser("~/") + name + "/" #folder to be tared
    os.makedirs(folder_to_tar_path)

    for file_path in file_list:
        try:
            real_path = expanduser(file_path)
            folder_name = real_path.split("/")[-1]
            copy_tree(real_path, folder_to_tar_path + folder_name)
        except distutils.errors.DistutilsFileError:
            filename = (real_path.split("/"))[-1]
            copyfile(real_path, folder_to_tar_path + "/" + filename)

    tar_name = tar_folder(folder_to_tar_path, name)
    print (colors.bcolors.OKGREEN + "Tar-ball successfully created under: "+ colors.bcolors.ENDC + tar_name)
    return tar_name, folder_to_tar_path

def clean_up(tar, folder):
    """
    Delete the tar ball and the folder used to make it.

    :param tar: Path to the tarball file, set to none if we do not want to remove it
    :param folder:
    :return:
    """
    print(colors.bcolors.OKBLUE + "Starting clean up..." + colors.bcolors.ENDC)
    print(colors.bcolors.OKBLUE + "The following files will be deleted from local system:" + colors.bcolors.ENDC)
    if (tar):
        print(colors.bcolors.FAIL + "-------->  " + colors.bcolors.ENDC + tar)
    if (folder):
        print(colors.bcolors.FAIL + "-------->  " + colors.bcolors.ENDC + folder)

    if (tar):
        os.remove(tar)
    if (folder):
        rmtree(folder)
    print(colors.bcolors.OKGREEN + "Files successfully deleted from local system..." + colors.bcolors.ENDC )


def tar_folder(folder_path, name):
    """
    Take an folder and make a tarball of it
    :param folder_path: Path to the folder to tar
    :param name: name of the output tar file desired
    :return: The tarball path
    """
    tar_name = name + ".tar.bz2"
    tar_name = expanduser("~/" + tar_name)
    with tarfile.open(tar_name, "w:bz2") as tar:
        tar.add(folder_path, arcname=os.path.basename(folder_path))
    return tar_name