import numpy as np
import dearpygui.dearpygui as dpg2
from core_plugins.player.editor import *
from  core_plugins.player._player import Player
from threading import Thread

class Plugin:
    def __init__(self, parent):
        self.name='player'
        self.parent = parent
        if self.parent.player == None:
            self.parent.player = Player(self.parent, self)
        else:
            self.parent.player.register_video_player(self)
        self.parent._player_registered = None
        self.parent.set_player_time = self.set_time
        self.parent.get_player_time = self.get_time

        self.parent.add_custom_menu(self.view_menu)
        self.parent.add_on_start(self.start)

    def change_clip(self, filename=None, clip=None):
        self.parent.player.change_clip(filename, clip)
        
    def start(self):
        self.video_player('root')

    def set_time(self, time):
        self.time = time

    def get_time(self):
        return self.last_time

    def video_player(self, sender):
        with dpg2.window(label="Video Window"):
            dpg2.add_image_button(texture_tag="video_tag", height=self.parent.player.player_size[0],
                width=self.parent.player.player_size[1], callback=self.parent.player.start_playback)
            self.playbtn = dpg2.add_button(label=self.parent.player.playbtn_label, callback=self.parent.player.start_playback)
            self._slider = dpg2.add_slider_float(tag="video_slider", callback=self.parent.player.slider_changed, width=600, default_value=0, max_value=1)

    def video_play(self, sender):
        self._max_time=self.clip.duration
        if self.last_time >= self._max_time:
            print("GREATER THAN")
            self.last_time=0
        if not self.is_playing:
            self.pause = False
            thread = Thread(target=self._play_clip, args=[self.last_time])
            thread.start()
            print(thread)
            self.is_playing = True
        else:
            self.pause = True
            print(self.last_time)

    def _set_last_time(self, time):
        print(self.last_time, self.clip.duration)
        if self.last_time >= self.clip.duration or time < 0:
            self.last_time = 0
        else:
           self.last_time += time

    def _play_clip(self, start=0, end=-1):
        self._resize_clip_player()
        if end == -1:
            end = self.clip.duration
        self.sub_clip = self.clip.subclip(start, end)
        self.sub_clip.preview(ret_val=self._set_last_time, pause_hook=self.video_pause)
        self.is_playing=False

    def video_pause(self):
        return self.pause

    def view_menu(self, dpg):
        with dpg.menu(label="View"):
            dpg.add_menu_item(label="Video Player", callback=self.video_player)
