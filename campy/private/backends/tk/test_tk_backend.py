from campy.private.backends.tk.backend_tk import TkBackend

b = TkBackend()

w = b.gwindow_constructor('gwindow', 600, 400, 10, False)
r = b.grect_constructor('grect', 200, 200)

b.run()

