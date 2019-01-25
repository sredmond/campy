import tkinter

from campy.private.backends.backend_base import GraphicsBackendBase

class TkBackend(GraphicsBackendBase):
    def __init__(self):
        self.root = tkinter.Tk()

    def gwindow_constructor(self, gw, width, height, top_compound, visible=True):
        self.canvas = tkinter.Canvas(self.root, width=width, height=height, bd=0, highlightthickness=0)
        self.canvas.pack()

        # self.root.update_idletasks()
        # self.root.update()

    def gwindow_delete(self, gw):
        pass

    def grect_constructor(self, gobj, width, height):
        self.canvas.create_rectangle(0, 0, width, height, fill='red')

    def run(self):
        self.root.mainloop()
