import os.path
def get_dir(name):
    editor_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(editor_dir)
    return os.path.join(root_dir, name)
