META_EXAMPLE = """
# The start and end dates in the YYYY-MM-DD format.
start_date: 2016-02-01
end_date: 2016-02-02

# The title of your album
title: The title of your album

# In which order do you want to display photos in this album. Default is
# by file name or by date and both can be ascending or descending.
# name_asc (default), name_desc, date_asc, date_desc
order_by: name_asc

# A list of subdirectories in the album directory that you want to exclude.
# To exclude the top directory just use: "- "
exclude:
    - rejected

# The file name of the cover photo for this album. The cover photo is the
# photo that is shown on the album overview page.
cover: IMG_000000.JPG

# You can divide your album in chapters. This can be done automatically or
# manually by providing the following settings.
chapters:
    - title: First chapter
      starts: IMG_000001.JPG
      subtitle: A small subtitle.
    - title: Second chapter.
      starts: IMG_000002.JPG
      # Add a daily subtitle automatically
      subtitle: daily
      # You can specify the anchor of this chapter. That way you can link to
      # it from your description
      anchor: second-chapter
      # etc.

# You can add your own parameters. They will be included in the json file
# for the album and you can use them on your site.
your_own_param: awesome

---
# Nice Title

In this part of the file you can use a markdown formatted description
of your project.

You can link to your chapters. E.g. [to the second one](#second-chapter). Or
you just link [to the firs chapter](#first-chapter).
"""

META_EXAMPLE_SHORT = """
title: %(title)s
start_date: %(start_date)s
# end_date:
# cover:
# chapters: daily
%(extra)s
"""

META_EXAMPLE_NO_ALBUM = """
album: false
"""
