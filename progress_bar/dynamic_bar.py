from typing import TYPE_CHECKING
from reprint.reprint import output


if TYPE_CHECKING:
    from .progress_bar import ProgressBar


class DynamicBar:
    def __init__(self, progress_bar: 'ProgressBar'):
        self.bar = progress_bar
        self._output = output('list')
        self._controller = self._output.__enter__()

    def render(self, progress: float) -> None:
        text = self.bar.render(progress)

        self._controller[0] = text

    __call__ = render

    def replace(self, text) -> None:
        self._controller[0] = text

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._output.refresh(forced=True)

        return self
