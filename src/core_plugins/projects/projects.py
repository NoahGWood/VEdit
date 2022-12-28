from gc import callbacks
from os import setuid
from turtle import width
import dearpygui.dearpygui as dpg2

from core_plugins.projects.base import Project
#from core_plugins.projects.filebase import FileBase

class Plugin:
    def __init__(self, parent):
        self.parent = parent
        self.project = None
        self.name = "projects"
        self.recent_projects = []
#        a = FileBase('Test','/home/noah/Desktop/music_symbol.jpeg', self.parent.timeline.drag_callback)
#        a = self.parent.Clip()
#        self.project_files = [a,a,a,a,a,a,a,a,a,a,a,a,a,a]
        self.project_files = []
        self.preferences_open = False

        self.add_project_file(0)

        self.parent.add_file_menu(self.file_menus)
        self.parent.add_edit_menu(self.edit_menus)
        self.parent.add_on_start(self.start)

    def prompt(self, reason):
        if reason == 'old_project':
            self.load_old_project()
        else:
            pass

    def add_project_file(self, sender):
        pass
#        self.project_files.append(self.parent.Clip(0, 'image', '/home/noah/Desktop/music_symbol.jpeg', drag_callback=self.parent.timeline.drag_callback))
#        self.project_files.append(self.parent.Clip(0, 'image', '/home/noah/Pictures/hmm.png', drag_callback=self.parent.timeline.drag_callback))
#        self.project_files.append(self.parent.Clip(0, 'image', '/home/noah/Pictures/idea2.png', drag_callback=self.parent.timeline.drag_callback))
        #self.make_table()

    def load_old_project(self):
        print("LOADING OLD")
        dpg2.configure_item("load_old_project", show=True)
        jobs = dpg2.get_callback_queue()
        dpg2.run_callbacks(jobs=jobs)

    def setup(self):
        with dpg2.window(menubar=False, show=False, no_close=True, no_collapse=True, no_title_bar=True) as p:
            with dpg2.file_dialog(directory_selector=False, show=False, callback=self.load_project, id="project_selector", width=800, height=400):
                dpg2.add_file_extension(".vedit", color=(0, 255, 0, 255), custom_text="[VEdit Project]")
                dpg2.add_file_extension(".*")

    def add_item(self, filename):
        """Adds item to project list"""
        pass

    def print_me(self, sender):
        print('derp')

    def preferences(self, sender):
        if not self.preferences_open:
            self.preferences_window(dpg2)

    def preferences_window(self, dpg):
        print("Opening window")
        self.preferences_open=True
        with dpg.window(label="Preferences"):
            dpg.add_text("Hello, world")
    
    def modal(self):
        with dpg2.window(tag="load_old_project", menubar=False, no_resize=True,
            no_title_bar=True, no_saved_settings=True, no_collapse=True,
            width=400, height=400, pos=(400,200), no_close=True, no_move=True, show=False):
            dpg2.add_text("Old Project Found, Load?")
            dpg2.add_button(label="Yes", callback=lambda: dpg2.delete_item("load_old_project") and self.project.load_old_project)
            dpg2.add_button(label="No", callback=lambda: dpg2.delete_item("load_old_project") and self.project.rm_old_project)

    def project_window(self, dpg):
        with dpg.window(label="Project") as w:
            dpg.add_text("Project Files")
            self.make_table()
        self.modal()
        self.project = Project(self.prompt)
        self.project.setup()

    def make_table(self):
        w=100*2
        max_width = dpg2.get_viewport_width()
        step = int(max_width / w)
        with dpg2.table(height=-2, width=-2, header_row=False, tag='file_chart', policy=dpg2.mvTable_SizingStretchProp,
                   borders_outerH=True, borders_innerV=True, borders_outerV=True) as t:
            for i in range(step):
                dpg2.add_table_column(tag="file_column_{}".format(i))
            table_files = [self.project_files[i:i+step] for i in range(0,len(self.project_files),step)]
            for row in table_files:
                print(row)
                with dpg2.table_row() as r:
                    for each in row:
                        with dpg2.table_cell() as g:
                            each.parent = g
                            each.setup_mpy_clip()

    def lb_callback(self, sender):
        print("List box pressed")
        print(sender)

    def start(self):
        self.setup()
        self.project_window(dpg2)

    def open_project(self,sender):
        dpg2.show_item("project_selector")

    def load_project(self, sender, filename):
        print("Loading {}".format(filename))
        self.project.load_project(filename['file_path_name'])

    def file_menus(self, dpg):
        dpg.add_menu_item(label="Add Item", callback=self.add_project_file)
        dpg.add_menu_item(label="New Project", callback=self.print_me)
        dpg.add_menu_item(label="Open Project", callback=self.open_project)
        dpg.add_menu_item(label="Save Project", callback=self.print_me)
        dpg.add_menu_item(label="Save Project As...", callback=self.print_me)
        dpg.add_separator()
        dpg.add_menu_item(label="Quit", callback=self.end)
    
    def end(self, sender):
        exit(1)

    def edit_menus(self, dpg):
        dpg.add_menu_item(label="Preferences", callback=self.preferences)
