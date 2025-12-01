import tkinter as tk

class VerticalMeter(tk.Canvas):
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
            width=110,
            height=320,
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

        self.scale_top = 55
        self.scale_bottom = 290
        self.scale_height = self.scale_bottom - self.scale_top

        self.bar_left = 25
        self.bar_right = 40

        self.tick_right = 75

        self.bind("<Button-1>", self._mouse)
        self.bind("<B1-Motion>", self._mouse)

        self.redraw()

    def _value_to_y(self, v):
        t = (v - self.min_value) / (self.max_value - self.min_value)
        return self.scale_bottom - t * self.scale_height

    def _y_to_value(self, y):
        t = (self.scale_bottom - y) / self.scale_height
        return max(self.min_value, min(self.max_value, t * 100))

    def set_value(self, v):
        self.value = max(self.min_value, min(self.max_value, v))
        self.redraw()

    def _mouse(self, e):
        self.set_value(self._y_to_value(e.y))

    def redraw(self):
        self.delete("all")

        self._draw_outer_frame()
        self._draw_display()
        self._draw_color_bar()
        self._draw_ticks_on_bar()
        self._draw_triangle_indicator()
        self._draw_caption()

    def _draw_outer_frame(self):
        self.create_rectangle(0, 0, 109, 319, outline="#000")
        self.create_rectangle(1, 1, 108, 318, outline="#FFF")
        self.create_rectangle(2, 2, 107, 317, outline="#A0A0A0")
        self.create_rectangle(3, 3, 106, 316, outline="#000")

    def _draw_display(self):
        box = (10, 10, 100, 40)

        self.create_rectangle(*box, fill="#303030", outline="#000")
        self.create_rectangle(
            box[0] + 2, box[1] + 2,
            box[2] - 2, box[3] - 2,
            fill="black", outline="#606060"
        )

        text = f"{self.value:0.1f} {self.unit}"

        self.create_text(
            (box[0] + box[2]) // 2,
            (box[1] + box[3]) // 2,
            text=text,
            font=("Arial", 14, "bold"),
            fill="#00FF00"
        )

    def _draw_color_bar(self):
        L = self.bar_left
        R = self.bar_right

        y_red_start = self._value_to_y(self.red_start)
        y_red_end = self._value_to_y(self.red_end)

        y_yellow_start = self._value_to_y(self.yellow_start)
        y_yellow_end = self._value_to_y(self.yellow_end)

        y_green_start = self._value_to_y(self.green_start)
        y_green_end = self._value_to_y(self.green_end)

        self.create_rectangle(L, y_red_end, R, y_red_start,
                              fill="#FF0000", outline="black")

        self.create_rectangle(L, y_green_end, R, y_green_start,
                              fill="#00A000", outline="black")

        self.create_rectangle(L, y_yellow_end, R, y_yellow_start,
                              fill="#FFFF00", outline="black")

    def _draw_ticks_on_bar(self):
        L = self.bar_left
        tick_major_to = self.tick_right - 20
        tick_minor_to = self.tick_right - 34

        self.create_line(L, self.scale_top, L, self.scale_bottom,
                         width=2, fill="black")

        majors = list(range(0, 120, 20))

        for v in majors:
            if v > 100:
                continue

            y = self._value_to_y(v)
            self.create_line(L, y, tick_major_to, y, width=2, fill="black")

            self.create_text(tick_major_to + 5, y,
                             text=str(v),
                             font=("Arial", 10),
                             anchor="w")

            minor_v = v + 10
            if minor_v < 100:
                y_minor = self._value_to_y(minor_v)
                self.create_line(L, y_minor, tick_minor_to, y_minor,
                                 width=1, fill="black")

    def _draw_triangle_indicator(self):
        y = self._value_to_y(self.value)
        tri_x = self.tick_right - 40

        pts = [
            tri_x, y,
            tri_x - 16, y - 8,
            tri_x - 16, y + 8
        ]

        self.create_polygon(pts, fill="lime", outline="black")

    def _draw_caption(self):
        self.create_text(55, 305, text=self.caption, font=("Arial", 9))

# -----------------------------------------------------
# DEMO
# -----------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    s = VerticalMeter(
        root,
        value=50,
        unit="%"
    )
    s.pack(padx=10, pady=10)
    root.mainloop()
