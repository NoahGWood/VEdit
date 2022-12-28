from os import setuid
from turtle import width
import dearpygui.dearpygui as dpg2

class Plugin:
    def __init__(self, parent):
        self.parent = parent
        self.name = "transitions"
        self.transitions = []
        self._transitions = []
        self.parent.add_new_transition = self.add_new_transition
        self.parent.add_on_start(self.start)

    def add_new_transition(self, name, preview_img, func):
        self._transitions.append({'name':name, 'img':preview_img, 'f':func})

    def transitions_window(self, dpg):
        with dpg.window(label="Transitions"):
            dpg.add_text("Project Files")

            dpg.add_listbox(items=self.transitions, callback=self.transition_callback)

    def transition_callback(self, sender, data):
        pass

    def start(self):
        self.transitions_window(dpg2)