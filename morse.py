from time import sleep

import asyncio
import RPi.GPIO as gpio


class MorseCode:
    unit_period = 250 / 2500

    dit_period = 1 * unit_period
    dah_period = 3 * unit_period

    intra_char_period = 1 * unit_period
    inter_char_period = 3 * unit_period
    word_space_period = 7 * unit_period

    translation_dictionary = {
        "A": ".-",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": ".-.",
        "S": "...",
        "T": "-",
        "U": "..-",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--.."
    }

    def __init__(self, led_pin):
        self.led_pin = led_pin

        gpio.setup(self.led_pin, gpio.OUT)
        gpio.output(self.led_pin, gpio.LOW)

    async def output_text(self, message: str):
        for character in message:
            if character == " ":
                await asyncio.sleep(self.word_space_period)
            else:
                await self._emit_char(character)
                await asyncio.sleep(self.inter_char_period)

    def _get_char_string(self, input_char: str):
        input_upper = input_char.upper()

        return self.translation_dictionary.get(input_upper, "")

    async def _emit_char(self, char_string: str):
        for character in self._get_char_string(char_string):
            if character == ".":
                await self._emit_dit()
            elif character == "-":
                await self._emit_dah()
            else:
                # Invalid character. Just skip it
                continue

            await asyncio.sleep(self.intra_char_period)

    async def _emit_dit(self):
        gpio.output(self.led_pin, gpio.HIGH)
        await asyncio.sleep(self.dit_period)
        gpio.output(self.led_pin, gpio.LOW)

    async def _emit_dah(self):
        gpio.output(self.led_pin, gpio.HIGH)
        await asyncio.sleep(self.dah_period)
        gpio.output(self.led_pin, gpio.LOW)
