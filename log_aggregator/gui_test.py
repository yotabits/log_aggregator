from appJar import gui
import os
import time
import thread
from threading import Thread
from opt_parser import manage_local, manage_conf_update, manage_show_conf
from free_space_checker import check_disk_available



class Gui:
    def __init__(self):
        self.app = gui(handleArgs=False)
        self.create_disk_subwindow()
        self.configure_main_window()
        self.create_progress_subwindow()
        self.enough_proceed_disk_space = None
        #self.p_bar_thread = Thread(target=self.loop_progress)
        #self.p_bar_thread.start()
        self.space_available = 0
        self.app.go()

    def button_manager_main(self, button):
        if button == "Validate file":
            path = self.app.getEntry("file_path")
            manage_conf_update(None, path)
        elif button == "Show configuration":
            manage_show_conf(None, no_check=True)
            self.app.infoBox("Take a look Closer", "Configuration file status displayed in console.")
        if button == "Tar Me":

            self.space_available, enough_space = check_disk_available(gb_availabe_min=1)
            if enough_space is False:
                self.enough_proceed_disk_space = None
                self.app.openSubWindow("disk sub")
                self.app.setLabel("disk_label", "Warning! Only " + str(self.space_available)
                                  + " GB of disk space available. Would you like to proceed ?")
                self.app.showSubWindow("disk sub")
                return

            self.make_tar_ball()

    def make_tar_ball(self):
        description_file_path = self.get_description()
        self.app.showSubWindow("sub1")
        manage_local(None, no_check=True, description_file=description_file_path, keep_raw=False)
        self.app.hideSubWindow("sub1")
        self.app.infoBox("success", "Success Fully created Tarball, Read console log for more details")
        self.app.clearTextArea("pb_describe")
        self.app.setTextArea("pb_describe", "Describe your problem")

    def save_on_low_disk_space(self, button):
        self.app.hideSubWindow("disk sub")
        if button == "Continue":
            self.make_tar_ball()
        else:
            print "Cancel"

    def create_progress_subwindow(self):
        self.app.startSubWindow("sub1", title="Please Wait...", modal=False, transient=True, blocking=False)
        self.app.addDualMeter("progress_meter")
        self.app.setSize(200, 300)
        self.app.stopSubWindow()

    def create_disk_subwindow(self):
        self.app.startSubWindow("disk sub", modal=True)
        self.app.addLabel("disk_label", "")
        self.app.addButtons(["Continue", "Cancel"], self.save_on_low_disk_space)
        self.app.stopSubWindow()

    def proceed_disk_space(self):
        print("toto")
        self.enough_proceed_disk_space = True
        self.app.hideSubWindow("disk_sub")

    def cancel_disk_space(self):
        print("titi")
        self.enough_proceed_disk_space = False
        self.app.hideSubWindow("disk_sub")

    def loop_progress(self):
        while self.app:
            for i in range(0, 100):
                self.app.setMeter("progress_meter", [i, i])
                time.sleep(0.3)

    def configure_main_window(self):
        self.app.addTextArea("pb_describe")
        self.app.setTextArea("pb_describe", "Describe your problem")
        self.app.addButtons(["Show configuration", "Tar Me"], self.button_manager_main)
        self.app.addFileEntry("file_path")
        self.app.addButton("Validate file", self.button_manager_main)

    def get_description(self):
        input = self.app.getTextArea("pb_describe")
        if(input != "Describe your problem"):#here we should save in file
            description_file_name = "bug describer"
            fp = open(description_file_name, "w")
            fp.write(input)
            fp.close()
            cwd = os.getcwd()
            file_path = cwd + "/" + description_file_name
            return file_path
        return None
