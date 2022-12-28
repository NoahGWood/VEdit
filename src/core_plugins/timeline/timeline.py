import dearpygui.dearpygui as dpg2

from core_plugins.projects.filebase import FileBase

class Plugin:
    def __init__(self, parent):
        self.parent = parent
        self.name = "timeline"
        self.parent.add_on_start(self.start)
        self.parent.timeline = self
        self.tracks = []
        self.parent.register_update(self.mouse_handling)

        self.w=0
        self.drag=False
        self.was_drag=False
        self.was_dropped=False
        self.external_drag=False
        self.dropped_position=None
        self.drag_clip=False
        self.clip = None
        self.clips = []

    def print_me(self, sender):
        print('derp')

    def preferences(self, sender):
        if not self.preferences_open:
            self.preferences_window(dpg2)

    
    def add_card_from_stage(self, sender, data, user):
        print(sender, data, user)
        drop_target_item = sender+1
        card = data
        old_card_window = dpg2.get_item_parent(data)
        print(drop_target_item)
        print(dpg2.get_item_type(drop_target_item))
        new_card_container = dpg2.add_child_window(parent=drop_target_item, height=dpg2.get_item_height(old_card_window), width=dpg2.get_item_width(old_card_window))
        dpg2.move_item(card, parent=new_card_container)
        dpg2.delete_item(old_card_window)


    def base_item(self, parent):
        dpg2.draw_rectangle((0,0),(100,100), fill=(69,69,69), parent=parent)
        dpg2.draw_text((5,5), "Track 1", size=20, parent=parent)


    def drag_callback(self, clip):
        self.clip = clip
        if clip not in self.clips:
            self.clips.append(clip)
        self.external_drag = True

    def add_clip(self):
        if self.clip != None:
            parent = dpg2.get_alias_id("track")
            # Get image position
            x = self.dropped_position
            self.clip.parent = parent
 #           self.clip.set_position(x)
            self.clip.draw_clip()
    #        if self.image != None:
    #            dpg2.draw_image(self.image, pmin=(x,5), pmax=(x+100, 95), parent=parent)

    def internal_drag(self):
        x, y = dpg2.get_drawing_mouse_pos()
        print("INTERNAL DRAGGING")
        print(self.drag, self.external_drag, self.was_drag, self.was_dropped, self.clip)
        print(True, False, False, True)
        for clip in self.clips:
            if clip == None:
                print("REEE")
                self.clips.remove(clip)                
                pass
            else:
                min_x = clip.position[0]
                max_x, max_y = (min_x+clip.duration, clip.height)
                print(min_x, max_x, x)
                if x >= min_x and x <= max_x:
                    print(clip)
                    print("DRAAGGING A CLIP!")
                    self.clip = clip
                    clip.drag_clip()
                    break

    def mouse_handling(self):
        """Used to handle mouse calling and stuff"""
        # Check if an item was dropped to the track first.
        # This flag is set on previous frame meaning that we are getting the
        # mouse position one frame later.
        # The reason for this is because dearpygui does not support drag/drop to drawings
        if self.was_dropped:
            self.dropped_position = dpg2.get_drawing_mouse_pos()
            # Make sure we're not further back than we should be
            if self.dropped_position[0] < 100:
                self.dropped_position[0] = 100
            if self.clip:
                if self.external_drag:
                    self.add_clip()
                    self.external_drag = False # Free up external_dragged
                elif self.drag_clip:
                    self.clip.set_position(self.dropped_position)
                    self.clip.drag_clip()           
                self.clip = None # Free up the clip
            self.was_dropped = False # Free up was_dropped
        # Resize track width to window width
        w = dpg2.get_item_width(dpg2.get_alias_id("timeline"))
        dpg2.set_item_width(dpg2.get_alias_id("track"), w)
        if w != self.w:
            dpg2.delete_item(dpg2.get_alias_id("track_1_width"))
            self.w = w
            self.draw_rect(w, dpg2.get_alias_id("track"))
        x, y = dpg2.get_drawing_mouse_pos()
        self.drag = dpg2.is_mouse_button_dragging(0,0.1)
        if self.drag:
            if x > w or x < 100:
                self.external_drag=False
    
        if self.drag == True and self.external_drag == False and self.was_drag == False and self.clip==None:
            #  Only works if mouse was in drawing before drag started
            print("INTERNAL DRAAGGING")
            self.internal_drag()
            self.was_drag=True
            self.drag_clip = True
        if self.drag_clip == True and self.clip != None and self.external_drag == False:
            self.clip.drag_clip()
#        print(self.drag, self.external_drag, self.was_drag, self.was_dropped, self.clip==None)
#s        print(True, False, False, True)

        # Must run at the end
        if self.drag  == True:
            self.was_drag = True
        else:
            if self.was_drag == True:
                self.was_drag = False
                self.was_dropped = True
                print(len(self.clips))
        
    def draw_rect(self, w, parent):
        dpg2.draw_rectangle((0,0), (w,100), fill=(70, 126, 145), rounding=20, tag="track_1_width", parent=parent)
        self.base_item(parent=parent)
        for i in range(0, w, 50):
            dpg2.draw_line((i+100,0), (i+100,100), color=(240, 240, 240), parent=parent)
            dpg2.draw_text((i+100,2), str(i/100), size=14, parent=parent)

    def timeline_window(self, dpg):
        with dpg.window(label="timeline", tag="timeline", width=dpg2.get_viewport_width()) as modal_id:
            with dpg2.group(horizontal=True):
                dpg2.add_spacer(width=100)
                dpg2.add_slider_float(width=-1, tag="timeline_slider")
            with dpg2.group(drop_callback=self.drop_clip):
                with dpg2.drawlist(width=dpg2.get_item_width(modal_id), height=100, tag="track") as dl:
                    self.draw_rect(dpg2.get_item_width(modal_id), dl)

    def start(self):
        self.timeline_window(dpg2)

    def render_center(self, c, p=None):
        print(c,p)
        if p:
            dpg2.set_item_pos(p, [200,200])

    def drop_clip(self, sender, data):
        print(sender, data)






"""

1. Get Mouse Position
2. Get a list of tracks
3. Get screen coordinates
4. Get height of number of tracks x height
5. Get frame count (max-min or 1)


if window is focused && alt key is pressed and right click
    then pan vieww




"""