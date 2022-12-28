class Plugin:
    def __init__(self, parent):
        self.parent = parent
        self.name = "plugin_loader"
        self.parent.add_plugin_menu(self.plugin_menus)

    def plugin_menus(self, dpg):
        # Add menu item to install new plugin
        dpg.add_menu_item(label="Install New Plugin")
#        dpg.add_menu_item(label="Modify Plugin Settings")
        # Add loaded plugins to menu
        with dpg.menu(label="Installed"):
            for plgn in self.parent.plugins.keys():
                if plgn not in self.parent.default_plugins:
                    with dpg.menu(label=plgn):
                        dpg.add_menu_item(label="Enable Plugin")
                        dpg.add_menu_item(label="Disable Plugin")
                        if hasattr(self.parent.plugins[plgn], 'plugin_menu_callback'):
                            dpg.add_menu_item(label=plgn, callback=self.parent.plugins[plgn].plugin_menu_callback)

    def install_plugin(self, sender):
        print("Installing plugin")
        pass

    def modify_plugin(self, sender):
        print("Modifying")
        pass