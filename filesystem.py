import os
import platform
import time
import zipfile

def get_appdata_path():
    if platform.system() == "Windows":
        # assume running Windows
        return os.path.join(os.environ['APPDATA'], "PZCurate")
    else:
        # assume running Linux-like system
        return os.path.expanduser(os.path.join("~", ".PZCurate"))

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

PATH_DATA = os.path.join(get_documents_path(), "PZCurate")
PATH_IMPORT = os.path.join(PATH_DATA, "import")
PATH_DATABASE = os.path.join(PATH_DATA, "data.db")    # Item/Tag/etc structured data
PATH_DATAZIP = os.path.join(PATH_DATA, "data.zip")    # actual file data
PATH_TMP = os.path.join(get_appdata_path(), "tmp")    # actual file data

class DataZipFile(zipfile.ZipFile):
    def __init__(self):
        super().__init__(PATH_DATAZIP,
                         mode="a",
                         compression=zipfile.ZIP_DEFLATED,
                         allowZip64=True,
                         compresslevel=-1)

    def get_num_files(self):
        # unused, may delete later
        file_count = 0
        for filename in self.namelist():
            if filename.startswith("files/"):
                file_count += 1
        return file_count


# create paths
os.makedirs(PATH_IMPORT, exist_ok=True)
os.makedirs(PATH_TMP, exist_ok=True)
