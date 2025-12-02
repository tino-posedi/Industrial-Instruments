import tkinter as tk

class HorizontalMeter(tk.Canvas):
    def __init__(
        self,
        master,
        value=50,
        unit="%",
        caption="SignalName1",
        red_start=60, red_end=100,
        yellow_start=0, yellow_end=40,
        green_start=40, green_end=60,
        **kwargs
    ):
        super().__init__(
            master,
            width=320,
            height=110,
            bg="#D9D9D9",
            highlightthickness=0,
            **kwargs
        )

        self.min_value = 0
        self.max_value = 100
        self.value = value
        self.unit = unit
        self.caption = caption

        self.red_start = red_start
        self.red_end = red_end
        self.yellow_start = yellow_start
        self.yellow_end = yellow_end
        self.green_start = green_start
        self.green_end = green_end

        self.scale_left = 25
        self.scale_right = 290
        self.scale_width = self.scale_right - self.scale_left

        self.bar_top = 45
        self.bar_bottom = 30

        self.tick_bottom = 75

        self.bind("<Button-1>", self._mouse)
        self.bind("<B1-Motion>", self._mouse)

        self.redraw()

    def _value_to_x(self, v):
        t = (v - self.min_value) / (self.max_value - self.min_value)
        return self.scale_left + t * self.scale_width

    def _x_to_value(self, x):
        t = (x - self.scale_left) / self.scale_width
        return max(self.min_value, min(self.max_value, t * 100))

    def set_value(self, v):
        self.value = max(self.min_value, min(self.max_value, v))
        self.redraw()

    def _mouse(self, e):
        self.set_value(self._x_to_value(e.x))

    def redraw(self):
        self.delete("all")
        self._draw_outer_frame()
        self._draw_color_bar()
        self._draw_ticks()
        self._draw_triangle()
        self._draw_caption()

    def _draw_outer_frame(self):
        self.create_rectangle(0, 0, 319, 109, outline="#000")
        self.create_rectangle(1, 1, 318, 108, outline="#FFF")
        self.create_rectangle(2, 2, 317, 107, outline="#A0A0A0")
        self.create_rectangle(3, 3, 316, 106, outline="#000")


    def _draw_color_bar(self):
        T = self.bar_top
        B = self.bar_bottom

        x_red_start = self._value_to_x(self.red_start)
        x_red_end = self._value_to_x(self.red_end)

        x_yellow_start = self._value_to_x(self.yellow_start)
        x_yellow_end = self._value_to_x(self.yellow_end)

        x_green_start = self._value_to_x(self.green_start)
        x_green_end = self._value_to_x(self.green_end)

        self.create_rectangle(x_red_start, T, x_red_end, B,
                              fill="#FF0000", outline="black")
        self.create_rectangle(x_green_start, T, x_green_end, B,
                              fill="#00A000", outline="black")
        self.create_rectangle(x_yellow_start, T, x_yellow_end, B,
                              fill="#FFFF00", outline="black")

    def _draw_ticks(self):
        T = self.bar_top 
        B = self.bar_bottom + 15

        major_len = 25
        minor_len = 15

        majors = list(range(0, 120, 20))

        self.create_line(self.scale_left, B, self.scale_right, B,
                         width=2, fill="black")

        for v in majors:
            if v > 100:
                continue

            x = self._value_to_x(v)
            self.create_line(x, B, x, B - major_len, width=2, fill="black")
            self.create_text(x, B + major_len - 5,
                             text=str(v), font=("Arial", 10))

            minor_v = v + 10
            if minor_v < 100:
                xm = self._value_to_x(minor_v)
                self.create_line(xm, B, xm, B-+ minor_len,
                                 width=1, fill="black")

    def _draw_triangle(self):
        x = self._value_to_x(self.value)
        tri_y = self.bar_top - 8

        pts = [
            x, tri_y,
            x - 8, tri_y + 16,
            x + 8, tri_y + 16
        ]

        self.create_polygon(pts, fill="lime", outline="black")

    def _draw_caption(self):
        self.create_text(160, 90, text=self.caption, font=("Arial", 9))


# -----------------------------------------------------
# DEMO
# -----------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    s = HorizontalMeter(root, value=50, unit="%")
    s.pack(padx=10, pady=10)
    root.mainloop()
