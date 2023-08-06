import functools
import sys

try:
    from PIL import Image, ImageFont, ImageDraw
except ImportError:
    sys.exit(
        "This library requires the PIL module\nInstall with: sudo pip install PIL")

try:
    from inky import InkyPHAT
except ImportError:
    sys.exit(
        "This library requires the inky module\nInstall with: sudo pip install inky")

try:
    from font_fredoka_one import FredokaOne
except ImportError:
    sys.exit(
        "This library requires the font_fredoka_one module\nInstall with: sudo pip install font_fredoka_one")


class InkyText:

    def __init__(self, color="red", font_type=FredokaOne, font_size=20, more_text_postfix="..."):
        self.inkyphat = InkyPHAT(color)
        self.color = self.__get_inky_color(color)

        self.more_text_postfix = more_text_postfix
        self.img = Image.new("P", (self.inkyphat.WIDTH, self.inkyphat.HEIGHT))
        self.font = ImageFont.truetype(font_type, font_size)

    def __get_inky_color(self, color):
        if color == "red":
            return self.inkyphat.RED
        if color == "black":
            return self.inkyphat.BLACK
        if color == "yellow":
            return self.inkyphat.YELLOW

        raise ValueError("Color {} is not valid!".format(color))

    def __get_words_count_line(self, words, word_count):
        phrase = ' '.join(words[0:word_count])
        w, h = self.font.getsize(phrase)

        if w > self.inkyphat.WIDTH or word_count > len(words):
            return word_count-1
        else:
            return self.__get_words_count_line(words, word_count + 1)

    def __get_text_lines(self, text):
        words = text.split(" ")
        words_count = len(words)
        words_proccessed = 0

        words_per_line_count = 0
        start_idx = 0
        lines = []

        while words_proccessed < words_count:
            words_per_line_count = self.__get_words_count_line(
                words[start_idx:], 0)
            end_idx = start_idx+words_per_line_count

            words_line = words[start_idx:end_idx]
            lines.append(' '.join(words_line))

            start_idx = start_idx + words_per_line_count
            words_proccessed += words_per_line_count

        return lines

    def write_text(self, text):
        lines = self.__get_text_lines(text)
        y_cursor = 0
        line_idx = 0
        lines_count = len(lines)
        draw = ImageDraw.Draw(self.img)

        while line_idx < lines_count and y_cursor < self.inkyphat.HEIGHT:
            line = lines[line_idx]
            w, h = self.font.getsize(line)
            draw.text((0, y_cursor), line, self.color, self.font)
            y_cursor += h
            line_idx += 1

        if line_idx < lines_count:
            w, h = self.font.getsize(self.more_text_postfix)
            postfix_x = self.inkyphat.WIDTH - w
            postfix_y = self.inkyphat.HEIGHT - h

            draw.text((postfix_x, postfix_y),
                      self.more_text_postfix, self.color, self.font)

        self.inkyphat.set_image(self.img)
        self.inkyphat.show()
