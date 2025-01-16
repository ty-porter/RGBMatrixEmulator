import tkinter
import os

from RGBMatrixEmulator.adapters.base import BaseAdapter
from RGBMatrixEmulator.graphics import Color
from RGBMatrixEmulator.logger import Logger


class TkinterAdapter(BaseAdapter):
    SUPPORTS_ALTERNATE_PIXEL_STYLE = True

    def __init__(self, width, height, options):
        super().__init__(width, height, options)
        self.__root = None
        self.__canvas = None
        self.__pixels = None

    def load_emulator_window(self):
        if self.loaded:
            return

        Logger.info("Loading {}".format(self.emulator_details_text()))
        self.__root = tkinter.Tk()
        self.__set_emulator_icon()
        self.__root.title(self.emulator_details_text())

        window_size = self.options.window_size()
        self.__root.geometry("{}x{}".format(*window_size))
        self.__canvas = tkinter.Canvas(
            self.__root,
            width=window_size[0],
            height=window_size[1],
            bd=0,
            highlightthickness=0,
            bg="black",
        )

        self.__initialize_bitmap()
        self.__root.update()

        self.loaded = True

    def draw_to_screen(self, pixels):
        for row, pixel_row in enumerate(pixels):
            for col, pixel in enumerate(pixel_row):
                shape_id = self.__pixels[row][col]

                self.__canvas.itemconfig(shape_id, fill=Color.to_hex(pixel))

        self.__canvas.pack()
        self.__root.update()

    def __initialize_bitmap(self):
        self.__pixels = []

        for row in range(0, self.height):
            new_row = []

            for col in range(0, self.width):
                coords = self.__pixel_dimensions(col, row)

                if self.options.pixel_style == "circle":
                    id = self.__canvas.create_oval(coords, width=0)
                else:
                    id = self.__canvas.create_rectangle(coords, width=0)

                new_row.append(id)

            self.__pixels.append(new_row)

    def __pixel_dimensions(self, col, row):
        size = self.options.pixel_size
        start, stop = (col * size, row * size)

        return (start, stop, start + size, stop + size)

    def __set_emulator_icon(self):
        emulator_path = os.path.abspath(os.path.dirname(__file__))
        raw_icon_path = os.path.join(emulator_path, "..", "icon.png")
        icon_path = os.path.normpath(raw_icon_path)

        icon = tkinter.PhotoImage(file=icon_path)
        self.__root.tk.call("wm", "iconphoto", self.__root._w, icon)
