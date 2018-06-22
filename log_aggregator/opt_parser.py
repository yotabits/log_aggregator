import argparse
import conf_loader
import tar_manager

def pars_args():
    parser = argparse.ArgumentParser(description="A simple, configurable software to tar a set of preconfigured log "
                                                 "files.", prog='log_aggregator', version='0.41')
    parser.add_argument("--show_conf", action="store_true", default=False, help="Show the actual configuration file in"
                                                                                " use if it exists")

    parser.add_argument("--default_conf", action="store_true", default=False, help="WARNING: Delete your actual conf if"
                                                                                   " it exists and generate the default"
                                                                                   " configuration file")
    parser.add_argument("--local", action="store_true", default=False, help="Create a local tarball under home directory")
    parser.add_argument("--gui", action="store_true", default=False, help="A gui to help you")
    parser.add_argument("--add_file", action="store_true", default=False, help="Add a file path in configuration file")
    parser.add_argument("--keep_raw", action="store_true", default=False, help="Allows to keep raw file stacks "
                                                                               "containing videos taken by 3d sensors.")
    return parser.parse_args()

def main():
    parsed_args = pars_args()
    manage_gui(parsed_args)
    manage_local(parsed_args, keep_raw=parsed_args.keep_raw)
    manage_show_conf(parsed_args)
    manage_default_conf(parsed_args)

def manage_gui(parsed_args):
    if(parsed_args.gui):
        import gui_test
        gui = gui_test.Gui()

def manage_conf_update(parsed_args, file_to_add=None):
    if(file_to_add is not None):
        conf_loader.add_entry_to_conf_file(file_to_add)
    elif(parsed_args.add_file):
       conf_loader.add_entry_to_conf_file(parsed_args.add_file)


def manage_local(parsed_args, no_check=False, description_file=None, keep_raw=False):
    run = no_check


    if(run == False and parsed_args.local):
        run = True

    if (run):
        file_list = conf_loader.check_create_load_conf(keep_raw=keep_raw)
        if description_file:
            file_list.append(description_file)
        tar_path, folder_to_tar_path = tar_manager.prepare_tar(file_list)
        tar_manager.clean_up(None, folder_to_tar_path)


def manage_show_conf(parsed_args, no_check=False):
    if (no_check or parsed_args.show_conf):
        if (conf_loader.check_conf_file_exist()):
            conf_loader.check_create_load_conf(skip_check=True, show_mode=True)


def manage_default_conf(parsed_args):
    if (parsed_args.default_conf):
        conf_loader.generate_default_conf()
