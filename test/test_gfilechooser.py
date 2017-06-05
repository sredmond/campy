from spgl.graphics.gfilechooser import GFileChooser

OPEN = True
SAVE = True

if OPEN:
    print("--------show_open_dialog--------")
    print(GFileChooser.show_open_dialog())
    print(GFileChooser.show_open_dialog('/Users/sredmond/Desktop/'))
    # print(GFileChooser.show_open_dialog('/'))
    # print(GFileChooser.show_open_dialog('~/Desktop'))
    print(GFileChooser.show_open_dialog('/not/a/dir'))
    print(GFileChooser.show_open_dialog('/no/trailing/slash/'))
    print(GFileChooser.show_open_dialog('../../'))


if SAVE:
    print("--------show_save_dialog--------")
    print(GFileChooser.show_save_dialog())
    print(GFileChooser.show_save_dialog('/'))
    print(GFileChooser.show_save_dialog('~/Desktop'))
    print(GFileChooser.show_save_dialog('/not/a/dir'))
    print(GFileChooser.show_save_dialog('/no/trailing/slash/'))
    print(GFileChooser.show_save_dialog('../../'))

