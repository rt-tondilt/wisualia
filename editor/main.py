# All imports are inside main function, this avoids importing them when
# creating worker thread.

def main() -> None:
    print('WISUALIA STARTING')
    # Sets current working directory so the behaviour of io operations won't
    # depend on users current directory.
    import os
    import __main__
    os.chdir(os.path.dirname(__main__.__file__))

    import gi #type: ignore
    gi.require_version('Gtk', '3.0')
    gi.require_version('GtkSource', '3.0')
    from gi.repository import GLib, Gtk, GObject, GtkSource #type: ignore
    GObject.type_register(GtkSource.View)

    import loop
    from gui import window, set_status_bar_text

    set_status_bar_text('No programm running')

    window.show_all()
    window.connect("delete-event", Gtk.main_quit)
    Gtk.main()

def main_with_memory_check():
    import tracemalloc
    tracemalloc.start()
    main()
    print('----------------------------------------------------------')
    ss = tracemalloc.take_snapshot()
    for i, a in enumerate(ss.statistics('traceback')):
        print(a)
        if i > 20: break

if __name__ == '__main__':
    main()
