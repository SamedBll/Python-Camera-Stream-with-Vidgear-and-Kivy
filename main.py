import kivy
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from vidgear.gears import CamGear
from vidgear.gears import NetGear
from datetime import datetime
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2


class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='horizontal')
        self.image = Image()
        layout.add_widget(self.image)
        options_1 = {
            "CAP_PROP_FRAME_WIDTH": 1920, # resolution 320x240
            "CAP_PROP_FRAME_HEIGHT": 1080,
        }
        self.stream = CamGear(source=0, logging=False, **options_1).start() #loggingi kapatacaz
        
        options = {"bidirectional_mode": True}
        self.server = NetGear(
            address="192.168.0.14", 
            port="5454",
            protocol="tcp",
            pattern=1,
            logging=False,
            **options
        )
        Clock.schedule_interval(self.load_video, 1.0/30.0)
        Clock.schedule_interval(self.stream_video, 1.0/30.0)
        return layout

    def stream_video(self, *args):
        frames = self.stream.read()
        now = datetime.now()
        zaman = now.strftime("%H%M%S%f")
        self.server.send(frames, message=zaman)

    def load_video(self, *args):
        frame = self.stream.read()
        buffers = cv2.flip(frame,0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffers, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture


if __name__ == '__main__':
    MyApp().run()
