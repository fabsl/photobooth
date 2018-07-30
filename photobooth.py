from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
import time
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.pagelayout import PageLayout
from kivy.core.window import Window
from kivy.uix.camera import Camera
from PIL import Image, ImageOps
from kivy.uix.image import Image as kvImage
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors import ButtonBehavior


class ImageButton(ButtonBehavior, kvImage):
    pass

####################################################################
###                             Screens                          ###
####################################################################
class PreviewScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = 'preview'
        self.my_float = FloatLayout()
        self.bt_back = Button(text="back",size_hint=(.05,.05),pos=(0,0),
                                background_color=(0,0,0,0))
        self.my_float.add_widget(self.bt_back)
        self.count = Label(text="", font_size=350)
        self.abc = Button(text="abc",size_hint=(.05,.05),pos=(100,0),
                            background_color=(0,0,0,0))########################
        self.my_float.add_widget(self.abc)####################################
        self.add_widget(self.my_float)
        self.bt_back.bind(on_press=self.change_to_edit)
        self.abc.bind(on_press=self.capture)###########################
        self.cam1 = MirrorCamera(id = 'camera1',index=0,resolution=(1920, 1080),
                                keep_ratio=False,allow_stretch=True,play = True)
        self.add_widget(self.cam1)
        self.bind(on_enter=self.start_countdown)



    def start_countdown(self, obj):
        num = 5
        time_to_wait = 6
        self.add_widget(self.count)
        def count_it(num):
            if num == 0:
                self.remove_widget(self.count)
                return
            self.count.text = str(num)
            num -= 1
            Clock.schedule_once(lambda dt: count_it(num), 1)    #1 = delay

        Clock.schedule_once(lambda dt: count_it(num), 0)
        Clock.schedule_once(lambda dt: self.capture(obj), time_to_wait)
        Clock.schedule_once(lambda dt: self.change_to_edit(obj),time_to_wait)


    def capture(self,obj):
        camera = self.cam1
        timestr = time.strftime("%Y%m%d_%H%M%S")
        global path
        path = 'C:\\Users\\fpila\\Desktop\\All The Things\\Programming\\Python\\Photobooth\\Pictures\\IMG_{}.png'.format(timestr)
        camera.export_to_png(path)
        # mirror the image so it isn't mirrored anymore
        image = Image.open(path)
        image = ImageOps.mirror(image)
        image.save(path)
        print("Captured")


    def change_to_edit(self, obj):
        my_screenmanager.current = 'edit'

class Main_Screen(Screen):
    def __init__(self):
        super().__init__()
        self.name = 'main'
        self.my_grid = GridLayout(cols=3, rows=2, spacing= 50, padding=50) # change layout so buttons fit better
        self.bt_pic = Button(text="Picture")
        #self.bt_bw_pic = Button(text="Black&White Picture")
        #self.bt_gif = Button(text="GIF")
        self.bt_bommerang = Button(text="Boomerang")
        #self.bt_video = Button(text="Video")
        self.bt_test = Button(text="test")
        self.my_grid.add_widget(self.bt_pic)
        #self.my_grid.add_widget(self.bt_bw_pic)
        #self.my_grid.add_widget(self.bt_gif)
        self.my_grid.add_widget(self.bt_bommerang)
        #self.my_grid.add_widget(self.bt_video)
        self.my_grid.add_widget(self.bt_test)
        self.add_widget(self.my_grid)

        self.bt_pic.bind(on_press=self.on_click_preview)
        self.bt_test.bind(on_press=self.on_click_gallery)

    def on_click_preview(self, obj):
        my_screenmanager.current = 'preview'

    def on_click_gallery(self, obj):
        my_screenmanager.current = 'gallery'

class GalleryScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = 'gallery'
        global path

        # default pic for gallery but change when new 1 is taken
        # google photos

        self.my_grid = GridLayout(cols=1, rows=2, spacing= 25, padding=5)
        self.my_grid1 = GridLayout(cols=2, rows=1, spacing= 25, padding=45)
        self.my_image1 = kvImage(source = '1.png')
        self.my_grid1.add_widget(self.my_image1)

        self.my_box2 = BoxLayout(orientation='vertical',size_hint=(.3,.3),spacing=5)
        self.my_image2 = ImageButton(source = '2.png',on_press = self.show_pic_2)
        self.my_box2.add_widget(self.my_image2)
        self.my_image3 = ImageButton(source = '3.png',on_press = self.show_pic_3)
        self.my_box2.add_widget(self.my_image3)
        self.my_image4 = kvImage(source = 'Logo.png')
        self.my_box2.add_widget(self.my_image4)

        self.my_grid1.add_widget(self.my_box2)
        self.my_grid.add_widget(self.my_grid1)
        self.add_widget(self.my_grid)

        self.my_box1 = BoxLayout(orientation='horizontal',size_hint=(.15,.15),spacing=25)
        self.bt_back = Button(text="back",size_hint=(.5,.5))
        self.bt_back.bind(on_press=self.on_click)
        self.my_box1.add_widget(self.bt_back)
        self.bt_send = Button(text="send",size_hint=(.5,.5))
        self.my_box1.add_widget(self.bt_send)
        self.textinput = TextInput(text='e-mail',size_hint=(.5,.5))
        self.my_box1.add_widget(self.textinput)
        #self.bt_print = Button(text="print",size_hint=(.5,.5))
        #self.my_box1.add_widget(self.bt_print)

        self.my_grid.add_widget(self.my_box1)


    def on_click(self, obj):
        my_screenmanager.current = 'main'

    def show_pic_2(self,*args):
        temp = self.my_image1.source
        self.my_image1.source = self.my_image2.source
        self.my_image2.source = temp

    def show_pic_3(self,*args):
        temp = self.my_image1.source
        self.my_image1.source = self.my_image3.source
        self.my_image3.source = temp

class EditScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = 'edit'
        global path

        # default pic for gallery but change it when new 1 is taken
        # buttons for redo and next
        # apply filters -> How?
        # make filters


####################################################################
###                             Customs                          ###
####################################################################
class MirrorCamera(Camera):
    def _camera_loaded(self, *largs):
        self.texture = self._camera.texture
        self.texture_size = list(self.texture.size)
        self.texture.flip_vertical()

############################################################
class TestApp(App):
    def build(self):
        global my_screenmanager
        my_screenmanager = ScreenManager()
        preview = PreviewScreen()
        main = Main_Screen()
        gallery = GalleryScreen()
        edit = EditScreen()
        my_screenmanager.add_widget(main)
        my_screenmanager.add_widget(preview)
        my_screenmanager.add_widget(gallery)
        my_screenmanager.add_widget(edit)
        return my_screenmanager

if __name__ == '__main__':
    Window.fullscreen = 'auto'
    TestApp().run()
