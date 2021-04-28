import asyncio
import os


os.environ["KIVY_EVENTLOOP"] = "asyncio"

import RPi.GPIO as gpio
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

from morse import MorseCode


LED_PIN = 33

gpio.setmode(gpio.BOARD)


class MorseScreen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2

        self._morse_code = MorseCode(LED_PIN)
        self._morse_code_task = None

        self.text_input = TextInput()
        button = Button(text="Display Message")
        button.bind(on_release=self.output_message)

        self.add_widget(self.text_input)
        self.add_widget(button)

    def output_message(self, value):
        if (self._morse_code_task is None) or (self._morse_code_task and self._morse_code_task.done()):
            self._morse_code_task = asyncio.create_task(self._morse_code.output_text(self.text_input.text))

    def on_parent(self, widget, parent):
        if parent is None and self._morse_code_task is not None:
            self._morse_code_task.cancel()

class MorseApp(App):
    def build(self):
        return MorseScreen()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(MorseApp().async_run())
    except:
        pass
    finally:
        gpio.cleanup()
        loop.close()
