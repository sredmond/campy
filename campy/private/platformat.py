"""
Java Backend Format Strings

The following section lists format strings for the Java backend, and can/
should be updated as the text API to the Stanford Portable Library changes.
The strings are marked using keyword format syntax, which can be expanded by
keyword in Python
"""
# Platform::filelib_fileExists
# Platform::filelib_isFile
# Platform::filelib_isSymbolicLink
# Platform::filelib_isDirectory
# Platform::filelib_setCurrentDirectory
# Platform::filelib_getCurrentDirectory
# Platform::filelib_getTempDirectory
# Platform::filelib_createDirectory
# Platform::filelib_deleteFile
# Platform::filelib_getDirectoryPathSeparator
# Platform::filelib_getSearchPathSeparator
# Platform::filelib_expandPathname
# Platform::filelib_listDirectory
# Platform::filelib_fileExists
# Platform::filelib_isFile
# Platform::filelib_isSymbolicLink
# Platform::filelib_isDirectory
# Platform::filelib_setCurrentDirectory
# Platform::filelib_getCurrentDirectory
# Platform::filelib_getTempDirectory
# Platform::filelib_createDirectory
# Platform::filelib_deleteFile
# Platform::filelib_getDirectoryPathSeparator
# Platform::filelib_getSearchPathSeparator
# Platform::filelib_expandPathname
# Platform::filelib_listDirectory

# Platform::setStackSize

# Platform::os_getLastError

# Platform::regex_match
# Platform::regex_matchCount
# Platform::regex_matchCountWithLines
# Platform::regex_replace

# Transfer to functions: DONE:
# File_


# TODO: special
File_openFileDialog = 'File.openFileDialog("{title!q}", "{mode}", "{path!q}")'   # TODO check if needs to be quoted

GWindow_constructor = 'GWindow.create("{id}", {width}, {height}, "{top_compound}", {visible!b})'
GWindow_delete = 'GWindow.delete("{id}")'
GWindow_close = 'GWindow.close("{id}")'
GWindow_requestFocus = 'GWindow.requestFocus("{id}")'
GWindow_setExitOnClose = 'GWindow.setExitOnClose("{id}", {value!b})'
GWindow_clear = 'GWindow.clear("{id}")'
GWindow_clearCanvas = 'GWindow.clearCanvas("{id}")'
GWindow_repaint = 'GWindow.repaint("{id}")'
GWindow_saveCanvasPixels = 'GWindow.saveCanvasPixels("{id}", {filename!q}'
GWindow_setSize = 'GWindow.setSize("{id}", {width}, {height})'
GWindow_setCanvasSize = 'GWindow.setCanvasSize("{id}", {width}, {height})'
GWindow_setCloseOperation = 'GWindow.setCloseOperation("{id}", {op}'
GWindow_minimize = 'GWindow.minimize("{id}")'
GWindow_pack = 'GWindow.pack("{id}")'
GWindow_setTitle = 'GWindow.setTitle("{id}", {title!q})'
GWindow_setLocation = 'GWindow.setLocation("{id}", {x}, {y})'
GWindow_setLocationSaved = 'GWindow.setLocationSaved("{id}", {value!b})'
GWindow_setPixel = 'GWindow.setPixel("{id}", {x}, {y}, {rgb}, {repaint!b})'
GWindow_setPixels = 'GWindow.setPixels("{id}", {base64!q})' # TODO: Special
GWindow_toBack = 'GWindow.toBack("{id}")'
GWindow_toFront = 'GWindow.toFront("{id}")'
GWindow_getScreenHeight = 'GWindow.getScreenHeight()'
GWindow_getScreenSize = 'GWindow.getScreenSize()'
GWindow_getScreenWidth = 'GWindow.getScreenWidth()'
GWindow_draw = 'GWindow.draw("{id}", "{gobj_id}")'
GWindow_drawInBackground = 'GWindow.drawInBackground("{id}", "{gobj_id}")'
GWindow_exitGraphics = 'GWindow.exitGraphics()' # TODO: special
GWindow_setRegionAlignment = 'GWindow.setRegionAlignment("{id}", "{region}", "{align}")'
GWindow_setResizable = 'GWindow.setResizable("{id}", {value!b})'
GWindow_addToRegion = 'GWindow.addToRegion("{id}", "{gobj_id}", "{region}")'
GWindow_getLocation = 'GWindow.getLocation("{id}")' # TODO special
GWindow_getPixel = 'GWindow.getPixel("{id}", {x}, {y})' # TODO special
GWindow_getPixels = 'GWindow.getPixels("{id}")'  # TODO special
GWindow_getRegionSize = 'GWindow.getRegionSize("{id}", "{region}")' # TODO: special
GWindow_removeFromRegion = 'GWindow.removeFromRegion("{id}", "{gobj_id}", "{region}")'
GWindow_getSize = 'GWindow.getSize("{id}")' # TODO special
GWindow_getCanvasSize = 'GWindow.getCanvasSize("{id}")'  # TODO: special
GWindow_getContentPaneSize = 'GWindow.getContentPaneSize("{id}")' # TODO: special
GWindow_setVisible = 'GWindow.setVisible("{id}", {flag!b})'

GTimer_constructor = 'GTimer.create("{id}", {millis})'
GTimer_delete = 'GTimer.deleteTimer("{id}")'
GTimer_start = 'GTimer.startTimer("{id}")'
GTimer_pause = 'GTimer.pause({millis})'
GTimer_stop = 'GTimer.stopTimer("{id}")'

HttpServer_sendResponse = 'HttpServer.sendResponse({request_id}, {http_error_code}, {contentType!q}, {responseText!q})'
HttpServer_sendResponseFile = 'HttpServer.sendResponseFile({request_id}, {content_type!q}, {response_file_path!q})'
HttpServer_start = 'HttpServer.start({port})'
HttpServer_stop = 'HttpServer.stop()'

Sound_constructor = 'Sound.create("{id}", {filename!q})'
Sound_delete = 'Sound.delete("{id}")'
Sound_play = 'Sound.play("{id}")'

# Platform::url_download

GCompound_constructor = 'GCompound.create("{id}")'
GCompound_add = 'GCompound.add("{compound_id}", "{gobj_id}")'

GObject_delete = 'GObject.delete("{id}")'
GObject_remove = 'GObject.remove("{id}")'
GObject_sendForward = 'GObject.sendForward("{id}")'
GObject_sendToFront = 'GObject.sendToFront("{id}")'
GObject_sendBackward = 'GObject.sendBackward("{id}")'
GObject_sendToBack = 'GObject.sendToBack("{id}")'
GObject_setVisible = 'GObject.setVisible("{id}", {flag!b})'
GObject_setColor = 'GObject.setColor("{id}", "{color}")'
GObject_scale = 'GObject.scale("{id}", {sx}, {sy})'
GObject_rotate = 'GObject.rotate("{id}", {theta})'
GObject_contains = 'GObject.contains("{id}", {x}, {y})'  # TODO: special move into gobjects.py
GObject_getBounds = 'GObject.getBounds("{id}")' # TODO: special
GObject_setLineWidth = 'GObject.setLineWidth("{id}", {line_width})'
GObject_setLocation = 'GObject.setLocation("{id}", {x}, {y})'
GObject_setSize = 'GObject.setSize("{id}", {width}, {height})'
GObject_setAntialiasing = 'GObject.setAntialiasing({value!b})'
GObject_setFilled = 'GObject.setFilled("{id}", {flag!b})'
GObject_setFillColor = 'GObject.setFillColor("{id}", "{color}")'

GInteractor_isEnabled = 'GInteractor.isEnabled("{id}")' # TODO: special
GInteractor_setEnabled = 'GInteractor.setEnabled("{id}", {value!b})'
GInteractor_setFont = 'GInteractor.setFont("{id}", "{font!u}")'
GInteractor_setIcon = 'GInteractor.setIcon("{id}", {filename!q})'
GInteractor_setMnemonic = 'GInteractor.setMnemonic("{id}", {mnemonic})' # TODO: special
GInteractor_setText = 'GInteractor.setText("{id}", {text!u})'
GInteractor_setTextPosition = 'GInteractor.setTextPosition("{id}", {horizontal}, {vertical})'
GInteractor_setTooltip = 'GInteractor.setTooltip("{id}", {tooltip_text!q})'

GRect_constructor = 'GRect.create("{id}", {width}, {height})'

GRoundRect_constructor = 'GRoundRect.create("{id}", {width}, {height}, {corner})'

G3DRect_constructor = 'G3DRect.create("{id}", {width}, {height}, {raised!b})'
G3DRect_setRaised = 'G3DRect.setRaised("{id}", {raised!b})'

GOval_constructor = 'GOval.create("{id}", {width}, {height})'

GArc_constructor = 'GArc.create("{id}", {width}, {height}, {start}, {sweep})'
GArc_setStartAngle = 'GArc.setStartAngle("{id}", {angle})'
GArc_setSweepAngle = 'GArc.setSweepAngle("{id}", {angle})'
GArc_setFrameRectangle = 'GArc.setFrameRectangle("{id}", {x}, {y}, {width}, {height})' # TODO: special

GLine_constructor = 'GLine.create("{id}", {x1}, {y1}, {x2}, {y2})'
GLine_setStartPoint = 'GLine.setStartPoint("{id}", {x}, {y})' # TODO special
GLine_setEndPoint = 'GLine.setEndPoint("{id}", {x}, {y})'

GImage_constructor = 'GImage.create("{id}", "{filename}")' # TODO: special

GLabel_constructor = 'GLabel.create("{id}", {label!q})'
GLabel_setFont = 'GLabel.setFont("{id}", "{font}")'
GLabel_setLabel = 'GLabel.setLabel("{id}", {label!q})'
GLabel_getFontAscent = 'GLabel.getFontAscent("{id}")' # TODO: special
GLabel_getFontDescent = 'GLabel.getFontDescent("{id}")'  # TODO: special
GLabel_getSize = 'GLabel.getGLabelSize("{id}")'  # TODO: special

GPolygon_constructor = 'GPolygon.create("{id}")'
GPolygon_addVertex = 'GPolygon.addVertex("{id}", {x}, {y})'  # TODO: special

DiffImage_compareImages = 'DiffImage.compareImages({file1!q}, {file2!q}, {outfile!q})'
DiffImage_compareWindowToImage = 'DiffImage.compareWindowToImage("{id}", {file2!q}, {ignore_winodw_size!b})'
DiffImage_show = 'DiffImage.show({file1!q}, {file2!q})'

GBufferedImage_constructor = 'GBufferedImage.create("{id}", {x}, {y}, {width}, {height}, {rgb})' # TODO special and round
GBufferedImage_fill = 'GBufferedImage.fill("{id}", {rgb})'
GBufferedImage_fillRegion = 'GBufferedImage.fillRegion("{id}", {x}, {y}, {width}, {height}, {rgb})'  # TODO rounding
GBufferedImage_load = 'GBufferedImage.load("{id}", {filename!q})'
GBufferedImage_resize = 'GBufferedImage.resize("{id}", {width}, {height}, {retain!b})'  # TODO: round
GBufferedImage_save = 'GBufferedImage.save("{id}", {filename!q})'
GBufferedImage_setRGB = 'GBufferedImage.setRGB("{id}", {x}, {y}, {rgb})' # TODO round
GBufferedImage_updateAllPixels = 'GBufferedImage.updateAllPixels("{id}", "{base64}")'

# SECTION: GInteractor

GInteractor_setAccelerator = 'GInteractor.setAccelerator("{id}", {accelerator!u})'
GInteractor_setActionCommand = 'GInteractor.setActionCommand("{id}", {cmd!q})'
GInteractor_setBackground = 'GInteractor.setBackground("{id}", "{color}")'
GInteractor_addActionListener = 'GInteractor.addActionListener("{id}")'
GInteractor_removeActionListener = 'GInteractor.removeActionListener("{id}")'
GInteractor_requestFocus = 'GInteractor.requestFocus("{id}")'
GInteractor_getFont = 'GInteractor.getFont("{id}")'  # TODO: special
GInteractor_getMnemonic = 'GInteractor.getMnemonic("{id}")' # TODO: special
GInteractor_getSize = 'GInteractor.getSize("{id}")'  # TODO: special

GButton_constructor = 'GButton.create("{id}", {label!q})'  # TODO: special

GCheckBox_constructor = 'GCheckBox.create("{id}", {label!q})'
GCheckBox_isSelected = 'GCheckBox.isSelected("{id}")'  # TODO: special
GCheckBox_setSelected = 'GCheckBox.setSelected("{id}", {state!b})'

GRadioButton_constructor = 'GRadioButton.create("{id}", {label!q}, {group!q})'
GRadioButton_isSelected = 'GRadioButton.isSelected("{id}")'  # TODO: special
GRadioButton_setSelected = 'GRadioButton.setSelected("{id}", {state!b})'

GSlider_constructor = 'GSlider.create("{id}", {min}, {max}, {value})'
GSlider_getMajorTickSpacing = 'GSlider.getMajorTickSpacing("{id}")'  # TODO: special
GSlider_getMinorTickSpacing = 'GSlider.getMinorTickSpacing("{id}")'  # TODO: special
GSlider_getPaintLabels = 'GSlider.getPaintLabels("{id}")'  # TODO: special
GSlider_getPaintTicks = 'GSlider.getPaintTicks("{id}")'  # TODO: special
GSlider_getSnapToTicks = 'GSlider.getSnapToTicks("{id}")'  # TODO: special
GSlider_getValue = 'GSlider.getValue("{id}")'  # TODO: special
GSlider_setMajorTickSpacing = 'GSlider.setMajorTickSpacing("{id}", {value})'
GSlider_setMinorTickSpacing = 'GSlider.setMinorTickSpacing("{id}", {value})'
GSlider_setPaintLabels = 'GSlider.setPaintLabels("{id}", {value!b})'
GSlider_setPaintTicks = 'GSlider.setPaintTicks("{id}", {value!b})'
GSlider_setSnapToTicks = 'GSlider.setSnapToTicks("{id}", {value!b})'
GSlider_setValue = 'GSlider.setValue("{id}", {value})'

GTable_constructor = 'GTable.create("{id}", {num_rows}, {num_cols}, {x}, {y}, {width}, {height})'  # TODO: special
GTable_autofitColumnWidths = 'GTable.autofitColumnWidths("{id}")'
GTable_clear = 'GTable.clear("{id}")'
GTable_clearFormatting = 'GTable.clearFormatting("{id}")'
GTable_get = 'GTable.get("{id}", {row}, {column})'  # TODO: special
GTable_getColumnWidth = 'GTable.getColumnWidth("{id}", {column})'  # TODO: special
GTable_getSelection = 'GTable.getSelection("{id}")'  # TODO: special
GTable_resize = 'GTable.resize("{id}", {num_rows}, {num_cols})'  # TODO: special
GTable_select = 'GTable.select("{id}", {row}, {column})'
GTable_set = 'GTable.set("{id}", {row}, {column}, {value!q})'
GTable_setCellAlignment = 'GTable.setCellAlignment("{id}", {row}, {column}, {align})'
GTable_setCellBackground = 'GTable.setCellBackground("{id}", {row}, {column}, {color!q})'
GTable_setCellFont = 'GTable.setCellFont("{id}", {row}, {column}, {font!q})'
GTable_setCellForeground = 'GTable.setCellForeground("{id}", {row}, {column}, {color!q}))'
GTable_setColumnAlignment = 'GTable.setColumnAlignment("{id}", {column}, {align}))'
GTable_setColumnBackground = 'GTable.setColumnBackground("{id}", {column}, {color!q})'
GTable_setColumnFont = 'GTable.setColumnFont("{id}", {column}, {font!q})'
GTable_setColumnForeground = 'GTable.setColumnForeground("{id}", {column}, {color!q})'
GTable_setColumnHeaderStyle = 'GTable.setColumnHeaderStyle("{id}", {style})'
GTable_setColumnWidth = 'GTable.setColumnWidth("{id}", {column}, {width})'
GTable_setEditable = 'GTable.setEditable("{id}", {editable!b})'
GTable_setEditorValue = 'GTable.setEditorValue("{id}", {row}, {column}, {value!q})'
GTable_setEventEnabled = 'GTable.setEventEnabled("{id}", {type}, {enabled!b})'
GTable_setFont = 'GTable.setFont("{id}", {font!q})'
GTable_setHorizontalAlignment = 'GTable.setHorizontalAlignment("{id}", {alignment!q})'
GTable_setRowAlignment = 'GTable.setRowAlignment("{id}", {row}, {align})'
GTable_setRowBackground = 'GTable.setRowBackground("{id}", {row}, {color!q})'
GTable_setRowColumnHeadersVisible = 'GTable.setRowColumnHeadersVisible("{id}", {visible!b})'
GTable_setRowFont = 'GTable.setRowFont("{id}", {row}, {font!q})'
GTable_setRowForeground = 'GTable.setRowForeground("{id}", {row}, {color!q})'

GTextArea_constructor = 'GTextArea.create("{id}", {width}, {height})'
GTextArea_getText = 'GTextArea.getText("{id}")'  # TODO: special
GTextArea_setEditable = 'GTextArea.setEditable("{id}", {editable!b})'
GTextArea_setFont = 'GTextArea.setFont("{id}", {font!q})'
GTextArea_setText = 'GTextArea.setText("{id}", {text!q})'

GTextField_constructor = 'GTextField.create("{id}", {num_chars})'  # TODO: special
GTextField_getText = 'GTextField.getText("{id}")'  # TODO: special
GTextField_isEditable = 'GTextField.isEditable("{id}")'  # TODO: special
GTextField_setEditable = 'GTextField.setEditable("{id}", {editable!b})'
GTextField_setPlaceholder = 'GTextField.setPlaceholder("{id}", {text!q})'
GTextField_setText = 'GTextField.setText("{id}", {text!q})'

GChooser_constructor = 'GChooser.create("{id}")'  #TODO: special
GChooser_addItem = 'GChooser.addItem("{id}", {item!q})'
GChooser_getSelectedItem = 'GChooser.getSelectedItem("{id}")' # TODO: special
GChooser_setSelectedItem = 'GChooser.setSelectedItem("{id}", {item!q})'

# END SECTION: GInteractor

GEvent_getNextEvent = 'GEvent.getNextEvent({mask})' # TODO: special
GEvent_waitForEvent = 'GEvent.waitForEvent({mask})' # TODO: special

GFileChooser_showOpenDialog = 'GFileChooser.showOpenDialog({current_dir!q}, {file_filter!q})'  # TODO: special
GFileChooser_showSaveDialog = 'GFileChooser.showSaveDialog({current_dir!q}, {file_filter!q})' # TODO: special

GOptionPane_showConfirmDialog = 'GOptionPane.showConfirmDialog({message!u}, {title!u}, {type})' # TODO: special
GOptionPane_showInputDialog = 'GOptionPane.showInputDialog({message!u}, {title!u})'  # TODO: special
GOptionPane_showMessageDialog = 'GOptionPane.showMessageDialog({message!u}, {title!u}, {type})'  # TODO: special
GOptionPane_showOptionDialog = 'GOptionPane.showOptionDialog({message!u}, {title!u}, {options}, {initially_selected!q})'  #TODO: very special
GOptionPane_showTextFileDialog = 'GOptionPane.showTextFileDialog({message!u}, {title!u}, {rows}, {cols})' # TODO: special

Clipboard_get = 'Clipboard.get()'  # TODO: special
Clipboard_set = 'Clipboard.set({text!u})'

# Platform::cpplib_setCppLibraryVersion
# Platform::cpplib_getCppLibraryVersion
SPL_getJavaBackEndVersion = 'StanfordCppLib.getJbeVersion()' # TODO: special

# JBEConsole_isBlocked = 'JBEConsole.isBlocked()'
JBEConsole_print = 'JBEConsole.print({line!q}, {stderr!b})'  # TODO: special
JBEConsole_getLine = 'JBEConsole.getLine()'  # TODO: special
JBEConsole_clear = 'JBEConsole.clear()'
JBEConsole_minimize = 'JBEConsole.minimize()'
JBEConsole_setFont = 'JBEConsole.setFont({font})'
JBEConsole_setSize = 'JBEConsole.setSize({width}, {height})'
JBEConsole_setTitle = 'JBEConsole.setTitle({title!q})'
JBEConsole_setLocation = 'JBEConsole.setLocation({x}, {y})'
JBEConsole_setCloseOperation = 'JBEConsole.setCloseOperation({value})'
JBEConsole_setErrorColor = 'JBEConsole.setErrorColor({color!q})'
JBEConsole_setExitProgramOnClose = 'JBEConsole.setExitProgramOnClose({value!b})'
JBEConsole_setLocationSaved = 'JBEConsole.setLocationSaved({value!b})'
JBEConsole_setOutputColor = 'JBEConsole.setOutputColor({color!q})'
JBEConsole_setVisible = 'JBEConsole.setVisible({value!b})'
JBEConsole_toFront = 'JBEConsole.toFront()'

Note_play = 'Note.play({note!u})'  # TODO: special

AutograderInput_addButton = 'AutograderInput.addButton({text!u}, {input!u})'  # TODO: special
AutograderInput_removeButton = 'AutograderInput.removeButton({text!u})'
AutograderInput_addCategory = 'AutograderInput.addCategory({name!u})'
AutograderInput_removeCategory = 'AutograderInput.removeCategory({name!u})'
AutograderInput_setVisible = 'AutograderInput.setVisible({visible!b})'
AutograderUnitTest_addTest = 'AutograderUnitTest.addTest({test_name!u}, {category!u}, {style_check!b})'
AutograderUnitTest_catchExceptions = 'AutograderUnitTest.catchExceptions()' # TODO: special
AutograderUnitTest_clearTests = 'AutograderUnitTest.clearTests({style_check!b})'
AutograderUnitTest_clearTestResults = 'AutograderUnitTest.clearTestResults({style_check!b})'
AutograderUnitTest_isChecked = 'AutograderUnitTest.isChecked({full_test_name!u})' # TODO special
AutograderUnitTest_setChecked = 'AutograderUnitTest.setChecked({full_test_name!u}, {checked!b})'
AutograderUnitTest_setTestCounts = 'AutograderUnitTest.setTestCounts({pass_count}, {test_count}, {style_check!b})'
AutograderUnitTest_setTestDetails = 'AutograderUnitTest.setTestDetails({test_full_name!u}, {deets!u}, {style_check!b})'
AutograderUnitTest_setTestingCompleted = 'AutograderUnitTest.setTestingCompleted({completed!b}, {style_check!b})'
AutograderUnitTest_setTestResult = 'AutograderUnitTest.setTestResult({test_full_name!u}, {result!u}, {style_check!b})'
AutograderUnitTest_setTestRuntime = 'AutograderUnitTest.setTestRuntime({test_full_name}, {runtime_ms})'
AutograderUnitTest_setVisible = 'AutograderUnitTest.setVisible({visible!b}, {style_check!b})'
AutograderUnitTest_setWindowDescriptionText = 'AutograderUnitTest.setWindowDescriptionText({text!u}, {style_check!b})'
