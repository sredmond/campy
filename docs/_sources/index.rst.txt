.. campy documentation master file, created by
   sphinx-quickstart on Sun Dec 30 02:22:47 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to campy's documentation!
=================================

Hello, world! Welcome to the `campy` libraries.

Installation
------------
The `campy` library can be installed via `pip`::

	python3 -m pip install campy

Getting Started
---------------

Let's write our first program using `campy`. We'll draw an empty rectangle and a filled oval on a graphical window::

	from campy.graphics.gwindow import GWindow
	from campy.graphics.gobjects import GRect, GOval

	window = GWindow()
	rect = GRect(200, 100)  # A rectangle 200 pixels wide and 100 pixels tall.
	oval = GOval(100, 50)  # An oval whose bounding box is 100 pixels wide and 50 pixels tall.
	oval.filled = True
	window.add(rect, x=20, y=40)  # Add the rectangle to the graphical window 20 pixels from the left and 40 pixels from the top.
	window.add(oval, x=40, y=20)  # Add the oval to the graphical window 20 pixels from the left and 40 pixels from the top.

Using this documentation
------------------------

If you're looking for more information about a particular module, use the Module Index link below. For a list of all exported symbols, see the general index. Otherwise, use the search bar in the upper-left to search for particular symbols, such as `GWindow` or `GOval`.

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
