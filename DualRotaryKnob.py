import tkinter as tk
import math


class DualRotaryKnob(tk.Canvas):
    def __init__(
        self,
        master,
        width=200,
        height=250,
        min_value=0,
        max_value=100,
        coarse_value=0,
        fine_value=0,
        text_color="#00FF00",
        dot_color="#00FF00",
        needle_color="#00AA00",
        caption="SignalName1",
        **kwargs
    ):
        super().__init__(
            master,
            width=width,
            height=height,
            bg="#D9D9D9",
            highlightthickness=0,
            **kwargs
        )

        self.w = width
        self.h = height

        self.min_value = min_value
        self.max_value = max_value
        self.coarse = coarse_value
        self.fine = fine_value

        self.text_color = text_color
        self.dot_color = dot_color
        self.needle_color = needle_color
        self.caption = caption

        self.cx = self.w // 2
        self.cy = self.h // 2 + 20

        self.angle_start = 225
        self.angle_end = -45
        
        self._last_fine_angle = None

        # knobs
        self.big_r = 50      # smaller than before
        self.small_r = 32

        # scale radius
        self.scale_r = 80    # smaller scale

        # mouse bindings
        self.bind("<Button-1>", self._mouse_big)
        self.bind("<B1-Motion>", self._mouse_big)

        self.bind("<Button-3>", self._mouse_small)
        self.bind("<B3-Motion>", self._mouse_small)
        
        self.bind("<ButtonRelease-3>", self._reset_fine_mouse)
        
        self.redraw()


    # ================================================================
    @property
    def value(self):
        return self.coarse + self.fine


    # ================================================================
    def redraw(self):
        self.delete("all")
        self._draw_outer_frame()
        self._draw_display()
        self._draw_scale()
        self._draw_big_knob()
        self._draw_small_knob()
        self._draw_small_triangle()
        self._draw_led_on_knob()
        self._draw_captions()


    # ================================================================
    def _value_to_angle(self, v):
        t = (v - self.min_value) / (self.max_value - self.min_value)
        ang = self.angle_start + (self.angle_end - self.angle_start) * t
        return math.radians(ang)
    
    def _mouse_angle(self, e):
        dx = e.x - self.cx
        dy = self.cy - e.y
        ang = math.degrees(math.atan2(dy, dx))  # 90 at top, -90 at bottom

        # Normalize to 0–360
        if ang < 0:
            ang += 360

        # Clamp to arc 225→315(-45)
        a0 = self.angle_start      # 225
        a1 = (self.angle_end % 360)  # -45 -> 315

        # If angle is outside arc, clamp to closest edge
        if ang > a0 and ang < a1:
            # Pick nearest boundary
            if abs(ang - a0) < abs(ang - a1):
                ang = a0
            else:
                ang = a1

        return ang

    def _reset_fine_mouse(self, e):
        self._last_fine_angle = None
    

    # ================================================================
    def _mouse_big(self, e):
        t = self._mouse_to_t(e)  # 0–1 along the arc
        self.coarse = self.min_value + t * (self.max_value - self.min_value)
        self.redraw()

    # ================================================================
    def _mouse_small(self, e):
        dx = e.x - self.cx
        dy = self.cy - e.y

        ang = math.degrees(math.atan2(dy, dx))
        ang = (ang + 360) % 360  # normalize to 0–360

        if self._last_fine_angle is None:
            self._last_fine_angle = ang
            return

        delta = ang - self._last_fine_angle

        # Handle wrap-around
        if delta > 180:
            delta -= 360
        elif delta < -180:
            delta += 360

        # CLOCKWISE should INCREASE fine
        self.fine -= delta * (10 / 360)

        self._last_fine_angle = ang
        self.redraw()


        
    # ================================================================
    def _mouse_to_t(self, e):
        """Convert mouse position to normalized t along the dial arc (0–1)."""
        ang = self._mouse_angle(e)  # 0–360, clamped to valid arc

        # Total span of the dial arc (e.g. 270° for 225 → -45)
        arc_span = (self.angle_start - self.angle_end) % 360  # > 0

        # Distance along the arc from angle_start towards angle_end,
        # moving in the direction of decreasing angle.
        arc_dist = (self.angle_start - ang) % 360

        t = arc_dist / arc_span
        # Safety clamp
        if t < 0:
            t = 0
        elif t > 1:
            t = 1
        return t

    # ================================================================
    def _draw_outer_frame(self):
        w, h = self.w, self.h
        self.create_rectangle(0, 0, w - 1, h - 1, outline="#000000")
        self.create_rectangle(1, 1, w - 2, h - 2, outline="#FFFFFF")
        self.create_rectangle(2, 2, w - 3, h - 3, outline="#C0C0C0")
        self.create_rectangle(4, 4, w - 5, h - 5, outline="#000000")


    # ================================================================
    def _draw_display(self):
        box = (self.w//2 - 45, 10, self.w//2 + 45, 40)

        self.create_rectangle(*box, fill="#303030", outline="#000")
        self.create_rectangle(
            box[0]+2, box[1]+2, box[2]-2, box[3]-2,
            outline="#555", fill="black"
        )

        txt = f"{self.value:0.1f} %"

        self.create_text(
            (box[0]+box[2])//2,
            (box[1]+box[3])//2,
            text=txt,
            font=("Arial", 14, "bold"),
            fill=self.text_color
        )


    # ================================================================
    def _draw_scale(self):
        # r = self.scale_r
        r = 66
        
        # major ticks
        for i in range(11):
            v = self.min_value + i * (self.max_value - self.min_value) / 10
            a = self._value_to_angle(v)

            x1 = self.cx + (r - 15) * math.cos(a)
            y1 = self.cy - (r - 15) * math.sin(a)
            x2 = self.cx + r * math.cos(a)
            y2 = self.cy - r * math.sin(a)

            self.create_line(x1, y1, x2, y2, width=2)

            nx = self.cx + (r + 18) * math.cos(a)
            ny = self.cy - (r + 18) * math.sin(a)
            self.create_text(nx, ny, text=str(int(v)), font=("Arial", 10))

        # minor ticks
        minor_start = self.big_r       # exactly at big knob surface (radius 50)
        minor_len   = 6                # short outward tick
        minor_end   = minor_start + minor_len

        for i in range(21):
            v = self.min_value + i * (self.max_value - self.min_value) / 20
            a = self._value_to_angle(v)

            x1 = self.cx + minor_start * math.cos(a)
            y1 = self.cy - minor_start * math.sin(a)

            x2 = self.cx + minor_end * math.cos(a)
            y2 = self.cy - minor_end * math.sin(a)

            self.create_line(x1, y1, x2, y2, width=1)

    # ================================================================
    def _draw_big_knob(self):
        r = self.big_r

        # SAME STYLE as small knob
        self.create_oval(
            self.cx - r, self.cy - r,
            self.cx + r, self.cy + r,
            fill="#D0D0D0", outline="#808080", width=2
        )

        # highlight arc
        self.create_arc(
            self.cx - r, self.cy - r,
            self.cx + r, self.cy + r,
            start=45, extent=180,
            outline="white", style="arc", width=2
        )


    # ================================================================
    def _draw_small_knob(self):
        r = self.small_r

        self.create_oval(
            self.cx - r, self.cy - r,
            self.cx + r, self.cy + r,
            fill="#D0D0D0", outline="#808080", width=2
        )

        # highlight arc
        self.create_arc(
            self.cx - r, self.cy - r,
            self.cx + r, self.cy + r,
            start=45, extent=180,
            outline="white", style="arc", width=2
        )


    # ================================================================
    def _draw_small_triangle(self):
        r = self.small_r - 5

        # fine value directly controls angle offset
        # 1 fine unit = 36 degrees
        ang = self.angle_start - self.fine * 36
        a = math.radians(ang)

        tip_x = self.cx + r * math.cos(a)
        tip_y = self.cy - r * math.sin(a)

        base_width = 12
        base_back = 8

        bx = self.cx + (r - base_back) * math.cos(a)
        by = self.cy - (r - base_back) * math.sin(a)

        left = a + math.radians(90)
        right = a - math.radians(90)

        b1x = bx + (base_width/2) * math.cos(left)
        b1y = by - (base_width/2) * math.sin(left)

        b2x = bx + (base_width/2) * math.cos(right)
        b2y = by - (base_width/2) * math.sin(right)

        self.create_polygon(
            tip_x, tip_y,
            b1x, b1y,
            b2x, b2y,
            fill="lime",
            outline="black"
        )

    # ================================================================
    def _draw_led_on_knob(self):
        """Green LED dot located ON the big knob instead of on the ring."""
        a = self._value_to_angle(self.coarse)
        r = self.big_r - 10

        x = self.cx + r * math.cos(a)
        y = self.cy - r * math.sin(a)

        self.create_oval(
            x-4, y-4, x+4, y+4,
            fill=self.dot_color, outline="black"
        )
        
    def _draw_captions(self):
        self.create_text(
            100, 225,
            text=self.caption,
            font=("Arial", 11)
        )



# -----------------------------------------------------
# DEMO
# -----------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    dial = DualRotaryKnob(root, caption="SignalName1")
    dial.pack(padx=10, pady=10)
    root.mainloop()
