#!/usr/bin/env python

# This draws a snazzy pseudo-3D graph where the z-axis is represented by the darkness of shading of the square.
# A lot of this code is copied from graph.py

import Image, ImageDraw, ImageFont
import math
import maths
import StringIO

class Graph3Dp:
    width = None
    height = None
    offset = None # (left, bottom, right, top)
    data = None
    line_colours = None
    grid_colour = None
    
    bound = None
    image = None
    draw = None
    colours = {
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "grey": (200, 200, 200)
    }
    bg_colour = None
    fg_colour = None
    x_maximum = None
    y_maxumim = None
    
    def __init__(self, data, size = (800, 600),    offset = (35, 20, 5, 5), font = False, bg_colour = colours["white"], fg_colour = colours["black"], line_colours = False, grid_colour = colours["grey"], tick_size = 5, labels = ([], [])):
        self.data = data
        self.width, self.height = size
        self.offset = offset
        self.bg_colour = bg_colour
        self.fg_colour = fg_colour
        self.line_colours = line_colours
        self.grid_colour = grid_colour
        self.tick_size = tick_size
        self.labels = labels
        if not font:
            self.font = ImageFont.truetype("DejaVuSansMono.ttf", 11)
        else:
            self.font = font
    
    def draw(self, format = "PNG"):
        width = self.width
        height = self.height
        offset = self.offset
        
        self.bound = (offset[0], height - offset[1], width - offset[2], offset[3])
        self.image = Image.new("RGBA", (width, height), self.bg_colour)
        self.draw = ImageDraw.Draw(self.image)

        self.x_axis()
        self.y_axis()
        self.plot_data()
        
        output = StringIO.StringIO()
        self.image.save(output, format)
        image_string = output.getvalue()
        output.close()
        
        return image_string
    
    def x_axis(self):
        draw = self.draw
        bound = self.bound
        fg_colour = self.fg_colour
        bg_colour = self.bg_colour
        font = self.font
        tick_size = self.tick_size
        labels = self.labels
        
        draw.line([(bound[0] - tick_size, bound[1]), (bound[2], bound[1])], fill = fg_colour)
        interval = (bound[2] - bound[0]) / float(len(labels[0]))
        self.x_interval = interval
        for i, label in enumerate(labels[0]):
            draw.line([
                ((i + 1) * interval + bound[0], bound[1]),
                ((i + 1) * interval + bound[0], bound[1] + tick_size)
            ], fill = fg_colour)
            if not (i == 0) or True:
                draw.line([
                    ((i + 1) * interval + bound[0], bound[3]),
                    ((i + 1) * interval + bound[0], bound[1] - 1)
                ], fill = self.grid_colour)
            font_offset = interval/2.0 - font.getsize(label)[0]/2.0
            draw.text(
                (i * interval + bound[0] + font_offset, bound[1] + tick_size + 2),
                label,
                fill = fg_colour,
                font = font
            )
    
    def y_axis(self):
        draw = self.draw
        bound = self.bound
        fg_colour = self.fg_colour
        bg_colour = self.bg_colour
        font = self.font
        tick_size = self.tick_size
        labels = self.labels
        
        draw.line([(bound[0], bound[1] + tick_size), (bound[0], bound[3])], fill = fg_colour)
        interval = (bound[3] - bound[1]) / float(len(labels[1]))
        self.y_interval = interval
        y_labels = labels[1][:]
        y_labels.reverse()
        for i, label in enumerate(y_labels):
            draw.line([
                (bound[0] - tick_size, (i + 1) * interval + bound[1]),
                (bound[0], (i + 1) * interval + bound[1])
            ], fill = fg_colour)
            if not (i == 0) or True:
                draw.line([
                    (bound[0] + 1, (i + 1) * interval + bound[1]),
                    (bound[2], (i + 1) * interval + bound[1])
                ], fill = self.grid_colour)
            x_font_pos = bound[0] - tick_size - 2 - font.getsize(label)[0]
            y_font_pos = bound[1] - (i * interval) - font.getsize(label)[1]/2.0 
            y_font_pos = bound[1] + (i * interval) + interval/2.0 - font.getsize(label)[1]/2.0
            draw.text(
                (x_font_pos, y_font_pos),
                label,
                fill = fg_colour,
                font = font
            )
    
    def plot_data(self):
        draw = self.draw
        bound = self.bound
        fg_colour = self.fg_colour
        bg_colour = self.bg_colour
        data = self.data
        x_interval = self.x_interval
        y_interval = self.y_interval
        
        maximum = maths.max_r(data)
        max_float = float(maximum)
        data_reversed = data[:]
        data_reversed.reverse()
        
        for i, row in enumerate(data_reversed):
            for j, cell_tuple in enumerate(row):
                length = len(cell_tuple)
                width = (x_interval - 2)/length
                for k, cell in enumerate(cell_tuple):
                    bl = (
                        j * x_interval + 1 + bound[0] + k * width,
                        bound[1] + (i * y_interval) - 1
                    )
                    tr = (
                        bl[0] + width - 2,
                        bl[1] + y_interval + 2
                    )
                    if k == length - 1:
                        filler = x_interval - width
                        tr = (tr[0] + filler, tr[1])
                    
                    proportion = cell / max_float
                    shade = 255 - int(255.0 * proportion)
                    colour = (shade,) * 3
                    
                    draw.rectangle([bl, tr], fill = colour)
