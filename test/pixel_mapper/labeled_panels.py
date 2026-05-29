import os

from samples.samplebase import SampleBase

from RGBMatrixEmulator import graphics

FONT_PATH = os.path.abspath(
    os.path.join(__file__, "..", "..", "..", "samples", "fonts", "6x9.bdf")
)

BORDER_COLOR = graphics.Color(255, 0, 0)
LABEL_COLOR = graphics.Color(255, 255, 255)


class LabeledPanels(SampleBase):
    """
    Draws the panel grid as the program sees it: the drawn buffer is divided
    into cols x rows cells, and each cell gets a red border plus a
    "<parallel #>.<panel #>" label. Rendered once through whatever pixel mapper
    is configured so the resulting screenshot shows how the mapper arranges or
    transforms the matrix.
    """

    def run(self):
        canvas = self.matrix.CreateFrameCanvas()

        cols = self.args.led_cols
        rows = self.args.led_rows
        panel_rows = canvas.height // rows
        panel_cols = canvas.width // cols

        font = graphics.Font()
        font.LoadFont(FONT_PATH)

        for parallel in range(panel_rows):
            for panel in range(panel_cols):
                x0 = panel * cols
                y0 = parallel * rows
                x1 = x0 + cols - 1
                y1 = y0 + rows - 1

                graphics.DrawLine(canvas, x0, y0, x1, y0, BORDER_COLOR)
                graphics.DrawLine(canvas, x0, y1, x1, y1, BORDER_COLOR)
                graphics.DrawLine(canvas, x0, y0, x0, y1, BORDER_COLOR)
                graphics.DrawLine(canvas, x1, y0, x1, y1, BORDER_COLOR)

                graphics.DrawText(
                    canvas,
                    font,
                    x0 + 2,
                    y0 + font.baseline + 1,
                    LABEL_COLOR,
                    f"{parallel}.{panel}",
                )

        self.matrix.SwapOnVSync(canvas)
