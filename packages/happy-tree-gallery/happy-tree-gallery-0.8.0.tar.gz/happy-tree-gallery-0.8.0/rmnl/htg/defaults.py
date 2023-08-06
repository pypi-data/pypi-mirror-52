# coding: utf-8

DEFAULT_CONFIG = """
###############################################################################
# Compulsory settings
###############################################################################

# The directory where htg will save resized photos
# e.g. /resized/photos/go/in/here
resized_photos_dir:

# The directory where htg will save the json data files
# e.g. /json/files/go/in/here
json_data_dir:

# The (relative) url where the webserver can find the resized photos
# e.g. /photos/
resized_photos_url: /photos/

# The (relative) url where the webserver can find the json data files
# e.g. /data/
json_data_url: /data/


###############################################################################
# Optional settings
###############################################################################

# The location of your database file.
# e.g.: /path/where/you/want/to/save/database.sqlite
# If you do not specify the database file the database will be saved as
# db.sqlite in the same directory as the config file.
database_file:

# A list of directories that contain your original photos.
# e.g. /path/where/you/keep/your/awesome/originals
original_photos_dirs:
    -

# Specify the sizes for the images you want to resize
# Make up a name for each size (e.g. large, thumb, etc)
# width: The maximum width of the resized image.
# height: The maximum height of the resized image. Leave empty to use the width.
# crop: Crop to fit maximum dimensions (true, false)
# include_resized_size_in_json: If true the exact size of the resized photo
# will be included in the json output.
sizes:
  large:
    crop: false
    height:
    include_resized_size_in_json: false
    width: 1920
  medium:
    crop: false
    height:
    include_resized_size_in_json: false
    width: 1280
  small:
    crop: false
    height:
    include_resized_size_in_json: false
    width: 640
  thumb:
    crop: false
    height: 150
    include_resized_size_in_json: true
    width: 50000

# By default the picture date is not set if no date can be found in a.
# the exif data and b. the filename. Use this flag to set the date to
# the file creation date.
use_file_creation_date_as_image_date: false

# Look for a file name <meta_file_name> in each directory. This meta file
# can contain settings and album data for that directory. See the
# documentation for info on the meta file.
meta_file_name: _meta.yaml

# Albums can be split into paragraphs and chapters defined inside the meta
# file, but if you set this to true paragraphs will automatically be created
# for each day inside an album. This helps make large amounts of pictures
# easier to digest
# You can also set this value inside the metafile for an album.
auto_day_paragraphs: true

# Albums are created for directories that contain a meta file but can also be
# created based on the directory name that resembles this one:
# YYYY-MM-DD - Title of you Album
create_albums_from_dir_names: true

# For the timeline view you can choose to show all photos or just those photos
# that do not belong to an album.
album_photos_in_timeline: true

# Files that match the following patterns will not be indexed. Files starting
# with . or : are always excluded.
exclude_files_and_dirs_that_match:
  - ^_.+$   # files starting with _

# Files and subdirectories in a directory that contains a file matching the
# name below will not be indexed.
exclude_file_name: _exclude

"""

# All the following settings can be set in the yaml file too.
# However they should be used carefully and do not need to be in the default
# yaml file that is generated from the above.
DEFAULT_ADVANCED = """
###############################################################################
# Other, more advanced settings
###############################################################################
image_extensions:
  - .jpg
  - .jpeg
  - .png
  - .bmp

video_extensions:
  - .mpg
  - .mpeg
  - .mov
  - .m4v
  - .mp4
  - .avi

file_date_formats:
  - \%Y-\%m-\%d-\%H.\%M.\%S
  - PANO_\%Y\%m\%d_\%H\%M\%S
  - TRIM_\%Y\%m\%d_\%H\%M\%S
  - VID_\%Y\%m\%d_\%H\%M\%S
  - IMG_\%Y\%m\%d_\%H\%M\%S
  - \%Y-\%m-\%d \%H.\%M.\%S
  - \%Y\%m\%d\%H\%M\%S
  - \%Y\%m\%d-\%H\%M\%S
  - \%Y\%m\%d-\%H\%M
  - \%Y\%m\%d\%H\%M\%S

album_dir_pattern: ^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})[ ]*-[ ]*(?P<title>.*)$
resize_with:
photos_per_json_file: 500

# Can be daily. daily or monthly.
timeline_granularity: monthly

"""  # noqa W605
