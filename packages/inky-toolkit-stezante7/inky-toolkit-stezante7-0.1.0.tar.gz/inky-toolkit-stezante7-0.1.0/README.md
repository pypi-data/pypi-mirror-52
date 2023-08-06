# Inky Toolkit

Inky Toolkit is a set of utilities for Inky pHAT display that I created to use on a few of my RasberryPi projects.

## How to use it

To install it run:

```
pip install inky-toolkit-stezante7
```

### InkyText

**write_text:**
display a text message, automatically taking care of number of words/rows to display.
If there is not enough space for the text to be displayed, a postfix symbol (by default "...") will show in the bottom right of the screen.

**Example**

```python
from inky_toolkit import inkytext

inkyT = inkytext.InkyText(color="red", font_type=FredokaOne, font_size=20, more_text_postfix="...")

inkyT.write_text("One love, one blood, one life, you got to do what you should. One life with each other: sisters, brothers. One life, but we're not the same. We get to carry each other, carry each other")

```

![IMG_20190923_204610](https://user-images.githubusercontent.com/14370527/65459784-7dbc1300-de48-11e9-8f9f-d14effd99f63.jpg)

## More

This Python library uses inky official library.
More details about inky and inkyphat libraries here:

- https://pypi.org/project/inky/
- https://github.com/pimoroni/inky-phat
- http://docs.pimoroni.com/inkyphat

## License

This library is available under the MIT license.
