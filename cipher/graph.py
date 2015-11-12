#!/usr/bin/env python

# This draws pretty graphs of arbitrary data.

import Image, ImageDraw, ImageFont
import math
import maths
import StringIO

class Graph:
    percentages = None
    width = None
    height = None
    offset = None # (left, bottom, right, top)
    tick_size = None
    data = None
    line_colours = None
    grid = None
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
    default_line_colours = [
        (255, 0, 0),
        (0, 0, 255),
        (0, 255, 0),
        (255, 255, 0),
        (255, 0, 255),
        (0, 255, 255)
    ]
    bg_colour = None
    fg_colour = None
    x_maximum = None
    y_maxumim = None
    
    # These options are fairly self-explanatory: offset means the margin between the actual graph and the edge of the image, not including labels.
    def __init__(self, data, size = (800, 600),    offset = (35, 20, 5, 5), tick_size = 5, labels = False, percentages = False, font = False, bg_colour = colours["white"], fg_colour = colours["black"], line_colours = False, grid = False, grid_colour = colours["grey"]):
        self.data = data
        self.width, self.height = size
        self.offset = offset
        self.tick_size = tick_size
        self.labels = labels
        self.percentages = percentages
        self.bg_colour = bg_colour
        self.fg_colour = fg_colour
        self.line_colours = line_colours
        self.grid = grid
        self.grid_colour = grid_colour
        if not font:
            self.font = ImageFont.truetype("DejaVuSansMono.ttf", 11)
        else:
            self.font = font
    
    def draw(self, format = "PNG"):
        width = self.width
        height = self.height
        offset = self.offset
        
        # These are the pixel locations for the corners of the graph
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
    
    # This calculates how big (in terms of the data) the distance between each tick on the axes should be. If we had a range from 0-20000, we wouldn't want an interval of 2!
    def calculate_interval(self, data, index_range, length, maximum = None):
        maximum = float(maths.range_tuples(data, index_range)[0])
        if maximum == 0:
            maximum = 1
        steps = [1, 2, 5]
        multiplier = 1
        interval = length
        done = False
        final_step = None
        while not done:
            for step in steps:
                interval = length / (maximum / step)
                if interval > 15:
                    final_step = step
                    done = True
                    break
            for i, j in enumerate(steps[:]):
                steps[i] = j * 10
        return (maximum, interval, final_step)

    def x_axis(self):
        draw = self.draw
        bound = self.bound
        fg_colour = self.fg_colour
        bg_colour = self.bg_colour
        data = self.data
        font = self.font
        tick_size = self.tick_size
        
        draw.line([(bound[0], bound[1]), (bound[2], bound[1])], fill = fg_colour)
        if self.labels:
            interval = (bound[2] - bound[0]) / (len(data) - 1.0)
            self.x_interval = interval
            for i, data_tuple in enumerate(data):
                label = data_tuple[0]
                draw.line([
                    (i * interval + bound[0], bound[1]),
                    (i * interval + bound[0], bound[1] + tick_size)
                ], fill = fg_colour)
                if self.grid and not (i == 0):
                    draw.line([
                        (i * interval + bound[0], bound[3]),
                        (i * interval + bound[0], bound[1] - 1)
                    ], fill = self.grid_colour)
                font_offset = font.getsize(label)[0]/2.0
                draw.text(
                    (i * interval + bound[0] - font_offset, bound[1] + tick_size + 2),
                    label,
                    fill = fg_colour,
                    font = font
                )
        else:
            (maximum, interval, step) = self.calculate_interval(data, (0, 1), bound[2] - bound[0])
            self.x_step = step
            self.x_interval = interval
            self.x_maximum = maximum
            for i in range(int(maximum/step) + 1):
                draw.line([
                    (i * interval + bound[0], bound[1]),
                    (i * interval + bound[0], bound[1] + tick_size)
                ], fill = fg_colour)
                if self.grid and not (i == 0):
                    draw.line([
                        (i * interval + bound[0], bound[3]),
                        (i * interval + bound[0], bound[1] - 1)
                    ], fill = self.grid_colour)
                label = str(i * step)
                x_font_pos = i * interval + bound[0] - font.getsize(label)[0]/2.0
                y_font_pos = bound[1] + tick_size + 2
                draw.text(
                    (x_font_pos, y_font_pos),
                    label,
                    fill = fg_colour,
                    font = font
                )
    
    def y_axis(self):
        draw = self.draw
        bound = self.bound
        fg_colour = self.fg_colour
        bg_colour = self.bg_colour
        data = self.data
        font = self.font
        tick_size = self.tick_size
        
        draw.line([(bound[0], bound[1]), (bound[0], bound[3])], fill = fg_colour)
        
        (maximum, interval, step) = self.calculate_interval(data, (1, len(data[0])), bound[1] - bound[3])
        self.y_step = step
        self.y_interval = interval
        self.y_maximum = maximum
        for i in range(int(maximum/step) + 1):
            draw.line([
                (bound[0] - tick_size, bound[1] - (i * interval)),
                (bound[0], bound[1] - (i * interval))
            ], fill = fg_colour)
            if self.grid and not (i == 0):
                draw.line([
                    (bound[0] + 1, bound[1] - (i * interval)),
                    (bound[2], bound[1] - (i * interval))
                ], fill = self.grid_colour)
            if self.percentages:
                label = str(i * step) + '%'
            else:
                label = str(i * step)
            x_font_pos = bound[0] - tick_size - 2 - font.getsize(label)[0]
            y_font_pos = bound[1] - (i * interval) - font.getsize(label)[1]/2.0
            draw.text(
                (x_font_pos, y_font_pos),
                label,
                fill = fg_colour,
                font = font
            )
    
    def plot_data(self):
        data = self.data
        bound = self.bound
        draw = self.draw
        line_colours = self.line_colours
        
        points = [[] for i in data[0][1:]]
        
        for i, data_tuple in enumerate(data):
            if self.labels:
                maximum = self.y_maximum
                x = i * self.x_interval + bound[0]
                for index, value in enumerate(data_tuple[1:]):
                    y = bound[1] - ((value / maximum) * (bound[1] - bound[3]))
                    points[index].append((x, y))
            else:
                x_value = data_tuple[0]
                x_maximum = self.x_maximum
                y_maximum = self.y_maximum
                x = ((x_value / x_maximum) * (bound[2] - bound[0])) + bound[0]
                for index, y_value in enumerate(data_tuple[1:]):
                    y = bound[1] - ((y_value / y_maximum) * (bound[1] - bound[3]))
                    points[index].append((x, y))
        for i, line in enumerate(points):
            if not line_colours:
                colour = self.default_line_colours[i % len(self.default_line_colours)]
            else:
                colour = line_colours[i]
            draw.line(line, fill = colour)
