from kivymd.app import MDApp
from kivymd.uix.datatables.datatables import MDDataTable
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.textinput import TextInput

import random
import time


#data of typing records
records = sorted(["29.4", "26.8", "38.1"])
row_data = [i for i in range(len(records))]
column_data = [("No.", dp(30)), ("Time (sec)", dp(30))]

for i in range(len(records)):
    row_data[i] = (str(i), records[i])


#additional classes
class SpecialInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        super().keyboard_on_key_down(window, keycode, text, modifiers)

        print(self.text)
        if self.text == self.parent.chosen_text:
            self.parent.finish_game()

class Windows(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.menu = MenuScreen(name="menu")
        self.add_widget(self.menu)

        self.current = "menu"


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        print(row_data)
        self.add_widget(MDDataTable(size_hint=(0.4, 0.3), pos_hint={"x": 0.3, "y": 0.5}, column_data=column_data, row_data=row_data))

    def start_the_game(self):
        self.manager.game = GameScreen(name="game")
        self.manager.add_widget(self.manager.game)
        self.manager.current = "game"


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.texts = ["There once was a man, named Bill.", "When it's winter, it snows"]
        self.chosen_text = self.texts[random.randint(0, len(self.texts)-1)]
        self.ids["text_to_write"].text = self.chosen_text

        self.timer = 0
        self.clock = Clock.schedule_interval(self.cancel_timer, 1)

        self.final_time = None

    def cancel_timer(self, dt):
        self.ids["counter"].text = str(self.timer)
        if self.timer != 5:
            self.timer += 1
            return
        self.clock.cancel()
        self.remove_widget(self.ids["counter"])
        self.start_typing()

    def start_typing(self):
        self.ids["type_input"].disabled = False
        self.final_time = time.time()

    def update_rows(self):
        global row_data

        x = [i for i in range(len(records))]
        for i in range(len(records)):
            x[i] = (i, sorted(records)[i])
        row_data = x

    def finish_game(self):
        self.final_time = time.time() - self.final_time
        records.append(str(self.final_time))
        self.update_rows()

        self.manager.remove_widget(self.manager.menu)
        self.manager.menu = MenuScreen(name="menu")
        self.manager.add_widget(self.manager.menu)
        self.manager.current = "menu"


class MainApp(MDApp):
    def build(self):
        return Windows()


if __name__ == "__main__":
    MainApp().run()
