from time import sleep

import asyncio
import RPi.GPIO as gpio


# Our encoding will use "/" as a seperator between letters
# and " " between words


class MorseCode:
    """
    A class that handles outputting messages to an LED using Morse code.
    """
    # define the timing constants
    unit_period = 250 / 2500

    dit_period = 1 * unit_period
    dah_period = 3 * unit_period

    intra_char_period = 1 * unit_period
    inter_char_period = 3 * unit_period
    word_space_period = 7 * unit_period

    # This dictionary translates letters to their Morse code representation.
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

        # Set up the pin and set it to a known state
        gpio.setup(self.led_pin, gpio.OUT)
        gpio.output(self.led_pin, gpio.LOW)


    async def output_text(self, message: str):
        """
        Display a message in Morse code on an LED.
        This method is asynchronous so that the GUI can still respond while this
        class is outputting Morse code.
        It first converts the message to morse code then displays it.
        """
        # Get a Morse code string representation of the message
        encoded_message = self._generate_encoded_message(message)

        # Loop through the message handling special pause characters and displaying each character
        for index, character in enumerate(encoded_message):
            if character == "/":
                await asyncio.sleep(self.inter_char_period)
            elif character == " ":
                await asyncio.sleep(self.word_space_period)
            else:
                await self._emit_char(character)

                # If we aren't at the last character and the next character isn't a special character
                # then it is still part of the current letter and we need to do an intra character wait.
                if (index + 1) < len(encoded_message) and encoded_message[index+1] not in [" ", "/"]:
                    await asyncio.sleep(self.intra_char_period)


    @classmethod
    def _generate_encoded_message(cls, message: str):
        """
        Convert a message to a Morse code string
        """
        encoded_message = ""

        # Only add to the string if there are letters to convert
        if len(message) > 0:
            encoded_message += cls._get_char_string(message[0])

            # If there are more than one characters, loop through and convert the rest
            # adding word joiners
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
    def _get_char_string(cls, input_char: str):
        """
        Convert a single charcter to a Morse code string
        """
        input_upper = input_char.upper()

        return cls.translation_dictionary.get(input_upper, "")

    async def _emit_char(self, character: str):
        """
        Display dit or dah depending on the character.
        """
        if character == ".":
            await self._emit_dit()
        elif character == "-":
            await self._emit_dah()

    async def _emit_dit(self):
        """
        Display a dit on the LED.
        """
        gpio.output(self.led_pin, gpio.HIGH)
        await asyncio.sleep(self.dit_period)
        gpio.output(self.led_pin, gpio.LOW)

    async def _emit_dah(self):
        """
        Display a dah on the LED.
        """
        gpio.output(self.led_pin, gpio.HIGH)
        await asyncio.sleep(self.dah_period)
        gpio.output(self.led_pin, gpio.LOW)
