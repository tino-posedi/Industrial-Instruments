import tkinter as tk

class LEDSlider(tk.Canvas):
    def __init__(self, master, width=38, height=290, command=None, **kw):
        super().__init__(master, width=width, height=height,
                         highlightthickness=0, bg="#000", **kw)

        self.width = width
        self.height = height
        self.command = command

        self.LED_ON  = "#00FF00"
        self.LED_OFF = "#003300"

        self.handle_height = 10
        self.handle_width = width - 8

        self.handle_y = height // 2

        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)

        self.redraw()

    def redraw(self):
        self.delete("all")

        self._bevel(0, 0, self.width, self.height)

        inner_l = 4
        inner_r = self.width - 4
        inner_t = 4
        inner_b = self.height - 4

        on_start = self.handle_y
        on_end   = inner_b

        self._draw_led_bars(inner_l, inner_t, inner_r,
                            self.handle_y - self.handle_height,
                            on=False)

        self._handle(inner_l,
                     self.handle_y - self.handle_height,
                     inner_r,
                     self.handle_y)

        self._draw_led_bars(inner_l, self.handle_y, inner_r,
                            inner_b, on=True)

    def _bevel(self, x1, y1, x2, y2):
        self.create_rectangle(x1, y1, x2, y2, outline="#000")
        self.create_rectangle(x1+1, y1+1, x2-1, y2-1, outline="#FFF")
        self.create_rectangle(x1+2, y1+2, x2-2, y2-2, outline="#3C3C3C")
        self.create_rectangle(x1+3, y1+3, x2-3, y2-3, outline="#DCDCDC")

    def _draw_led_bars(self, x1, y1, x2, y2, on):
        if y2 <= y1:
            return

        y = y1
        toggle = True 

        while y < y2:
            if on:
                color = self.LED_ON if toggle else self.LED_OFF
            else:
                color = self.LED_OFF

            self.create_line(x1, y, x2, y, fill=color)
            toggle = not toggle
            y += 1

    def _handle(self, x1, y1, x2, y2):
        self.create_rectangle(x1, y1, x2, y2,
                              fill="#C0C0C0", outline="#000")
        self.create_rectangle(x1+1, y1+1, x2-1, y2-1,
                              outline="#FFF")

    def on_click(self, e):
        self.set_from_y(e.y)

    def on_drag(self, e):
        self.set_from_y(e.y)

    def set_from_y(self, y):
        min_y = 4 + self.handle_height
        max_y = self.height - 4

        self.handle_y = max(min_y, min(max_y, y))
        self.redraw()
        if self.command:
            self.command(self.get_value())

    def get_value(self):
        min_y = 4 + self.handle_height
        max_y = self.height - 4
        return 1 - (self.handle_y - min_y) / (max_y - min_y)

# -------------------------------
# DEMO
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="SystemButtonFace")

    def on_change(v):
        print("value:", round(v, 2))

    slider = LEDSlider(root, command=on_change)
    slider.pack(padx=20, pady=20)

    root.mainloop()
