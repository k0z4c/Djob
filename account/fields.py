from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.db.models.fields.files import ImageFieldFile
from copy import copy
''' find a way to put correct weight and height readed from Field; or simply put in conf'''
''' proxy class to file used by *Field'''
class AvatarImageFieldFile(ImageFieldFile):

    def save(self, name, content, save=True):
        im = Image.open(content)
        im.thumbnail((self.field.default_width, self.field.default_height), Image.ANTIALIAS)
        tmp_file = BytesIO(b'')
        im.save(tmp_file, 'JPEG')
        tmp_file.seek(0)
        content = File(tmp_file)
        super().save(name, content, save)

class AvatarImageField(models.ImageField):
    attr_class = AvatarImageFieldFile

    def __init__(self, default_width=None, default_height=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_width = default_width
        self.default_height = default_height
