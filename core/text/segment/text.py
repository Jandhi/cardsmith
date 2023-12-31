from core.color import Color, RGBA, color
from core.geometry import Point
from core.text.tag import Tag
from core.text.fonts import get_font
from PIL import ImageDraw, ImageFont, Image
from core.text.segment.line import LineSegment
from core.alignment import YAlignment

class TextSegment(LineSegment):
    content : str
    tags : list[Tag]
    font : str
    font_size : int
    fill : RGBA

    def __init__(self, content : str, font : str, font_size : int, fill : Color, tags : list[Tag]) -> None:
        self.content = content
        self.tags = tags
        self.font = font
        self.font_size = font_size
        self.fill = fill
        self.apply_tags()
        self.size = self.calculate_size()

    def apply_tags(self):
        for tag in self.tags:
            if tag.name == 'font':
                self.font = tag.data
            if tag.name == 'size':
                self.font_size = int(tag.data)
            if tag.name == 'color' or tag.name == 'fill':
                self.fill = color(tag.data)

    def get_font(self):
        return get_font(self.font, self.font_size, self.tags)

    def __repr__(self) -> str:
        content = self.content
        prefix = ''
        suffix = ''

        for tag in self.tags:
            prefix += tag.opening_repr()
            suffix += tag.closing_repr()

        return f'{prefix}{content}{suffix}'

    def draw(self, coords : Point, line_size : Point, image : Image.Image, alignment : YAlignment):
        draw = ImageDraw.Draw(image)
        font = self.get_font()
        draw.fontmode = "L"

        if alignment == YAlignment.TOP:
            y_offset = self.height()
        elif alignment == YAlignment.MIDDLE:
            y_offset = (line_size.y - self.height()) / 2
        elif alignment == YAlignment.BOTTOM:
            y_offset = line_size.y - self.height()

        my_coords = coords + Point.y_span(y_offset)

        draw.text(
            xy=my_coords.to(my_coords + (1000, 1000)).int_tuple(),
            text=self.content,
            font=font,
            fill=self.fill.tuple(),
        )

    def height(self) -> int:
        font = self.get_font()
        x1, y1, x2, y2 = font.getbbox('ABCDEFGHIJKLMNOPRSTUVWXYZ1234567890abcdefhiklmnorstuvwxz')
        return (y2 - y1)

    def calculate_size(self) -> Point:
        font = self.get_font()
        x1, y1, x2, y2 = font.getbbox(self.content)
        return Point(x2 - x1, self.height())