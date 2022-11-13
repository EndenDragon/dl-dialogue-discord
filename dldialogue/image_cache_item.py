import shutil
import io

class ImageCacheItem:
    def __init__(self, url, file_object):
        self.url = url
        self.file_object = self.copy(file_object)

    def get_file_object(self):
        return self.copy(file_object)

    def copy(self, file_object):
        new_file_obj = io.BytesIO()
        shutil.copyfileobj(file_object, new_file_obj)
        new_file_obj.seek(0)
        return new_file_obj