Python ProgressBar

Simple usage:

```python

from progress_bar import ProgressBar
from time import sleep

with ProgressBar(high=10) as bar:
    for i in range(10):
        bar.render(i)

        sleep(0.1)

```

This code block prints one line and was **replacing** progress ten times,
as edit controller using package reprint.

Default progress view: `[####        ]` You can configure more thing while 
init bar. If you not user with construction, while render, you can
configure `RenderSettings` by render (render returns string)

ProgressBar give you more tools to conduct colors in your bar, seems
look in `ProgressBar` init method and `ProgressBar.render` function
