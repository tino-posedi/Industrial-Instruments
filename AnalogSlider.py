import tkinter as tk
import math


class AnalogSlider(tk.Canvas):
    def __init__(
        self,
        master,

        caption1="SignalName1",
        unit="%",            

        min_value=0,
        max_value=100,
        value=0,

        slider_color="gray",
        text_color="#00FF00",
        led_color="#00FF00",

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

        self.width = 110
        self.height = 320

        self.caption1 = caption1
        self.unit = unit     

        self.min_value = min_value
        self.max_value = max_value
        self.value = value

        self.slider_color = slider_color
        self.text_color = text_color
        self.led_color = led_color

        self.scale_top = 60
        self.scale_bottom = 280
        self.scale_height = self.scale_bottom - self.scale_top

        self.cx_left = 35
        self.cx_right = 75
        self.cx_center = 55

        self.bind("<Button-1>", self._mouse)
        self.bind("<B1-Motion>", self._mouse)

        self.redraw()

    def _value_to_y(self, v):
        t = (v - self.min_value) / (self.max_value - self.min_value)
        return self.scale_bottom - t * self.scale_height

    def _y_to_value(self, y):
        t = (self.scale_bottom - y) / self.scale_height
        return self.min_value + t * (self.max_value - self.min_value)

    def set_value(self, v):
        v = max(self.min_value, min(self.max_value, v))
        self.value = v
        self.redraw()

    def _mouse(self, e):
        self.set_value(self._y_to_value(e.y))

    def redraw(self):
        self.delete("all")
        self._draw_outer_frame()
        self._draw_display()
        self._draw_scale()
        self._draw_led_bar()
        self._draw_slider()
        self._draw_captions()

    def _draw_outer_frame(self):
        self.create_rectangle(0, 0, 109, 319, outline="#000")
        self.create_rectangle(1, 1, 108, 318, outline="#FFF")
        self.create_rectangle(2, 2, 107, 317, outline="#C0C0C0")
        self.create_rectangle(4, 4, 105, 315, outline="#000")

    def _draw_display(self):
        box = (10, 10, self.width - 10, 40)

        self.create_rectangle(*box, fill="#303030", outline="#000")
        self.create_rectangle(box[0] + 2, box[1] + 2,
                              box[2] - 2, box[3] - 2,
                              outline="#555", fill="black")

        display_text = f"{self.value:0.1f} {self.unit}"

        self.create_text(
            (box[0] + box[2]) / 2,   
            (box[1] + box[3]) / 2,
            text=display_text,
            font=("Arial", 14, "bold"),
            fill=self.text_color
        )

    def _draw_scale(self):
        cx_left = self.cx_left
        cx_right = self.cx_right

        value_range = self.max_value - self.min_value

        if value_range <= 10:
            major_step = 1
        elif value_range <= 20:
            major_step = 2
        elif value_range <= 50:
            major_step = 5
        else:
            major_step = 10

        major_values = set()

        for v in range(self.min_value, self.max_value + 1, major_step):
            major_values.add(v)

        major_values.add(self.min_value)
        major_values.add(self.max_value)

        for v in sorted(major_values):
            y = self._value_to_y(v)

            self.create_line(cx_left - 4, y, cx_left + 4, y, width=2)
            self.create_line(cx_right - 4, y, cx_right + 4, y, width=2)

            self.create_text(cx_left - 6, y, text=str(v),
                             font=("Arial", 9), anchor="e")
            self.create_text(cx_right + 6, y, text=str(v),
                             font=("Arial", 9), anchor="w")

        minor_step = major_step / 2
        for i in range(int(value_range / minor_step) + 1):
            v = self.min_value + i * minor_step
            if v in major_values:
                continue  
            if v > self.max_value:
                break

            y = self._value_to_y(v)
            self.create_line(cx_left, y, cx_left + 3, y, width=1)
            self.create_line(cx_right - 3, y, cx_right, y, width=1)


    def _draw_led_bar(self):
        cx = self.cx_center
        bar_width = 8

        self.create_rectangle(
            cx - bar_width/2, self.scale_top,
            cx + bar_width/2, self.scale_bottom,
            fill="#202020", outline="#101010"
        )

        y_value = self._value_to_y(self.value)

        self.create_rectangle(
            cx - bar_width/2 + 1, y_value,
            cx + bar_width/2 - 1, self.scale_bottom,
            fill=self.led_color, outline="#003000"
        )

    def _draw_slider(self):
        y_center = self._value_to_y(self.value)
        cx = (self.cx_left + self.cx_right) / 2

        knob_half_w = 14
        knob_half_h = 6

        self.create_rectangle(
            cx - knob_half_w, y_center - knob_half_h,
            cx + knob_half_w, y_center + knob_half_h,
            fill=self.slider_color, outline="black"
        )

        self.create_rectangle(
            cx - (knob_half_w - 1), y_center - (knob_half_h - 1),
            cx + (knob_half_w - 1), y_center + (knob_half_h - 1),
            outline="white"
        )

    def _draw_captions(self):
        self.create_text(
            self.width / 2,
            self.height - 22,
            text=self.caption1,
            font=("Arial", 10)
        )

# -----------------------------------------------------
# DEMO
# -----------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("AnalogSlider Demo")

    slider = AnalogSlider(
        root,
        caption1="SignalName1",
        unit="%",
        min_value=0,
        max_value=100,
        value=0,
    )
    slider.pack(padx=10, pady=10)

    root.mainloop()
