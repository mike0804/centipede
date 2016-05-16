# -*- coding: utf-8 -*-

from slugify import Slugify

slugify_filename = Slugify(to_lower=True)
slugify_filename.separator = '_'
slugify_filename.safe_chars = '-.'
slugify_filename.max_length = 255