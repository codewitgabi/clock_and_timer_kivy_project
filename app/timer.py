import kivy
kivy.require("2.0.0")
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import StringProperty, Clock, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
import time


class ClockScreen(Screen):
	cur_time = StringProperty("")
	am_or_pm = StringProperty("")
			
	def update_time(self, dt):
		self.cur_time = time.strftime("%X")
		self.am_or_pm = time.strftime("%p")
	

class CreateTimerScreen(Screen):
	cur_timer_label_text = StringProperty("[u]00h 00m 00s[/u]")
	default_cur_timer = ""
	
	
	def enable_button(self):
		self.ids.timer_btn0.disabled = False
		self.ids.timer_btn1.disabled = False
		self.ids.timer_btn2.disabled = False
		self.ids.timer_btn3.disabled = False
		self.ids.timer_btn4.disabled = False
		self.ids.timer_btn5.disabled = False
		self.ids.timer_btn6.disabled = False
		self.ids.timer_btn7.disabled = False
		self.ids.timer_btn8.disabled = False
		self.ids.timer_btn9.disabled = False
		
	
	def timer_button_pressed(self, btn_text):
		if len(self.default_cur_timer) == 0 and btn_text == "0":
			self.ids.start_btn.disabled = True
			self.remove_widget(self.ids.start_btn)
		else:
			self.default_cur_timer += btn_text
			base = self.default_cur_timer.zfill(6)
			output = "[u]" + base[:2] + "h " + base[2:4] + "m " + base[4:] + "s" + "[/u]"
			self.cur_timer_label_text = output
			self.ids.start_btn.disabled = False
				
			if int(self.cur_timer_label_text[3]) > 0:
				self.ids.timer_btn0.disabled = True
				self.ids.timer_btn1.disabled = True
				self.ids.timer_btn2.disabled = True
				self.ids.timer_btn3.disabled = True
				self.ids.timer_btn4.disabled = True
				self.ids.timer_btn5.disabled = True
				self.ids.timer_btn6.disabled = True
				self.ids.timer_btn7.disabled = True
				self.ids.timer_btn8.disabled = True
				self.ids.timer_btn9.disabled = True
				
			self.ids.start_btn.disabled = False
			
		
	def start_display_timer(self):
		self.manager.get_screen("timer_display").begin()
		
		
	def delete_item(self):
		if len(self.default_cur_timer) > 0:
			self.enable_button()
			data = self.default_cur_timer[:-1]
			new_data = data.zfill(6)
			new_timer = "[u]" + new_data[:2] + "h " + new_data[2:4] + "m " + new_data[4:] + "s" + "[/u]"
			
			self.cur_timer_label_text = new_timer
			self.default_cur_timer = str(int(data)) if len(str(data)) != 0 else ""
			self.ids.start_btn.disabled = False
		
		if len(self.default_cur_timer) == 0:
			self.ids.start_btn.disabled = True
			

class DisplayTimerScreen(Screen):
	timer_text = StringProperty("00:00:00")
	angle = NumericProperty(0)	
	
	
	def update_timer(self, dt):
		try:
			if self.cur_time >= 0:
				min, secs = divmod(self.cur_time, 60)
				hour, min = divmod(min, 60)
				
				self.cur_time -= 1
				self.angle -= 360/(self.given_time)
				self.timer_text = f"{hour:02d}:{min:02d}:{secs:02d}"
				
			else:
				self.cur_time = self.given_time
				m, s = divmod(self.cur_time, 60)
				h, m = divmod(m, 60)
				self.timer_text = f"{h:02d}:{m:02d}:{s:02d}"
				self.angle = 0
				self.ids.start_btn.disabled = False
				self.manager.get_screen("create_timer").ids.start_btn.disabled = False
				Clock.unschedule(self.clock)
		except:
			pass
			
	
	def begin(self):
		self.clock = Clock.schedule_interval(self.update_timer, 1)
		self.ids.start_btn.disabled = True
		self.manager.get_screen("create_timer").ids.start_btn.disabled = True
		
		
	def pause_timer(self):
		try:
			if self.given_time != 0:
				Clock.unschedule(self.clock)
				self.ids.start_btn.disabled = False
				self.manager.get_screen("create_timer").ids.start_btn.disabled = False
		except:
			pass
		
				
	def delete_timer(self):
		try:
			self.given_time = 0
			self.cur_time = self.given_time
			self.timer_text = "00:00:00"
			self.angle = 0
			Clock.unschedule(self.clock)
			self.ids.start_btn.disabled = True
			self.manager.get_screen("create_timer").ids.start_btn.disabled = False
			self.manager.transition.direction = "right"
			self.manager.current = "create_timer"
		except:
			pass
		

class TimerApp(App):
	def build(self):
		Window.clearcolor = [34/255.0, 32/255.0, 119/225.0, 1]
		screen_manager = ScreenManager()
		
		widget = ClockScreen(name= "clock")
		Clock.schedule_interval(widget.update_time, 1)
		
		screen_manager.add_widget(widget)
		
		screen_manager.add_widget(
			CreateTimerScreen(name= "create_timer")
		)
		
		screen_manager.add_widget(
			DisplayTimerScreen(name= "timer_display")
		)
		
		return screen_manager
		

if __name__ == "__main__":	
	TimerApp().run()