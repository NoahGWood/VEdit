from gc import callbacks
import numpy as np
import dearpygui.dearpygui as dpg2
from core_plugins.player.editor import *
from threading import Thread

class Plugin:
    def __init__(self, parent):
        self.parent = parent
        self.parent.player = self
        self.name = "player"
        self.fname = "core_plugins/player/intro.mp4"
        self.video_open = False
        self.is_playing = False
        self.is_setup = False
        self.pause = False
        self.playbtn_label = "Play"
        self.last_time = 0
        self._max_time = 100
        self._load_clip()
        self._slider = None
        self.parent.add_custom_menu(self.view_menu)
        self.parent.add_on_start(self.start)
        self.parent.change_clip = self.change_clip
        self.parent.set_player_time = self.set_time
        self.parent.get_player_time = self.get_time

    def change_clip(self, filename=None, clip=None):
        if clip:
            self.clip = clip
            self.sub_clip = self.clip
        elif filename:
            self.fname = filename
            self._load_clip()
            # Stop if we are playing
            self.pause = True
            # Set the frame to frame 0
            self.set_frame()

    def _load_clip(self):
        self.clip = VideoFileClip(self.fname)
        self.sub_clip = self.clip

    def _resize_clip_player(self):
        self.clip = self.clip.resize((600,400))
        self.sub_clip = self.clip

    def start(self):
        self.video_player('root')

    def set_frame(self, frame=-1):
        self._resize_clip_player()
        self.clip.show(frame)
        self._set_last_time(frame)

    def set_time(self, time):
        self.time = time

    def get_time(self):
        return self.last_time

    def video_player(self, sender):
        if not self.is_setup:
            base = np.ndarray(shape=(400*2,400*2))
            with dpg2.texture_registry(show=False):
                dpg2.add_raw_texture(600, 400, base, tag="video_tag", format=dpg2.mvFormat_Float_rgb)
                self.set_frame()
            self.is_setup = True

        print("CALLED")
        if dpg2.does_item_exist('video_slider'):
            dpg2.delete_item('video_slider')
        if dpg2.does_item_exist('video_btns'):
            dpg2.delete_item('video_btns')
        with dpg2.window(label="Video Window", width=600):
            dpg2.add_image_button(texture_tag="video_tag", height=400, width=600, callback=self.video_play)
            self._slider = dpg2.add_slider_float(tag="video_slider", callback=self._slider_changed, width=600, default_value=0, max_value=5184000)
            # Add buttons
            with dpg2.group(tag="video_btns", horizontal=True, width=120):
                self.rev_btn = dpg2.add_button(label="<<<", callback=self.rewind)
                self.revbtn = dpg2.add_button(label="<", callback=self.rewind)
                self.playbtn = dpg2.add_button(label=self.playbtn_label, callback=self.video_play)
                self.fwbtn = dpg2.add_button(label=">", callback=self.fforward)
                self.ff_btn = dpg2.add_button(label=">>>", callback=self.fforward)

        self.parent.register_update(self.window_updates)
        self.parent._player_registered = True

    def rewind(self, sender):
        pass

    def fforward(self, sender):
        pass

    def _slider_changed(self):
        # Pause
        self.pause=True
        # Load frame
        frame = dpg2.get_value("video_slider")
        self.last_time = frame
        self.video_play('')

    def set_video_time(self, t):
        """Sets the video time to t seconds"""
        self.last_time = t
        self.video_play('')

    def window_updates(self):
        
        if self._slider:           
            if not self.pause:
                self.playbtn_label = "Play"
                if self.last_time>0:
                    dpg2.configure_item(self._slider, max_value=self._max_time)
                    dpg2.configure_item("timeline_slider", max_value=self._max_time)
                    if self.last_time >=self._max_time:
                        print(self._max_time)
                    dpg2.set_value("video_slider", self.last_time)
                    dpg2.set_value("timeline_slider", self.last_time)
                else:
                    dpg2.set_value("video_slider", 0)
                    dpg2.set_value("timeline_slider", 0)
            else:
                self.playbtn_label = "Pause"

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
