from django.core.files.uploadhandler import MemoryFileUploadHandler

# https://docs.djangoproject.com/en/1.11/_modules/django/core/files/uploadhandler/#FileUploadHandler.new_file
class AvatarUploadHandler(MemoryFileUploadHandler):
    def file_complete(self, file_size):
        # io,bytesIO object; a file-like object (bytes)
        print("executing file_complete routine")
        from PIL import Image
        print("upload handler starts")
        print(self)
        img = Image.open(self.file).resize((10,10))
        self.file = BytesIO(img)
        super(AvatarUploadHandler, self).file_complete(file_size)

    # def upload_complete(self):
    #     print("Upload procedure terminated!")
    #     print(self.file)
    #     super().upload_complete()
