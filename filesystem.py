import os
import platform

def get_appdata_path():
    if platform.system() == "Windows":
        # assume running Windows
        return os.path.join(os.environ['APPDATA'], "pzcurate")
    else:
        # assume running Linux-like system
        return os.path.expanduser(os.path.join("~", ".pzcurate"))

def get_documents_path():
    if platform.system() == "Windows":
        # https://stackoverflow.com/a/30924555/5013267
        import ctypes.wintypes

        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf)

        return buf.value
    else:
        # assume running Linux-like system
        return os.path.expanduser(os.path.join("~", "Documents"))

def get_data_path():
    return os.path.join(get_documents_path(), "PZCurate")

PATH_IMPORT = os.path.join(get_data_path(), "import")

# create paths
os.makedirs(PATH_IMPORT, exist_ok=True)