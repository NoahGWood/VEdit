import dearpygui.dearpygui as dpg
def save_init():
    dpg.save_init_file("imgui.ini")


class Plugin:
    def __init__(self, parent):
        self.parent = parent
        self.name = 'gui'
        self.run_on_start = []
        self.file_menus = []
        self.edit_menus = []
        self.plugin_menus = []
        self.custom_menus = []
        self.open_windows = []
        self.parent.root_window = 0
        self.parent.open_window = self.open_window
        self.parent.close_window = self.close_window
        self.parent.add_file_menu = self.add_file_menu
        self.parent.add_edit_menu = self.add_edit_menu
        self.parent.add_plugin_menu = self.add_plugin_menu
        self.parent.add_custom_menu = self.add_custom_menu
        self.parent.add_on_start = self.add_on_start


    def add_on_start(self, func):
        """Adds a function to be run on start"""
        self.run_on_start.append(func)

    def close_window(self, func):
        """Removes a window"""
        self.open_windows.remove(func)

    def open_window(self, func):
        """Adds a window to end of function"""
        self.open_windows.append(func)
        print("Added new window!")

    def add_file_menu(self, func):
        """Adds a menu to file menu"""
        self.file_menus.append(func)

    def add_edit_menu(self, func):
        """Adds a menu to edit menu"""
        self.edit_menus.append(func)

    def add_plugin_menu(self, func):
        """Adds plugin to plugin menu"""
        self.plugin_menus.append(func)

    def add_custom_menu(self, func):
        self.custom_menus.append(func)

    def print_me(self, sender=None):
        print("Menu Item: {}".format(sender))

    def main(self):
        dpg.create_context()
        dpg.configure_app(init_file="imgui.ini")
        dpg.enable_docking()
        dpg.create_viewport(title="VEdit")
        dpg.setup_dearpygui()
        with dpg.viewport_menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Save", callback=self.print_me)
                dpg.add_menu_item(label="Save As", callback=self.print_me)
                for func in self.file_menus:
                    if func:
                        func(dpg)
            with dpg.menu(label="Edit"):
                for func in self.edit_menus:
                    if func:
                        func(dpg)
            with dpg.menu(label="Plugins"):
                for func in self.plugin_menus:
                    if func:
                        func(dpg)
            for func in self.custom_menus:
                if func:
                    func(dpg)
        with dpg.window(tag="Primary Window"):
            pass
        for func in self.run_on_start:
            if func:
                func()
        dpg.show_viewport()
        dpg.set_primary_window("Primary Window", True)
        self.parent.root_window = dpg.get_active_window()
        while dpg.is_dearpygui_running():
            for func in self.open_windows:
                if func:
                    func(dpg)
            self.parent.update()
            dpg.render_dearpygui_frame()
        dpg.destroy_context()
#        dpg.start_dearpygui()
