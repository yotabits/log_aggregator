from appJar import gui
from cStringIO import StringIO
import colors
import sys
import time
import thread
from opt_parser import manage_local, manage_conf_update, manage_show_conf


class Gui:
    def __init__(self):
        self.app = gui(handleArgs=False)
        self.create_progress_subwindow()
        self.configure_main_window()
        self.launch_threads()
        self.app.go()

    def button_manager_main(self, button):
        if (button == "Validate file"):
            path = self.app.getEntry("file_path")
            manage_conf_update(None, path)
        elif(button == "Show configuration"):
            manage_show_conf(None, no_check=True)
            self.app.infoBox("Take a look Closer", "Configuration file status displayed in console.")
        if (button == "Tar Me"):
            self.app.showSubWindow("sub1")
            manage_local(None, no_check=True)
            self.app.hideSubWindow("sub1")
            self.app.infoBox("success", "Success Fully created Tarball, Read console log for more details")

    def create_progress_subwindow(self):
        self.app.startSubWindow("sub1", title="Pleas Wait...", modal=False, transient=False,)
        self.app.addDualMeter("progress")
        thread.start_new_thread(self.loop_progress,())
        self.app.setGeometry(300, 100)
        self.app.stopSubWindow()

    def loop_progress(self):
        for i in range(0,100):
            self.app.setMeter("progress", [i, i])
            time.sleep(0.1)
        self.loop_progress()

    def launch_threads(self):
        thread.start_new_thread(self.loop_progress, ())

    def configure_main_window(self):
        self.app.addButtons(["Show configuration", "Tar Me"], self.button_manager_main)
        self.app.addFileEntry("file_path")
        self.app.addButton("Validate file", self.button_manager_main)

