from os import setuid
from turtle import width
import dearpygui.dearpygui as dpg2

class Plugin:
    def __init__(self, parent):
        self.parent = parent
        self.name = "effects"
        self.effects = []
        self.parent.add_on_start(self.start)
    
    def effects_window(self, dpg):
        with dpg.window(label="Effects"):
            dpg.add_text("Effects")
            dpg.add_listbox(items=self.effects, callback=self.effects_callback)

    def effects_callback(self, sender, data):
        pass

    def start(self):
        self.effects_window(dpg2)

