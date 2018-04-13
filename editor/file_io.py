import gi
from gi.repository import Gtk

from gui import input_buffer
from state import switch_running, stop_running_and_playing
import dir_tools
# NB: There is one more import in the end of this file.

# Do not change this variable from other modules.
file_name = None #type: Optional[str]


TMP = 'temporary.py'

DEFAULT_PROGRAM = '''import wisualia
from wisualia.do import fill, stroke
from wisualia.shapes import circle
from wisualia.patterns import RGBA
from wisualia.animation import animate

def loop(t):
    circle((0,0), 1+t)
    fill(RGBA(1,1,0,0.5))
    stroke()

animate(loop)
'''

# Save input_buffer to file_name.
# Only works if file_name != None.
def save():
    code = input_buffer.get_text(input_buffer.get_start_iter(), input_buffer.get_end_iter(), True)
    with open(file_name, 'w') as f:
        f.write(code)

# Run dialog and set file_name and file_label.
# file_name and file_label won't change if user cancels.
# Return True if user didn't cancel, False otherwise.
def file_dialog(label:str) -> bool:
    global file_name
    assert label in ['Open', 'Save']

    gtk_stock_ok = Gtk.STOCK_OPEN if label=='Open' else Gtk.STOCK_SAVE
    action = Gtk.FileChooserAction.OPEN if label=='Open' else Gtk.FileChooserAction.SAVE
    dialog = Gtk.FileChooserDialog(label, window,
        action,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
         gtk_stock_ok, Gtk.ResponseType.OK))

    dialog.set_current_folder(dir_tools.get_dir('examples'))
    if dialog.run() == Gtk.ResponseType.OK:
        name = dialog.get_filename()
        file_name = name
        file_label.set_text(os.path.basename(name))
        dialog.destroy()
        return True
    else:
        dialog.destroy()
        return False

def load_default_program():
    global file_name
    file_name = os.getcwd()[:-6]+'\\'+TMP
    file_label.set_text(TMP)
    # file_name = None
    # file_label.set_text('')
    input_buffer.set_text(DEFAULT_PROGRAM)
    switch_running(None)


def new_file(_widget):
    dialog = Gtk.MessageDialog(window, 0, Gtk.MessageType.WARNING,
        Gtk.ButtonsType.OK_CANCEL, "New file")
    dialog.format_secondary_text(
        "You will lose all your unsaved changes.")
    if dialog.run() == Gtk.ResponseType.OK:
        load_default_program()
        stop_running_and_playing()
    dialog.destroy()

def open_file(_widget):
    if file_dialog('Open'):
        with open(file_name, 'r') as f:
            input_buffer.set_text(f.read())
            stop_running_and_playing()

def save_file_as(_widget):
    if file_dialog('Save'):
        save()
        stop_running_and_playing()

def save_file(_widget):
    if file_name == None or TMP in file_name:
        save_file_as(None)
    else:
        save()

def export(_widget):
    save_file(None)  # May not save if file_name==None and user cancels.
    if file_name == None:
        set_output('','Can not export if file is not saved.')
        return

    dirpath = os.path.dirname(file_name)
    libpath = dir_tools.get_dir('library')
    interpath = sys.executable #python interpreter path
    task = ('start cmd /c '
            '"cd {} && set PYTHONPATH=%PYTHONPATH%;{} && '
            '{} {} animate || '
            'pause"').format(dirpath, libpath, interpath, file_name)
    os.system(task)

# TODO: The result gets overwritten if playing is True.
def typecheck(_widget):
    stop_running_and_playing()
    loop.start()

    save_file(None) # May not save if file_name==None and user cancels.
    if file_name == None:
        set_output('','Can not typecheck if file is not saved.')
        return

    stdout, stderr, exitcode = mypy.api.run([file_name, '--config-file','mypy_user.ini'])
    result = stdout+stderr
    if result == '':
        result = 'Typecheck: No errors were found.'

    set_output('', str(result).replace('\n', '\n\n'))


from gui import *
new_button.connect('activate', new_file)
open_button.connect('activate', open_file)
save_button.connect('activate', save_file)
save_as_button.connect('activate', save_file_as)
export_button.connect('clicked', export)
typecheck_button.connect('clicked', typecheck)
