import os
import tkinter
import turtle

from RGBMatrixEmulator.adapters.base import BaseAdapter
from RGBMatrixEmulator.graphics.color import Color
from RGBMatrixEmulator.logger import Logger


class TurtleAdapter(BaseAdapter):
    def __init__(self, width, height, options):
        super().__init__(width, height, options)
        self.__pen = None
        self.__screen = None

    def draw_to_screen(self, pixels):
        self.__pen.clear()

        for row, pixel_row in enumerate(pixels):
            self.__move_pen_to_row_start(row)

            for _col, pixel in enumerate(pixel_row):
                self.__draw_pixel(pixel)
                self.__move_pen_next_pixel()

        self.__screen.update()

    def load_emulator_window(self):
        if self.loaded:
            return

        Logger.info("Loading {}".format(self.emulator_details_text()))
        turtle.setup(*self.options.window_size())
        turtle.title(self.emulator_details_text())
        self.__pen = turtle.Turtle(visible=False)
        self.__screen = self.__pen.getscreen()
        self.__set_emulator_icon()
        self.__screen.bgcolor(Color.BLACK())
        turtle.tracer(0, 0)
        turtle.colormode(255)

        self.loaded = True

    def __draw_pixel(self, pixel):
        self.__pen.color(*pixel)
        self.__pen.begin_fill()

        if self.options.pixel_style == "circle":
            self.__draw_circle_pixel()
        else:
            self.__draw_square_pixel()

        self.__pen.end_fill()

        self.__pen.setheading(0)

    def __draw_square_pixel(self):
        for _ in range(0, 4):
            self.__pen.forward(self.options.pixel_size)
            self.__pen.left(90)

    def __draw_circle_pixel(self):
        self.__pen.pendown()
        self.__pen.dot(self.options.pixel_size)
        self.__pen.penup()

        # Apparently dots cannot overlap, so set movement to the smallest increment possible
        self.__pen.forward(1)

    def __move_pen_next_pixel(self):
        self.__pen.penup()
        self.__pen.forward(self.options.pixel_size)
        self.__pen.pendown()

    def __move_pen_to_row_start(self, row_number):
        self.__reset_pen_position()
        self.__pen.penup()
        self.__pen.setheading(270)
        self.__pen.forward(self.options.pixel_size * row_number)
        self.__pen.setheading(0)
        self.__pen.pendown()

    def __reset_pen_position(self):
        self.__pen.penup()
        self.__pen.goto(
            self.options.pixel_size / 2 - self.__screen.window_width() / 2,
            self.__screen.window_height() / 2 - self.options.pixel_size / 2,
        )
        self.__pen.pendown()

    def __set_emulator_icon(self):
        emulator_path = os.path.abspath(os.path.dirname(__file__))
        raw_icon_path = os.path.join(emulator_path, "..", "icon.png")
        icon_path = os.path.normpath(raw_icon_path)

        icon_image = tkinter.Image("photo", file=icon_path)
        self.__screen._root.iconphoto(True, icon_image)
