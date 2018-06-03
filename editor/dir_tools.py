import os.path


EDITOR_DIR = os.path.dirname(os.path.abspath(__file__))
WISUALIA_DIR = os.path.dirname(EDITOR_DIR)
def relative_to_wisualia(name):
    return os.path.join(WISUALIA_DIR, name)
