"""Set up and manage a menu bar."""
import tkinter as tk

def setup_menubar(master):
    """Create a menu bar and attach it to a tk.Tk() or tk.Toplevel().

    This menu bar looks like::

        MENU
        |-- File/
        |   |-- Save/
        |   |-- Exit/
        .-- Help/
            .-- About
    """
    menubar = tk.Menu(master)

    filemenu = tk.Menu(menubar, tearoff=False)
    filemenu.add_command(label="Save", command=lambda: print('Save Menu clicked.'))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=master.quit)  # TODO(sredmond): Why not master.destroy?
    menubar.add_cascade(label="File", menu=filemenu)

    helpmenu = tk.Menu(menubar, tearoff=False)
    helpmenu.add_command(label="About...", command=lambda: print('The campy libraries were created by Sam Redmond.'))
    menubar.add_cascade(label="Help", menu=helpmenu)

    master.config(menu=menubar)
