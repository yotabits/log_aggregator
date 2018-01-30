import colors
from gopher_robot_version import sys_packages
from gopher_robot_version import ros_packages
from gopher_robot_version import writer
import os

def prepare_string():
    result = ""
    error_msg = " packages directory NOT FOUND, and won't be part of gopher_version_file"
    success_msg =" packages version"+ colors.bcolors.OKGREEN + " successfully" + colors.bcolors.ENDC + \
                 " added to gopher_version_file"

    devel_path = "/opt/yujin/amd64/indigo-devel"
    stable_path = "/opt/yujin/amd64/indigo-stable"
    base_path = "/opt/ros"

    system_dict = sys_packages.get_system_packages()
    print( "System" + success_msg)


    try:
        ros_dict_devel = ros_packages.get_ros_packages(devel_path)
        print (devel_path + success_msg)
    except OSError:
        print(colors.bcolors.FAIL + "-------->  " + colors.bcolors.ENDC
              + devel_path + error_msg)
        ros_dict_devel = {}

    try:
        ros_dict_stable = ros_packages.get_ros_packages(stable_path)
        print(stable_path + success_msg)
    except OSError:
        print(colors.bcolors.FAIL + "-------->  " + colors.bcolors.ENDC
              + stable_path + error_msg)
        ros_dict_stable = {}

    try:
        ros_dict_base = ros_packages.get_ros_packages(base_path)
        print(base_path + success_msg)
    except OSError:
        print(colors.bcolors.FAIL + "-------->  " + colors.bcolors.ENDC
              + base_path + error_msg)
        ros_dict_base = {}


    result += writer.dict_to_str(system_dict, "SYSTEM PACAKGES")
    result += writer.dict_to_str(ros_dict_devel, "YUJIN_DEVEL")
    result += writer.dict_to_str(ros_dict_stable, "YUJIN STABLE")
    result += writer.dict_to_str(ros_dict_base, "ROS INTERNAL")

    return result

def write_to_file():
    filename = "gopher_version_file"
    fp = open(filename, "w+")
    data = prepare_string()
    fp.write(data)
    fp.close()
    cwd = os.getcwd()
    file_path = cwd + "/" + filename
    return file_path
