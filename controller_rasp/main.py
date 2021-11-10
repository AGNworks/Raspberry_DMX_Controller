import sys
from kivy.config import Config
from kivy.app import App
from kivy.lang import Builder 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
#from smbus2 import SMBus
import os
import time


addr = 0x20
#bus = SMBus(1)

decoder = 1
channel = 1

def send_array(dmx):
    for i in dmx:
        bus.write_byte(addr, i)
        
        
#For identification 
name_programmer  = "user"
passw_programmer = "12344321"



#open kivy file
Builder.load_file('design.kv')

dmx = []

for i in range(0,3,1):
    dmx.append(0)
print(len(dmx))

class ProgrammerScreen(Screen):
    def back_to_main(self):
        self.manager.transition.direction = "left"
        self.manager.current= "main_screen"
        
    def check_user(self, uname, pword):
        print(uname, pword)
        if name_programmer == uname and passw_programmer == pword:
            print("Welcome Master")
            sys.exit(0)
            
    def system_off(self):
        print("Shutting down")
        time.sleep(5)
        os.system("sudo shutdown -h now")


class MainScreen(Screen):
    def more_options(self):
        self.manager.transition.direction = "left"
        self.manager.current= "control_screen"
    def programming(self):
        self.manager.transition.direction = "right"
        self.manager.current= "programmer_screen"
    
    def turn_all_off(self):
        print("all_off")
        dmx[0] = 0
        dmx[1] = 0
        send_array(dmx)
        
    def turn_all_on(self):
        print("all_on")
        dmx[0] = 0
        dmx[1] = 1
        send_array(dmx)

    def turn_red(self):
        print("red")
        dmx[0] = 0
        dmx[1] = 2
        send_array(dmx)

    def turn_green(self):
        print("green")
        dmx[0] = 0
        dmx[1] = 3
        send_array(dmx)

    def turn_blue(self):
        print("blue")
        dmx[0] = 0
        dmx[1] = 4
        send_array(dmx)

    def turn_white(self):
        print("white")
        dmx[0] = 0
        dmx[1] = 5
        send_array(dmx)
        
    def turn_to_RGB(self):
        print("RGB")
        dmx[0] = 0
        dmx[1] = 6
        send_array(dmx)
        
    def turn_to_RGBW(self):
        print("RGBW")
        dmx[0] = 0
        dmx[1] = 7
        send_array(dmx) 


class ControlScreen(Screen):    
    def back_to_main(self):
        self.manager.transition.direction = "right"
        self.manager.current= "main_screen"

    def setting(self):
        self.manager.transition.direction = "left"
        self.manager.current= "channel_screen"

    def turn_to_RGB(self):
        print("RGB")
        dmx[0] = 0
        dmx[1] = 6
        send_array(dmx)
        
    def turn_to_RGBW(self):
        print("RGBW")
        dmx[0] = 0
        dmx[1] = 7
        send_array(dmx)
    
    def turn_red(self):
        global decoder
        print("red")
        dmx[0] = 1
        dmx[1] = 2
        dmx[2] = decoder
        send_array(dmx)

    def turn_green(self):
        global decoder
        print("green")
        dmx[0] = 1
        dmx[1] = 3
        dmx[2] = decoder
        send_array(dmx)

    def turn_blue(self):
        global decoder
        print("blue")
        dmx[0] = 1
        dmx[1] = 4
        dmx[2] = decoder
        send_array(dmx)

    def turn_white(self):
        global decoder
        print("white")
        dmx[0] = 1
        dmx[1] = 5
        dmx[2] = decoder
        send_array(dmx)
        
    def plus_one(self):
        global decoder
        print("+1")   
        dmx[0] = 0
        dmx[1] = 0
        if decoder < 300 :
            decoder += 1
        self.ids.labeldecoder.text = str(decoder)
        send_array(dmx)
        
    def plus_ten(self):
        global decoder
        print("+10")
        dmx[0] = 0
        dmx[1] = 0
        if (decoder < 300) :
            decoder += 10
        self.ids.labeldecoder.text = str(decoder)
        send_array(dmx)
        
    def minus_one(self):
        global decoder
        print("-1")
        print(decoder)
        dmx[0] = 0
        dmx[1] = 0
        if decoder > 1 :
            decoder -= 1
        self.ids.labeldecoder.text = str(decoder)
        send_array(dmx)
        
    def minus_ten(self):
        global decoder
        print("-10")
        dmx[0] = 0
        dmx[1] = 0
        if decoder > 10 :
            decoder -= 10
        self.ids.labeldecoder.text = str(decoder)
        send_array(dmx)
        
    def turn_off(self):
        print("off")
        dmx[0] = 0
        dmx[1] = 0
        send_array(dmx)

class ChannelScreen(Screen):
    def back_to_control(self):
        self.manager.transition.direction = "right"
        self.manager.current= "control_screen"
        
    def scenes(self):
        self.manager.transition.direction = "left"
        self.manager.current= "scenes_screen"
    
    def plus_one(self):
        global channel
        print("+1")   
        dmx[0] = 0
        dmx[1] = 0
        if channel < 512 :
            channel += 1
        self.ids.labelchannel.text = str(channel)
        send_array(dmx)
        
    def plus_ten(self):
        global channel
        print("+10")
        dmx[0] = 0
        dmx[1] = 0
        if (channel < 503) :
            channel += 10
        self.ids.labelchannel.text = str(channel)
        send_array(dmx)
        
    def minus_one(self):
        global channel
        print("-1")
        print(channel)
        dmx[0] = 0
        dmx[1] = 0
        if channel > 1 :
            channel -= 1
        self.ids.labelchannel.text = str(channel)
        send_array(dmx)
        
    def minus_ten(self):
        global channel
        print("-10")
        dmx[0] = 0
        dmx[1] = 0
        if channel > 10 :
            channel -= 10
        self.ids.labelchannel.text = str(channel)
        send_array(dmx)
        
    def slider_move(self):
        global channel
        dmx[0] = 2
        dmx[1] = channel
        dmx[2] = int(self.ids.slider.value)
        print(int(self.ids.slider.value))
        send_array(dmx)

class ScenesScreen(Screen):
    def back_to_channel(self):
        self.manager.transition.direction = "right"
        self.manager.current= "channel_screen"
        dmx[0] = 3
        dmx[1] = 0
        print("Stop scene")
        send_array(dmx)
        
    def scene_one(self):
        dmx[0] = 3
        dmx[1] = 1
        print("Scene 1")
        send_array(dmx)
        
    def stop_scene(self):
        dmx[0] = 3
        dmx[1] = 0
        print("Stop scene")
        send_array(dmx)
        
class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    Config.set('graphics','fullscreen','auto')
    Config.set('graphics','window_state', 'maximized')
    Config.write()
    MainApp().run()