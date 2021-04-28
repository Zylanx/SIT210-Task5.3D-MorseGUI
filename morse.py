from time import sleep

import asyncio
import RPi.GPIO as gpio


# Our encoding will use "/" as a seperator between letters
# and " " between words


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
        "Z": "--..",
        " ": " "
    }

    def __init__(self, led_pin):
        self.led_pin = led_pin

        gpio.setup(self.led_pin, gpio.OUT)
        gpio.output(self.led_pin, gpio.LOW)

    async def output_text(self, message: str):
        encoded_message = self._generate_encoded_message(message)

        for index, character in enumerate(encoded_message):
            if character == "/":
                await asyncio.sleep(self.inter_char_period)
            elif character == " ":
                await asyncio.sleep(self.word_space_period)
            else:
                await self._emit_char(character)
                if (index + 1) < len(encoded_message) and encoded_message[index+1] not in [" ", "/"]:
                    await asyncio.sleep(self.intra_char_period)

    @classmethod
    def _generate_encoded_message(cls, message: str):
        encoded_message = ""

        if len(message) > 0:
            encoded_message += cls._get_char_string(message[0])

            if len(message) > 1:
                for character in message[1:]:
                    if character == " ":
                        encoded_message += " "
                    else:
                        if encoded_message[-1] != " ":
                            encoded_message += "/"
                        encoded_message += cls._get_char_string(character)

        return encoded_message

    @classmethod
    def _get_char_string(self, input_char: str):
        input_upper = input_char.upper()

        return self.translation_dictionary.get(input_upper, "")

    async def _emit_char(self, character: str):
        if character == ".":
            await self._emit_dit()
        elif character == "-":
            await self._emit_dah()

    async def _emit_dit(self):
        gpio.output(self.led_pin, gpio.HIGH)
        await asyncio.sleep(self.dit_period)
        gpio.output(self.led_pin, gpio.LOW)

    async def _emit_dah(self):
        gpio.output(self.led_pin, gpio.HIGH)
        await asyncio.sleep(self.dah_period)
        gpio.output(self.led_pin, gpio.LOW)
