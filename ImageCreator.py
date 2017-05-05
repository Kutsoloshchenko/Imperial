from PIL import Image, ImageDraw, ImageFont
import os


class QuoteCreator:
    @staticmethod
    def _getFont(font_size):
        return ImageFont.truetype(os.path.join('Impact.ttf'), font_size)

    @staticmethod
    def _createline(line):
        return ''.join('%s ' % i for i in line).rstrip()

    @staticmethod
    def _prepearimage():
        img = Image.open(os.path.join('.//temp.gif'))
        return img

    def _name_preparation(self, text):
        if len(text) < 30:
            font_size = 36
        elif len(text) <60:
            font_size = 24
        else:
            font_size = 18
        return self._getFont(font_size)

    def _textconversion(self, text):
        if len(text) < 150:
            font_size = 36
            max = 30
            ychange = 40
        elif len(text) <400:
            font_size = 24
            max = 50
            ychange = 30
        else:
            font_size = 18
            max = 75
            ychange = 25

        font = self._getFont(font_size)

        words = text.split()

        words[0] = '"%s' % words[0]

        words[-1] = '%s"' % words[-1]

        current_line = 0
        line = []
        all_lines = []

        for word in words:
            if (current_line + len(word)) <= max:
                line.append(word)
                current_line += len(word)
            else:
                all_lines.append(line)
                line = []
                current_line = 0

                line.append(word)
                current_line += len(word)

        all_lines.append(line)

        all_lines = [self._createline(i) for i in all_lines]

        return font, all_lines, ychange

    def createquote(self, author, text):

        if len(text) >= 1500:
            return u"Сокращай, мудила"
        elif len(author) >= 65:
            author = author[:50] + '...'

        img = Image.new("RGB", (1280, 720))
        font, text, ychange = self._textconversion(text.lower())
        draw = ImageDraw.Draw(img)
        size = img.size
        size = (size[0]//2 - 40, size[1]//4 - 25)

        y = 0

        for line in text:
            draw.text((size[0], size[1]+y), line, (255,255,255), font=font)
            y +=ychange

        author_image = self._prepearimage()
        img.paste(author_image, (img.size[0]//20, img.size[1]//5))
        author = "(c)%s" % author
        font = self._name_preparation(author)
        draw.text((img.size[0]*6//10, img.size[1]*9//10), author, (255,255,255), font=font)

        draw = ImageDraw.Draw(img)
        os.system('rm temp.gif')
        img.save("temp.gif")

if __name__ == "__main__":
    h = QuoteCreator()
    h.createquote()