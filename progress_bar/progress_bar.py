import typing
from colorama import Style, Fore

from .coloring import ColoredStr, text_optional_colored, Palette
from .dynamic_bar import DynamicBar


class RenderSettings:
    """ Render setting object to ProgressBar.render """

    class Text:
        def __init__(self, prefix: text_optional_colored, postfix: text_optional_colored,
                     fill: text_optional_colored, empty: text_optional_colored):
            palette = Palette()

            self.prefix = self.standardize_text(prefix, palette, 'prefix')
            self.postfix = self.standardize_text(postfix, palette, 'postfix')
            self.fill = self.standardize_text(fill, palette, 'fill')
            self.empty = self.standardize_text(empty, palette, 'empty')

            self.palette = palette

        def __iter__(self):
            result = iter(vars(self).items())

            return result

        def keys(self):
            result = vars(self).keys()

            return result

        @staticmethod
        def standardize_text(text: text_optional_colored, pinned_palette: Palette, label: str) -> str:
            """Standardize text

            If color found in text, it removing and
            writing into pinned pallet.

            """

            if isinstance(text, tuple):
                text, color = text
            elif isinstance(text, ColoredStr):
                text, color = text.text, text.color
            else:
                text, color = text, ''

            setattr(pinned_palette, label, color)

            return text

    def __init__(self, prefix: text_optional_colored, postfix: text_optional_colored,
                 fill: text_optional_colored, empty: text_optional_colored, bar_len: int,
                 palette: Palette = None):

        text = self.Text(prefix, postfix, fill, empty)

        if palette is None:
            palette = text.palette

        self.prefix = text.prefix
        self.postfix = text.postfix
        self.fill = text.fill
        self.empty = text.empty

        self.palette = palette

        self.bar_len = bar_len

    @typing.overload
    def colorize(self, *, palette: Palette = None, reset: bool = False):
        ...

    @typing.overload
    def colorize(self, *, prefix: str = None, postfix: str = None, fill: str = None, empty: str = None,
                 reset: bool = False):
        ...

    def colorize(self, *, palette: Palette = None, prefix: str = None, postfix: str = None,
                 fill: str = None, empty: str = None, reset: bool = False):

        """Render palette colorize"""

        if palette is None:
            palette = Palette(prefix, postfix, fill, empty)

        values_to_reset = None
        if not reset:
            values_to_reset = [key
                               for key, value in palette
                               if value != '']

        self.reset_color(values_to_reset)

        self.palette = palette

    def reset_color(self, vars_to_reset: list[str] = None) -> None:
        for key, value in self.palette:
            if key in vars_to_reset:
                setattr(self.palette, key, None)

        return None


class ProgressBar:
    """Progress bar object
    Use it to visualize progress

    Simple guide
    ------------

    You can replace any symbol in render
    Do it on initialize step or letter

    >>> bar = ProgressBar(high=50, fill='|', prefix='/', postfix='/')
    >>> bar.render(20)
    '/||||      /'
    >>> bar.render_settings.fill = '#'
    >>> bar.render(30)
    '/######    /'

    Colorizing
    ----------

    Also, you can colorize your bar (examples use colorama.Fore and colorama.Style)

    >>> bar = ProgressBar(high=50)
    >>> bar.colorize(fill=Fore.GREEN)

    On init step, you can do it so...

    >>> bar = ProgressBar(fill=('|', Fore.GREEN))

    >>> bar = ProgressBar(fill=ColoredStr(text='|', color=Fore.GREEN))

    """

    @typing.overload
    def __init__(self, *, low: int = None, high: int = None, prefix: text_optional_colored = None,
                 postfix: text_optional_colored = None, fill: text_optional_colored = None,
                 empty: text_optional_colored = None, bar_len: int = None, palette: Palette = None):
        ...

    @typing.overload
    def __init__(self, *, low: int = None, high: int = None, render_settings: RenderSettings = None):
        ...

    def __init__(self, *, low: int = 0, high: int = 100, prefix: text_optional_colored = '[',
                 postfix: text_optional_colored = ']', fill: text_optional_colored = '#',
                 empty: text_optional_colored = ' ', bar_len: int = 10,
                 palette: Palette = None,
                 render_settings: RenderSettings = None):

        """Progress bar object initialize method

        :param low: lowest value of bar
        :param high: highest value of bar
        :param render_settings: RenderSettings object, settings for method render
        """

        if render_settings is None:
            render_settings = RenderSettings(prefix, postfix, fill, empty, bar_len, palette)

        self.low = low
        self.high = high
        self.render_settings = render_settings

        self.colorize = self.render_settings.colorize

        self._current_dynamic: typing.Optional[DynamicBar] = None

    def render(self, progress: typing.Union[int, float], render_settings: RenderSettings = None) -> str:
        """Progress bar rendering

        :arg progress: integer or float value, bar progress to render
        :arg render_settings: RenderSettings object, render settings (default is sat while init progress bar)
        :returns: result string

        >>> my_bar = ProgressBar(high=50)
        >>> my_bar.render(10)
        '[##        ]'

        """

        if render_settings is None:
            render_settings = self.render_settings

        bar = self._render_bar(progress, render_settings)

        result = render_settings.prefix + bar + render_settings.postfix

        return result

    def _render_bar(self, raw_progress: typing.Union[int, float], render_settings: RenderSettings):
        """Bar rendering
        Render func without add postfix and prefix
        """

        progress = raw_progress / (self.high - self.low)  # between 0 and 1
        float_shanks_fill = render_settings.bar_len * progress

        shanks_fill = int(float_shanks_fill)

        if shanks_fill > render_settings.bar_len:
            shanks_fill = render_settings.bar_len

        shanks_empty = int(render_settings.bar_len - shanks_fill)

        bar = (
                render_settings.palette.fill
                + (shanks_fill * render_settings.fill)
                + self._optimize_style_reset(render_settings.palette.fill)

                + render_settings.palette.empty
                + (shanks_empty * render_settings.empty)
                + self._optimize_style_reset(render_settings.palette.empty)
        )

        return bar

    @staticmethod
    def _optimize_style_reset(old_color: str):
        if not old_color:
            return ''
        else:
            return Style.RESET_ALL

    def get_controller(self) -> DynamicBar:
        """Bar in terminal

        Return dynamic bar to easily render bar in terminal

        """

        dynamic = DynamicBar(self)

        return dynamic

    def __enter__(self) -> DynamicBar:
        new_dynamic = self.get_controller()
        self._current_dynamic = new_dynamic

        return new_dynamic

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._current_dynamic:
            return None

        dynamic = self._current_dynamic

        return dynamic.__exit__(exc_type, exc_val, exc_tb)
