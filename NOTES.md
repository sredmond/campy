# Notes

This file is used to keep track of weird notes and observations. These notes aren't necessarily a problem / bug, just something to write down. It could be apparent strange behavior with the C++ libraries (should be reported to Marty), an odd implementation note, or anything else.

## Apparent Problems with the C++ Library

When adding a note, please append your username and the date.

- `GWindow.getScreenHeight` uses the width of screen, not the height (sredmond ????)
- `Platform.setValue` the string command is GetValue not SetValue (sredmond ????)
- Possibly no `GWindow::setVisible` in C++ libs? (sredmond 2017-10-21)
- `void addItem(std::string item)` in C++ libs should probably accept const& (sredmond 2017-10-22)
- line 106 of gbufferedimage should have x,y comments (sredmond 2017-11-02)
- `SparseGrid` in `sparsegrid.py` `fill` method should not fill everything when fill is called, just keep a ref to the filled item (or a copy?)
- `countDiffPixels` should be decomposed
- `GLabel` doesn't recompute ascent/descent in C++ after changing text (sredmond 2017-12-07)
- `GLabel` C++ platform doesn't urlencode the font, where GInteractor `setFont` does (sredmond 2017-12-07)
- `GCompound_Add` in C++ version for some reason gets status with a very cryptic comment (all it says is `  // JL`)

## Building Documentation

- `sphinx-quickstart` and enable all extensions
- `sphinx-apidoc -o docs/ . --separate`
- `make html`