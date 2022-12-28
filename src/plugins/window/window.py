from cProfile import label
from fileinput import filename


class Plugin:
    def __init__(self, parent):
        self.parent=parent
        self.name = 'window'
        print("Window installed")
        self.parent.add_custom_menu(self.clip_menu)

    def plugin_menu_callback(self, sender):
        print("CALLED PLUGIN!")

    def load_clip(self, sender):
        print(sender)
        import os
        local = os.path.join(os.path.join(os.getcwd(), 'plugins'), 'window')
        print(local)
        if 39 == sender:
            self.parent.change_clip(filename=os.path.join(local, "exponents.mp4"))
        elif 40 == sender:
            self.parent.change_clip(filename=os.path.join(local, "circles.mp4"))
        elif 41 == sender:
            self.parent.change_clip(filename=os.path.join(local, "webapp.mp4"))
    def clip_menu(self, dpg):
        with dpg.menu(label="Clips"):
            dpg.add_menu_item(label="Exponents", callback=self.load_clip)
            dpg.add_menu_item(label="Circles", callback=self.load_clip)
            dpg.add_menu_item(label="Web App", callback=self.load_clip)
