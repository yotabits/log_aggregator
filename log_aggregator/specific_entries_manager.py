import colors
import os
from os.path import expanduser, isdir
from os import listdir
import re
import gopher_version_manager
from image_sequence_unwarper import convert_video_to_image



def manage_entries(entry, show_mode=False, keep_raw=False):
    """
    Some entries in the configuration file are not path but keywords, this function translate those keywords to
    path,
    :param entry: Value from the configuration file
           show_mode:In case we are just showing the configuration file content this let us know that no operation
           should be done
    :return: A list of paths "calculated" from entries found in the configuration file .log_to_nurc file
    """
    file_list = []
    robot_env_patten = re.compile('.*/.gopher_robot_environment.bash$')
    if (entry == 'latest_log'):
        file_list.append(manage_ros_log(show_mode, keep_raw=keep_raw))
        return file_list
    elif (robot_env_patten.match(entry)):
        return get_semantics_from_robot_env(entry)
    elif (entry == 'gopher_version'):
        return gen_version_file(show_mode)

    file_list.append(entry)
    return file_list


def gen_version_file(show_mode):
    if (show_mode):
        return ["gopher_version_file"]
    else:
        return [gopher_version_manager.write_to_file()]

def manage_ros_log(show_mode=False, keep_raw=False):
    """
    As .ros/log/latest symlink is broken we manually search the path to the last ros log.

    :return: The path of the latest log folder.
    """
    log_folder_path = expanduser("~/.ros/log")
    try:
        log_folder_content = listdir(log_folder_path)
    except OSError:
        print (colors.bcolors.FAIL + "Ros log folder %s does not exist..." % (log_folder_path) + colors.bcolors.ENDC)
        exit(1)
    log_folder_list = [] #list of folders under ~/.ros/log
    for element in log_folder_content:
        actual_folder_path = log_folder_path + "/" + element
        if (isdir(actual_folder_path)):
            log_folder_list.append((actual_folder_path,element))

    #remove folder not matching the xxxx-xx-xx pattern
    exact_log_folder_list = []
    pattern = re.compile("[0-9]{4}-{1}[0-9]{2}-{1}[0-9]{2}")
    for element in log_folder_list:
        if pattern.match(element[1]):
            exact_log_folder_list.append(element)
    log_folder_list = exact_log_folder_list

    sorted_log_folder_list = sorted(log_folder_list, key=lambda tup: tup[1])

    latest = None
    try :
        latest = ((sorted_log_folder_list[-1])[0])
    except IndexError:
        print (colors.bcolors.FAIL + "No log folder has been found une ~/.ros/log" + colors.bcolors.ENDC)

    latest_log_path = latest + "/latest"
    if not show_mode:
        print ( colors.bcolors.OKBLUE + "Pre processing ROS log folder..." + colors.bcolors.ENDC)
        convert_video_to_image(latest_log_path, keep_raw)
        print ( colors.bcolors.OKBLUE + "Finish pre processing ROS log folder..." + colors.bcolors.ENDC)
    return latest_log_path

def get_semantics_from_robot_env(robot_env_file_path):
    """
    Grab from the robot configuration file the semantic file path.
    :return: The semantic_file_paht if it's found.
    """
    to_ret = []
    to_ret.append(robot_env_file_path)
    robot_env_file_path = expanduser(robot_env_file_path)

    if os.path.isfile(robot_env_file_path):
        robot_env_fp = open(robot_env_file_path)

        line = robot_env_fp.readline()
        pattern = re.compile("export GOPHER_SEMANTICS=[^=]+")

        while line:
            line_list = line.split('#')
            line = line_list[0] # we grab here everything before the fisrt comment
            if line and pattern.match(line):
                line = (line.split("="))[1] #We get what is on the right side of the equal, Now line is the path
                line = line.strip()
                line = expanduser(line)     #of the semantic file... we should still check existence OFC
                if os.path.isfile(line):
                    to_ret.append(line)
                    return to_ret  #path to semantics
                else:
                    print (colors.bcolors.WARNING + "Path provided in .gopher_robot_environement.bash (%s) is not a "
                                                    "valid absolute or relative path. Semantic file won't be tared"
                                                    % (line) + colors.bcolors.ENDC)

            line = robot_env_fp.readline()
        robot_env_fp.close()

    return to_ret