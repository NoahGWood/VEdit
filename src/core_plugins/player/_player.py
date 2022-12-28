"""The player manager class

This class manages instances of player.py windows
"""
import numpy as np
import dearpygui.dearpygui as dpg
from core_plugins.player.editor import *
from threading import Thread


class Player:
    def __init__(self, core, player=None):
        self.core = core
        self.player_size=(600,400)
        self.players = []
        self.player = player
        self.fname = "core_plugins/player/intro.mp4"
        self.main_clip = None
        self.video_open = False
        self.clip_loaded = False
        self.is_playing = False
        self.is_setup = False
        self.pause = False
        self.playbtn_label = "Play"
        self.last_time = 0
        self._max_time = 100
        self._slider = None
        self.core.add_on_start(self.setup)
        self.core.change_clip = self.change_clip


    def register_video_player(self, player):
        number = len(self.players)
        self.players.append(player)
        return number

    def _load_clip(self):
        self.clip = VideoFileClip(self.fname)
        self._resize_clip_for_player()
        self.sub_clip = self.clip

    def _resize_clip_for_player(self):
        self.clip = self.clip.resize(self.player_size)

    def _is_paused(self):
        return self.pause

    def _set_last_time(self, t):
        if self.last_time >= self.clip.duration or t < 0:
            self.last_time = 0
        else:
            self.last_time += t
            
    def _play_clip(self, start=0, end=-1):
        if end == -1:
            end = self.clip.duration
        self.sub_clip = self.clip.subclip(start, end)
        self.sub_clip.preview(ret_val=self._set_last_time, pause_hook=self._is_paused)
        self.is_playing = False

    def set_frame(self, frame=-1):
        #self._resize_clip_for_player()
        self.clip.show(frame)
        self._set_last_time(frame)

    def setup(self, sender=None):
        if not self.is_setup:
            self._load_clip()
            base = np.ndarray(shape=(400*2, 400*2))
            print("Setting up")
            with dpg.texture_registry(show=False):
                dpg.add_raw_texture(600, 400, base,
                    tag="video_tag", format=dpg.mvFormat_Float_rgb
                )
                self.set_frame()
            self.is_setup = True
        print("Video player set up")
        self.core.register_update(self.player_updates,-1)

    def pause_playback(self):
        self.pause = True

    def start_playback(self):
        self._max_time = self.clip.duration
        if self.last_time >= self._max_time:
            self.last_time=0
            self.pause_playback()
        if not self.is_playing:
            self.pause = False
            thread = Thread(target=self._play_clip, args=[self.last_time])
            thread.start()
            self.is_playing = True
        else:
            # We're playing, so someone is probably trying to pause
            self.pause_playback()

    def player_updates(self):
        if not self.pause:
            dpg.configure_item(self.player._slider, max_value=self._max_time)
            dpg.set_value("video_slider", self.last_time)
            self.play_label = "|>"
        else:
            self.play_label = "||"
            dpg.set_value("video_slider", 0)

    def change_clip(self, filename=None, clip=None):
        if clip:
            self.clip = clip
            self.sub_clip = self.clip
        elif filename:
            self.fname=filename
            self._load_clip()
            # Stop if we are playing
            self.pause = True
            # Set time to 0
            self.set_time()
        pass

    def set_time(self, t=0):
        self.last_time = t

    def slider_changed(self):
        self.pause=True
        time = dpg.get_value("video_slider")
        self.last_time = time
        self.start_playback()
