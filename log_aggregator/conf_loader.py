import colors
from os.path import expanduser
import os
from specific_entries_manager import manage_entries

def check_file_existence(files_list):
    """
    The existence or not of files or DIRECTORIES paths in file list
    when an invalid path is found it's automatically remove from the list.
    :param files_list: List of paths to check for existence.
    :return: Return the input list with incorrect paths removed as first return value. As a second value return
    the list of incorrect paths
    """
    not_exist_list = []
    for file in files_list:
        tmp_file = expanduser(file)
        if not os.path.exists(tmp_file):
            if not os.path.isfile(tmp_file):
                not_exist_list.append(file)

    for file in not_exist_list:
        files_list.remove(file)

    return files_list, not_exist_list


def check_create_load_conf(skip_check=False, show_mode=False, keep_raw=False):
    """
    Firstly check if the configuration file ~/.log_to_nurc exist, create it if not, read the files to tar
    from this configuration file and check their existence.
    :param skip_check: configuration file existence checking is skipped if this is set to true
    :return: Return the file list read from log_to_nucrc files/path, ensure that each of these path exists
    """
    conf_file_found = True
    conf_file_path = get_default_conf_path()

    if (skip_check == False):
        conf_file_found = check_conf_file_exist(conf_file_path)

    files_list = []
    if(conf_file_found):
        conf_file_fp = open(conf_file_path)
        line = conf_file_fp.readline()
        while line:
            line = line.replace('\n', '')
            entry_files = manage_entries(line, show_mode=show_mode, keep_raw=keep_raw)
            for file in entry_files:
                files_list.append(file)
            line = conf_file_fp.readline()
    else:
        generate_default_conf(conf_file_path)
        print(colors.bcolors.OKGREEN + "Configuration file successfully created..." + colors.bcolors.ENDC)
        return check_create_load_conf()

    files_list, not_exist_list = check_file_existence(files_list)

    if(show_mode and "gopher_version_file" in not_exist_list):
        not_exist_list.remove("gopher_version_file")
        files_list.append("gopher_version_file")

    file_sent_displayer(files_list, not_exist_list)
    return files_list


def file_sent_displayer(files_list, not_exist_list):
    """
    Simply pretty print the files/folder that will be successfully sent and the one that does not exists.

    :param files_list: List of files/folders to be tared and sent.
    :param not_exist_list: List of files/folders found in configuration file that does not exists.
    """
    print(colors.bcolors.OKGREEN + "The following files will be tared:" + colors.bcolors.ENDC)
    for file in files_list:
        print (colors.bcolors.OKGREEN + "-------->  " + colors.bcolors.ENDC +  file)
    if len(not_exist_list) != 0:
        print colors.bcolors.FAIL + "The following file(s) won't be tared as they DO NOT exist under the curent file system:" + colors.bcolors.ENDC
        for file in not_exist_list:
            print (colors.bcolors.FAIL + "-------->  "+ colors.bcolors.ENDC + file)
        print colors.bcolors.FAIL + "Hint: To prevent this message from appearing again correct the previously listed " \
                                    "entries under ~/.log_to_nucrc configuration file." + colors.bcolors.ENDC


def check_conf_file_exist(conf_file_path=None):
    """
    Check if the ~/.log_to_nucrc file exist
    :param conf_file_path: custom configuration path
    :return: True or False
    """
    if (conf_file_path is None):
        conf_file_path = get_default_conf_path()

    if (os.path.isfile(conf_file_path)):
        print(colors.bcolors.OKGREEN + "Configuration file found..." + colors.bcolors.ENDC)
        return True
    else:
        print(colors.bcolors.WARNING + "Configuration file not found..." + colors.bcolors.ENDC)
        return False


def generate_default_conf(conf_file_path=None):
    """
    Create the default configuration file.
    :param conf_file_path: custom path for configuration file
    :return: return the list of files to avoid to read it again.
    """
    if (conf_file_path is None):
        conf_file_path = get_default_conf_path()

    default_file_list = ["latest_log", "~/.gopher_robot_environment.bash", "/var/log/syslog",
                         "gopher_version", "~/.ros/log/console_output.log", "/proc/version"]
    conf_file_fp = open(conf_file_path, "w")
    for element in default_file_list:
        conf_file_fp.write(element + "\n")
    conf_file_fp.close()
    print (colors.bcolors.OKGREEN + "Default configuration file successfully generated ~/.log_to_nucrc"
           + colors.bcolors.ENDC)
    return


def get_default_conf_path():
    """
    Return the absolute path of the configuration file
    :return: configuration file path
    """
    conf_file_name = '.log_to_nucrc'
    conf_file_path = expanduser("~/" + conf_file_name)
    return conf_file_path


def add_entry_to_conf_file(entry_to_add, conf_file_path=None):
    """
    Add an entry to the configuration file
    :param entry_to_add:  absolute or relative path of the file or directory to be added to the configuration file
    :param conf_file_path:
    :return:
    """
    wrote = False

    if (entry_to_add == "" or entry_to_add == None):
        print(colors.bcolors.WARNING + "File path not Provided !" + colors.bcolors.ENDC)
        return wrote

    if (not check_conf_file_exist()):
        generate_default_conf()
    if conf_file_path is None:
        conf_file_path = get_default_conf_path()

    conf_file_fp = open(conf_file_path, "r+")
    read = conf_file_fp.readline()

    found_list = []
    while read:
        found_list.append(read)
        read = conf_file_fp.readline()

    if entry_to_add not in found_list:
        conf_file_fp.writelines(entry_to_add)
        wrote = True
        print(colors.bcolors.OKGREEN + "File path Succesfully append to configuration file..." + colors.bcolors.ENDC)
    else:
        print(colors.bcolors.FAIL + "File path already exist in actuall configuration file.")
    conf_file_fp.close()
    return wrote