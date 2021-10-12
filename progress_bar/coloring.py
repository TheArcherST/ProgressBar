from typing import Union, Tuple, Optional
from colorama import Fore, Back


class ColoredStr:
    def __init__(self, text, color):
        self.color = color
        self.text = text


text_optional_colored = Union[str, Tuple[str, str], ColoredStr]


class Palette:
    def __init__(self, prefix: str = None, postfix: str = None, fill: str = None, empty: str = None):

        self.prefix = self.normalize_color(prefix)
        self.postfix = self.normalize_color(postfix)
        self.fill = self.normalize_color(fill)
        self.empty = self.normalize_color(empty)

    def __iter__(self):
        result = iter(vars(self).items())

        return result

    @classmethod
    def normalize_color(cls, color: Optional[str]) -> str:
        if color is None:
            return ''

        if not cls.is_color(color):
            raise ValueError

        return color

    @staticmethod
    def is_color(color: Optional[str]) -> bool:
        if color == '' or color is None:
            return True

        fore = vars(Fore).values()
        back = vars(Back).values()

        result = color in fore or color in back

        return result
