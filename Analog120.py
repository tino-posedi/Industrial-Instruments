import tkinter as tk
import math


class Analog120(tk.Canvas):
    def __init__(
        self,
        master,
        needle_color="#008000",
        peak_color="#FF0000",
        caption="SignalName1",

        red_start=80,
        red_end=100,
        yellow_start=40,
        yellow_end=80,
        green_start=0,
        green_end=40,

        start_value=0,
        end_value=100,

        value=0,
        **kwargs
    ):
        super().__init__(
            master,
            width=253,
            height=145,
            bg="#D9D9D9",
            highlightthickness=0,
            **kwargs,
        )

        self.width = 253
        self.height = 145

        self.needle_color = needle_color
        self.peak_color = peak_color
        self.caption = caption

        self.red_start = red_start
        self.red_end = red_end
        self.yellow_start = yellow_start
        self.yellow_end = yellow_end
        self.green_start = green_start
        self.green_end = green_end

        self.min_value = start_value
        self.max_value = end_value

        self.value = value
        self.peak_value = value

        self.angle_start = 160
        self.angle_end = 20

        self.center_x = 126
        self.center_y = 135

        self.redraw()

    def set_value(self, v: float):
        v = max(self.min_value, min(self.max_value, v))
        self.value = v
        if v > self.peak_value:
            self.peak_value = v
        self.redraw()

    def reset_peak(self):
        self.peak_value = self.value
        self.redraw()

    def set_needle_color(self, c: str):
        self.needle_color = c
        self.redraw()

    def set_peak_color(self, c: str):
        self.peak_color = c
        self.redraw()

    def _value_to_angle(self, v):
        t = (v - self.min_value) / (self.max_value - self.min_value)
        return math.radians(self.angle_start + (self.angle_end - self.angle_start) * t)

    def _mouse(self, e):
        dx = e.x - self.center_x
        dy = self.center_y - e.y
        ang = math.degrees(math.atan2(dy, dx))

        a0 = self.angle_start
        a1 = self.angle_end

        if a1 > a0:
            a0, a1 = a1, a0

        ang = max(a1, min(a0, ang))

        t = (ang - self.angle_start) / (self.angle_end - self.angle_start)
        v = self.min_value + t * (self.max_value - self.min_value)
        self.set_value(v)

    def redraw(self):
        self.delete("all")
        self._draw_outer_frame()
        self._draw_inner_bezel()
        self._draw_scale_background()
        self._draw_ticks()
        self._draw_numbers()
        self._draw_peak_indicator()
        self._draw_needle()
        self._draw_label()

    def _draw_outer_frame(self):
        self.create_rectangle(0, 0, 252, 144, outline="#000")
        self.create_rectangle(1, 1, 251, 143, outline="#FFF")
        self.create_rectangle(2, 2, 250, 142, outline="#C0C0C0")
        self.create_rectangle(4, 4, 248, 140, outline="#000")

    def _draw_inner_bezel(self):
        cx, cy = self.center_x, self.center_y - 40
        r_outer = 90
        r_inner = 85

    def _draw_scale_background(self):
        cx, cy = self.center_x, self.center_y - 5
        r = 82
        thickness = 18

        box = (cx - r, cy - r, cx + r, cy + r)

        start = self.angle_start
        total = self.angle_end - self.angle_start

        def A(percent):
            return start + total * (percent / 100)

        self.create_arc(
            box, start=A(self.green_start), extent=A(self.green_end) - A(self.green_start),
            style="arc", outline="#00CC00", width=thickness
        )

        self.create_arc(
            box, start=A(self.yellow_start), extent=A(self.yellow_end) - A(self.yellow_start),
            style="arc", outline="#FFFF00", width=thickness
        )

        self.create_arc(
            box, start=A(self.red_start), extent=A(self.red_end) - A(self.red_start),
            style="arc", outline="#FF0000", width=thickness
        )

        outer_r = r + thickness / 2
        box_outer_border = (
            cx - outer_r, cy - outer_r,
            cx + outer_r, cy + outer_r
        )

        self.create_arc(
            box_outer_border,
            start=start,
            extent=total,
            style="arc",
            outline="#000000",
            width=2
        )

    def _draw_ticks(self):
        cx = self.center_x
        cy = self.center_y - 5

        inner = 91
        outer_major = 102
        outer_minor = 100

        step_major = (self.max_value - self.min_value) / 5
        for i in range(6):
            v = self.min_value + i * step_major
            a = self._value_to_angle(v)
            x1 = cx + inner * math.cos(a)
            y1 = cy - inner * math.sin(a)
            x2 = cx + outer_major * math.cos(a)
            y2 = cy - outer_major * math.sin(a)
            self.create_line(x1, y1, x2, y2, width=2)

        step_minor = (self.max_value - self.min_value) / 10
        for i in range(1, 10, 2):
            v = self.min_value + i * step_minor
            a = self._value_to_angle(v)
            x1 = cx + inner * math.cos(a)
            y1 = cy - inner * math.sin(a)
            x2 = cx + outer_minor * math.cos(a)
            y2 = cy - outer_minor * math.sin(a)
            self.create_line(x1, y1, x2, y2, width=1)

    def _draw_numbers(self):
        cx = self.center_x
        cy = self.center_y - 5

        r_numbers = 115

        step = (self.max_value - self.min_value) / 5

        for i in range(6):
            v = self.min_value + i * step
            a = self._value_to_angle(v)
            x = cx + r_numbers * math.cos(a)
            y = cy - r_numbers * math.sin(a)
            self.create_text(
                x, y,
                text=str(int(v)),
                font=("Arial", 10, "normal"),
                anchor="center"
            )

    def _draw_peak_indicator(self):
        a = self._value_to_angle(self.peak_value)

        cx = self.center_x
        cy = self.center_y - 5

        arc_r = 91

        tip_r = arc_r
        base_r = arc_r + 9
        half_width = math.radians(5)

        tip_x = cx + tip_r * math.cos(a)
        tip_y = cy - tip_r * math.sin(a)

        a_left = a + half_width
        a_right = a - half_width

        b1_x = cx + base_r * math.cos(a_left)
        b1_y = cy - base_r * math.sin(a_left)
        b2_x = cx + base_r * math.cos(a_right)
        b2_y = cy - base_r * math.sin(a_right)

        self.create_polygon(
            tip_x, tip_y, b1_x, b1_y, b2_x, b2_y,
            fill=self.peak_color,
            outline="black",
            width=1
        )

    def _draw_needle(self):
        a = self._value_to_angle(self.value)

        cx_arc = self.center_x
        cy_arc = self.center_y - 5
        arc_r = 91

        tip_x = cx_arc + arc_r * math.cos(a)
        tip_y = cy_arc - arc_r * math.sin(a)

        cx = self.center_x
        cy = self.center_y - 20
        base_r = 8

        left = a + math.radians(90)
        right = a - math.radians(90)

        b1_x = cx + base_r * math.cos(left)
        b1_y = cy - base_r * math.sin(left)
        b2_x = cx + base_r * math.cos(right)
        b2_y = cy - base_r * math.sin(right)

        self.create_polygon(
            b1_x, b1_y, b2_x, b2_y, tip_x, tip_y,
            fill=self.needle_color, outline="#003000"
        )

        self.create_oval(
            cx - base_r, cy - base_r,
            cx + base_r, cy + base_r,
            fill="#303030", outline="#000"
        )

    def _draw_label(self):
        self.create_text(126, 132, text=self.caption, font=("Arial", 9))


# -----------------------------------------------------
# DEMO
# -----------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Analog120 Demo")

    gauge = Analog120(
        root,
        needle_color="lime",
        peak_color="red",
        caption="SignalName1",

        start_value=0,
        end_value=100,

        red_start=80,
        red_end=100,
        yellow_start=40,
        yellow_end=80,
        green_start=0,
        green_end=40,
    )
    gauge.pack(padx=10, pady=10)

    def on_slider(value):
        gauge.set_value(float(value))

    slider = tk.Scale(
        root,
        from_=-50,
        to=150,
        orient="horizontal",
        length=300,
        label="Gauge Value",
        command=on_slider
    )
    slider.pack(padx=10, pady=10)

    gauge.set_value(0)
    slider.set(0)

    root.mainloop()
