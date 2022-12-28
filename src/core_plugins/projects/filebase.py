import dearpygui.dearpygui as dpg

class FileBase:
    def __init__(self, fname, img=None, drag_callback=""):
        self.fname = fname
        self.img = img
        self.w, self.h, self.channels, self.data = 100,100,0,0
        self.tag=None
        self.drag_callback=drag_callback

    def load_image(self):
        self.w, self.h, self.channels, self.data = dpg.load_image(self.img)

    def cb(self, other=None, some=None):
        print(other, some)


    def stage_card_to_payload(self, sender, data, user):
        card = sender
        payload = card #dpg.get_item_children(card, slot=3)[0]
        old_card_window = dpg.get_item_parent(card)
        self.drag_callback(self.tag)


    def setup(self, parent):
        self.load_image()
        self.tag = dpg.generate_uuid()
        with dpg.child_window(parent=parent, height=self.h, width=self.w, no_scrollbar=True):
            with dpg.texture_registry(show=False):
                dpg.add_static_texture(self.w, self.h, self.data, tag=self.tag)
            
            with dpg.group(drag_callback=self.stage_card_to_payload) as card:
                dpg.add_image(self.tag)
                with dpg.drag_payload(parent=card, payload_type="CARD", drag_data=card, drop_data="drop data"):
                    dpg.add_image(self.tag)