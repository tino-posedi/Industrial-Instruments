import tkinter as tk
import math


class Analog180(tk.Canvas):
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
            width=260,
            height=145,
            bg="#D9D9D9",
            highlightthickness=0,
            **kwargs
        )

        self.width = 260
        self.height = 145
        self.center_x = self.width // 2
        self.center_y = self.height - 25

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

        self.angle_start = 180
        self.angle_end = 0

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

    def _value_to_angle(self, v):
        t = (v - self.min_value) / (self.max_value - self.min_value)
        return math.radians(self.angle_start + (self.angle_end - self.angle_start) * t)

    def redraw(self):
        self.delete("all")
        self._draw_outer_frame()
        self._draw_scale_background()
        self._draw_ticks()
        self._draw_numbers()
        self._draw_peak_indicator()
        self._draw_needle()
        self._draw_caption()

    def _draw_outer_frame(self):
        self.create_rectangle(0, 0, self.width - 1, self.height - 1, outline="#000")
        self.create_rectangle(1, 1, self.width - 2, self.height - 2, outline="#FFF")
        self.create_rectangle(2, 2, self.width - 3, self.height - 3, outline="#C0C0C0")
        self.create_rectangle(4, 4, self.width - 5, self.height - 5, outline="#000")

    def _draw_scale_background(self):
        cx, cy = self.center_x, self.center_y
        r = 75            
        thickness = 18

        box = (cx - r, cy - r, cx + r, cy + r)

        start = self.angle_start
        total = self.angle_end - self.angle_start

        def A(percent):
            return start + total * (percent / 100)

        self.create_arc(box, start=A(self.green_start),
                        extent=A(self.green_end) - A(self.green_start),
                        style="arc", outline="#00CC00", width=thickness)

        self.create_arc(box, start=A(self.yellow_start),
                        extent=A(self.yellow_end) - A(self.yellow_start),
                        style="arc", outline="#FFFF00", width=thickness)

        self.create_arc(box, start=A(self.red_start),
                        extent=A(self.red_end) - A(self.red_start),
                        style="arc", outline="#FF0000", width=thickness)

        outer_r = r + thickness / 2
        box2 = (cx - outer_r, cy - outer_r, cx + outer_r, cy + outer_r)
        self.create_arc(box2, start=start, extent=total, style="arc",
                        outline="#000", width=2)

    def _draw_ticks(self):
        cx, cy = self.center_x, self.center_y

        inner = 84        
        outer_major = 95   
        outer_minor = 92   

        step_major = (self.max_value - self.min_value) / 5
        for i in range(6):
            a = self._value_to_angle(self.min_value + i * step_major)
            x1 = cx + inner * math.cos(a)
            y1 = cy - inner * math.sin(a)
            x2 = cx + outer_major * math.cos(a)
            y2 = cy - outer_major * math.sin(a)
            self.create_line(x1, y1, x2, y2, width=2)

        step_minor = (self.max_value - self.min_value) / 10
        for i in range(1, 10, 2):
            a = self._value_to_angle(self.min_value + i * step_minor)
            x1 = cx + inner * math.cos(a)
            y1 = cy - inner * math.sin(a)
            x2 = cx + outer_minor * math.cos(a)
            y2 = cy - outer_minor * math.sin(a)
            self.create_line(x1, y1, x2, y2, width=1)

    def _draw_numbers(self):
        cx, cy = self.center_x, self.center_y
        r = 108        

        step = (self.max_value - self.min_value) / 5
        for i in range(6):
            a = self._value_to_angle(self.min_value + i * step)
            x = cx + r * math.cos(a)
            y = cy - r * math.sin(a)
            self.create_text(x, y, text=str(int(self.min_value + i * step)),
                             font=("Arial", 10, "normal"))

    def _draw_peak_indicator(self):
        cx, cy = self.center_x, self.center_y
        a = self._value_to_angle(self.peak_value)

        arc_r = 84          
        tip_r = arc_r
        base_r = arc_r + 9   
        half_angle = math.radians(5)

        tip_x = cx + tip_r * math.cos(a)
        tip_y = cy - tip_r * math.sin(a)

        b1_x = cx + base_r * math.cos(a + half_angle)
        b1_y = cy - base_r * math.sin(a + half_angle)
        b2_x = cx + base_r * math.cos(a - half_angle)
        b2_y = cy - base_r * math.sin(a - half_angle)

        self.create_polygon(tip_x, tip_y, b1_x, b1_y, b2_x, b2_y,
                            fill=self.peak_color, outline="black", width=1)

    def _draw_needle(self):
        a = self._value_to_angle(self.value)

        cx_arc, cy_arc = self.center_x, self.center_y
        arc_r = 84     

        tip_x = cx_arc + arc_r * math.cos(a)
        tip_y = cy_arc - arc_r * math.sin(a)

        cx = self.center_x
        cy = self.center_y - 10
        base_r = 8

        left = a + math.radians(90)
        right = a - math.radians(90)

        b1_x = cx + base_r * math.cos(left)
        b1_y = cy - base_r * math.sin(left)
        b2_x = cx + base_r * math.cos(right)
        b2_y = cy - base_r * math.sin(right)

        self.create_polygon(b1_x, b1_y, b2_x, b2_y, tip_x, tip_y,
                            fill=self.needle_color, outline="#003000")

        self.create_oval(cx - base_r, cy - base_r,
                         cx + base_r, cy + base_r,
                         fill="#303030", outline="#000")

    def _draw_caption(self):
        self.create_text(self.center_x, self.height - 13,
                         text=self.caption, font=("Arial", 9))

# -----------------------------------------------------
# DEMO
# -----------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Analog180 Demo")

    gauge = Analog180(
        root,
        needle_color="lime",
        peak_color="red",
        caption="SignalName1",

        start_value=0,
        end_value=100,
    )
    gauge.pack(padx=10, pady=10)

    def on_slider(val):
        gauge.set_value(float(val))

    slider = tk.Scale(root, from_=0, to=100,
                      orient="horizontal", length=300,
                      command=on_slider)
    slider.pack()

    root.mainloop()