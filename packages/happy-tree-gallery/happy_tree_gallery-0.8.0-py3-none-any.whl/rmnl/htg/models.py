import datetime
import os

import peewee as pw

from playhouse.shortcuts import model_to_dict

from .utils import alphanum_hash
from .utils import slugify
from .utils import to_utc_timestamp

database = pw.SqliteDatabase(None)


class BaseModel(pw.Model):
    def dict(self):
        return model_to_dict(self)

    class Meta:
        database = database


class Picture(BaseModel):
    key = pw.CharField(unique=True, default=alphanum_hash)
    # Initial fields, must always be set.
    checksum = pw.CharField(unique=True)
    file_path = pw.TextField(unique=True)
    file_name = pw.CharField()

    # Meta data fields, only set on change
    sort_date = pw.DateTimeField(null=True)
    caption = pw.CharField(null=True)
    latitude = pw.FloatField(null=True)
    longitude = pw.FloatField(null=True)
    rotation = pw.IntegerField(default=True)

    # last_scan = pw.ForeignKeyField(Scan, related_name='pictures', null=True)
    last_change_indexed = pw.DateTimeField(default=datetime.datetime.now)

    def build_dict(self, picture_root):
        d = {"name": self.file_name, "ext": self.ext, "path": self.resize_path(picture_root)}
        if self.sort_date is not None:
            d["date"] = to_utc_timestamp(self.sort_date)
        if self.caption:
            d["caption"] = self.caption
        if self.latitude is not None and self.longitude is not None:
            d["location"] = [self.latitude, self.longitude]
        return d

    @property
    def ext(self):
        name, ext = os.path.splitext(self.file_name)
        return ext.lower()

    def resize_path(self, picture_root):
        return os.path.join(picture_root, self.key[:2], "%s-" % self.key[2:])

    class Meta:
        db_table = "pictures"


class Size(BaseModel):
    name = pw.CharField(unique=True)
    width = pw.IntegerField()
    height = pw.IntegerField()
    crop = pw.BooleanField(default=True)
    include_in_json = pw.BooleanField(default=False)
    change_date = pw.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return "<Size: %s>" % self.build_dict()

    def build_dict(self):
        return {
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "cropped": self.crop,
            "include_in_json": self.include_in_json,
            "change_date": self.change_date,
        }

    @staticmethod
    def all_names():
        try:
            return [size.name for size in Size.select()]
        except pw.OperationalError:
            return []

    @staticmethod
    def get_size_by_name(name):
        try:
            return Size.get(name=name)
        except Size.DoesNotExist:
            return None

    class Meta:
        db_table = "sizes"


class ResizedPicture(BaseModel):
    picture = pw.ForeignKeyField(Picture, related_name="resized_pictures")
    size = pw.ForeignKeyField(Size, related_name="sizes")
    picture_path = pw.TextField()
    resize_date = pw.DateTimeField(null=True)
    successfully_created = pw.BooleanField(default=False)
    width = pw.IntegerField(default=0)
    height = pw.IntegerField(default=0)

    @property
    def path(self):
        name, ext = os.path.splitext(self.picture.file_name)
        return os.path.join(
            self.picture_path, self.picture.key[:2], "%s-%s%s" % (self.picture.key[2:], self.size.name, ext.lower())
        )

    def url(self, picture_root):
        name, ext = os.path.splitext(self.picture.file_name)
        return os.path.join(
            picture_root, self.picture.key[:2], "%s-%s%s" % (self.picture.key[2:], self.size.name, ext)
        )

    class Meta:
        db_table = "resized_pictures"


class Album(BaseModel):
    key = pw.CharField(unique=True, default=alphanum_hash)
    hidden = pw.BooleanField(default=False)
    from_dir = pw.BooleanField(default=True)
    album_path = pw.TextField(unique=True)
    start_date = pw.DateTimeField(null=True)
    end_date = pw.DateTimeField(null=True)
    title = pw.CharField()
    description = pw.TextField(null=True)
    meta = pw.TextField(null=True)
    pictures = pw.ManyToManyField(Picture, backref="albums")

    exclude = []

    @property
    def slug(self):
        s = "%s-%s" % (slugify(self.title), self.key)
        if self.start_date:
            s = "%s-%s" % (self.start_date.strftime("%Y-%m-%d"), s)
        return s

    class Meta:
        db_table = "albums"


AlbumPicture = Album.pictures.get_through_model()


def init_database(db_file):
    database.init(db_file)
    database.connect()
    for tcl in [Picture, Size, ResizedPicture, Album, AlbumPicture]:
        if not tcl.table_exists():
            tcl.create_table()
    return database
