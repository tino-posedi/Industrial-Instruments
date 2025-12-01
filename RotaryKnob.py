import tkinter as tk
import math

class RotaryKnob(tk.Canvas):
    def __init__(
        self,
        master,
        value=10,
        unit="%",
        caption="SignalName1",
        caption2="SignalName2",
        min_value=0,
        max_value=100,
        **kwargs
    ):
        super().__init__(
            master,
            width=150,
            height=220,
            bg="#D9D9D9",
            highlightthickness=0,
            **kwargs
        )

        self.value = value
        self.unit = unit
        self.caption = caption
        self.caption2 = caption2
        self.min_value = min_value
        self.max_value = max_value

        self.knob_center = (75, 115)
        self.knob_radius = 35

        self.last_angle = self.value_to_angle(value)

        self.bind("<Button-1>", self._mouse_down)
        self.bind("<B1-Motion>", self._mouse_drag)

        self.redraw()

    def value_to_angle(self, v):
        t = (v - self.min_value) / (self.max_value - self.min_value)
        return -140 + t * 280

    def angle_to_value(self, ang):
        ang = max(-140, min(140, ang))
        t = (ang + 140) / 280
        return self.min_value + t * (self.max_value - self.min_value)

    def _mouse_down(self, e):
        self._mouse_drag(e)

    def _mouse_drag(self, e):
        cx, cy = self.knob_center
        dx = e.x - cx
        dy = e.y - cy

        ang = math.degrees(math.atan2(dx, -dy))

        ang = max(-140, min(140, ang))

        self.value = self.angle_to_value(ang)
        self.last_angle = ang

        self.redraw()

    def redraw(self):
        self.delete("all")
        self._draw_outer_frame()
        self._draw_display()
        self._draw_knob()
        self._draw_captions()

    def _draw_outer_frame(self):
        self.create_rectangle(0, 0, 149, 219, outline="#000")
        self.create_rectangle(1, 1, 148, 218, outline="#FFF")
        self.create_rectangle(2, 2, 147, 217, outline="#A0A0A0")
        self.create_rectangle(3, 3, 146, 216, outline="#000")

    def _draw_display(self):
        box = (25, 10, 125, 45)  

        self.create_rectangle(*box, fill="#303030", outline="#000")

        self.create_rectangle(
            box[0] + 2, box[1] + 2,
            box[2] - 2, box[3] - 2,
            fill="black", outline="#606060"
        )

        text = f"{self.value:0.1f} {self.unit}"

        cx = (box[0] + box[2]) / 2
        cy = (box[1] + box[3]) / 2

        self.create_text(
            cx, cy,
            text=text,
            anchor="center",
            font=("Arial", 16, "bold"),
            fill="#00FF00"
        )


    def _draw_knob(self):
        cx, cy = self.knob_center
        r = self.knob_radius

        self.create_oval(cx-r, cy-r, cx+r, cy+r,
                         fill="#D0D0D0", outline="#808080", width=2)

        self.create_arc(cx-r, cy-r, cx+r, cy+r,
                        start=45, extent=180,
                        style="arc", outline="#FFFFFF", width=2)

        major_vals = (0, 20, 40, 60, 80, 100)

        for val in major_vals:
            ang = self.value_to_angle(val)
            rad = math.radians(ang)

            x1 = cx + math.sin(rad) * (r + 2)
            y1 = cy - math.cos(rad) * (r + 2)

            x2 = cx + math.sin(rad) * (r + 12)
            y2 = cy - math.cos(rad) * (r + 12)

            self.create_line(x1, y1, x2, y2, width=2)

            xt = cx + math.sin(rad) * (r + 26)
            yt = cy - math.cos(rad) * (r + 26)
            self.create_text(xt, yt, text=str(val), font=("Arial", 10))

        for val in (10, 30, 50, 70, 90):
            ang = self.value_to_angle(val)
            rad = math.radians(ang)

            x1 = cx + math.sin(rad) * (r + 2)
            y1 = cy - math.cos(rad) * (r + 2)

            x2 = cx + math.sin(rad) * (r + 7)
            y2 = cy - math.cos(rad) * (r + 7)

            self.create_line(x1, y1, x2, y2, width=1)

        ang = self.value_to_angle(self.value)
        rad = math.radians(ang)

        x = cx + math.sin(rad) * (r - 12)
        y = cy - math.cos(rad) * (r - 12)

        self.create_oval(x-3, y-3, x+3, y+3,
                         fill="lime", outline="black")

    def _draw_captions(self):
        self.create_text(
            75, 195,
            text=self.caption,
            font=("Arial", 11)
        )


# ----------------------------------------------------------
# DEMO
# ----------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    knob = RotaryKnob(root, value=10, unit="%", caption="SignalName1")
    knob.pack(padx=10, pady=10)
    root.mainloop()
