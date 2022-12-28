import dearpygui.dearpygui as dpg
import numpy as np

import core_plugins.player.editor as mpy

class Plugin:
    def __init__(self, parent):
        self.parent = parent
        self.name = "clips"
        self.parent.Clip = Clip
        self.parent.stage_card_to_payload = self.stage_card_to_payload
#        self.parent.add_card_from_stage = self.add_card_from_stage

    def stage_card_to_payload(self, sender, data, user, delete_old=True):
        card = sender
        payload = dpg.get_item_children(card, slot=3)[0]
        old_card_window = dpg.get_item_parent(card)
        delete_old = delete_old
   
    def move_card_to_item(self, sender, item, user, delete_old):
        """Moves a card to item."""
        drop_target_item = sender+1
        card = item
        old_card_window = dpg.get_item_parent(item)
        print(drop_target_item)
        print(dpg.get_item_type(drop_target_item))
        new_card_container = dpg.add_child_window(parent=drop_target_item, height=dpg2.get_item_height(old_card_window), width=dpg2.get_item_width(old_card_window))
        dpg.move_item(card, parent=new_card_container)
        if delete_old:
            dpg.delete_item(old_card_window)

    def clone_card_to_item(self, sender, data, user):
        """Clones a card to item."""
        card = sender
        payload = dpg.get_item_children(card, slot=3)[0]
        pass

    def clone_and_copy_card_to_item(self, sender, data, user):
        """Clones a card and moves it to item"""
        pass

class Clip:
    def __init__(self, parent, type, file=None, text="Edit Text...", font="Amiri-Bold", mask=False, drag_callback=None):
        self.parent = parent
        self.type = type
        self.file = file
        self.text = text
        self.font = font
        self.width = 100
        self.height = 80
        self.duration = 300 # Default length = 3 seconds
        self.size = (self.width, self.height)
        self.fill = (0,0,0)
        self.position = (0,0)
        self.padding = (8,10)
        self.rounding = 20
        self.tag=None
        self.tag2=None
        self.texture = None
        self.lock_height = True # Only allows resizing the width
        self.drag_callback = drag_callback
        # Set the default scale to 100 pixels/second
        self.scale = 0.01 # pixels / second on the horizontal axis

        self.clip = None # Will be populated with a MoviePy clip
        self.mask = mask # Whether the clip is a mask (ignored for audio and text clips)
        #self.setup_mpy_clip()
        
    def update_scale(self, pixels_per_second):
        self.scale = 1 / pixels_per_second
    
    def setup_mpy_clip(self, custom_setup_function=None):

        self.tag = dpg.generate_uuid()
        self.tag2 = dpg.generate_uuid()
        self.texture = dpg.generate_uuid()

        if self.type == 'audio':
            self.load_audio()
        elif self.type == 'image':
            self.load_image()
        elif self.type == 'video':
            self.load_video_file()
        elif self.type == 'text':
            self.load_text()
        elif self.type == 'custom' and custom_setup_function != None:
            custom_setup_function()

    def load_audio(self):
        self.clip = mpy.AudioFileClip(self.file)

    def load_video_file(self):
        self.clip = mpy.VideoFileClip(self.file, ismask=self.mask)

    def load_text(self):
        self.clip = mpy.TextClip(self.text, font=self.font)

    def load_image(self):
        self.clip = mpy.ImageClip(self.file, ismask=self.mask)
        w, h, channels, data = dpg.load_image(self.file)
#        with dpg.texture_registry(show=False):
#            dpg.add_static_texture(self.width, self.height, data, tag=self.texture)
        with dpg.child_window(parent=self.parent, height=self.height, width=self.width, no_scrollbar=True):
            with dpg.texture_registry(show=False):
                dpg.add_static_texture(self.width, self.height, data, tag=self.texture)
            
            with dpg.group(drag_callback=self.callback) as card:
                dpg.add_image(self.texture)
                with dpg.drag_payload(parent=card, payload_type="CARD", drag_data=card, drop_data="drop data"):
                    dpg.add_image(self.texture)
    
    def callback(self, sender, user, data):
        self.drag_callback(self)

    def compute_duration(self):
        start_time_in_seconds = self.scale * self.position[0]
        duration_in_seconds = start_time_in_seconds + self.scale * self.size[0]
        self.duration = duration_in_seconds
        self.clip.set_duration(self.duration)

    def set_position(self, position):
        print(position)
        x, y = position
        self.position = (x, self.position[1])

    def delete_clip(self):
        if dpg.does_item_exist(self.tag):
            dpg.delete_item(self.tag)
        if dpg.does_item_exist(self.tag2):
            dpg.delete_item(self.tag2)

    def draw_clip(self):
        try:
            # Delete if already exists
            self.delete_clip()
            # Draw border
            # start at the start position
            print(self.position, self.size)
            dpg.draw_rectangle(pmin=self.position, pmax=tuple(np.add(self.position, (self.duration, 90))), fill=self.fill, rounding=self.rounding, parent=self.parent, tag=self.tag)
            # Draw image
            print(tuple(np.add(self.position, self.padding)),tuple(np.subtract(tuple(np.add(self.position, self.size)), self.padding)))
            dpg.draw_image(self.texture, pmin=tuple(np.add(self.position, self.padding)), pmax=tuple(np.subtract(tuple(np.add(self.position, self.size)), self.padding)), parent=self.parent, tag=self.tag2)
        except Exception as e:
            print("EXCEPTION")
            print(e)
    def drag_clip(self):
        # Draw a new clip at mouse position
        self.set_position(dpg.get_mouse_pos())
        self.draw_clip()

    def drop_clip(self):
        # Delete old clip
        # Draw a new clip at final mouse position
        self.drag_clip(dpg.get_mouse_pos())

    def resize_clip(self):
        # Get mouse position
        mp = dpg.get_mouse_pos()
        if self.lock_height:
            x, y = self.size
            self.size = (x+mp[0],y)
        else:
            self.size = tuple(np.add(self.size + mp))
        # Set position
        self.set_position(mp)
        # Draw the clip
        self.draw_clip()
        # Compute duration
