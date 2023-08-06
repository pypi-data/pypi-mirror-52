# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['beetsplug']

package_data = \
{'': ['*']}

install_requires = \
['beets>=1.4,<2.0', 'confuse>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'beets-kergoth',
    'version': '0.3.2',
    'description': "Various personal beets plugins that don't yet have a home elsewhere.",
    'long_description': "beets-kergoth\n=============\n\nThis is my personal collection of beets_ plugins that are not currently being\ndistributed separately.\n\nGenerally useful\n----------------\n\nThese plugins I consider to be useful in general and polished enough that I\nintend to either submit them upstream to beets or split off into separate\nprojects / python packages.\n\n- The `Alias Plugin`_ lets you define command aliases, much like git, and also\n  makes available any beet-prefixed commands in your ``PATH`` as well.\n- The `Import Inspect Plugin`_ lets you inspect the metadata changes to be\n  applied when importing.\n- The `Modify On Import Plugin`_ lets you define metadata changes to occur\n  on import when the specified queries match.\n- The `Replace Format Plugin`_ defines format functions for search/replace of\n  text, both single replacements and applications of a set of replacements\n  like the built in ``replace`` configuration option.\n- The `Saved Formats Plugin`_ lets you define saved, named format strings by\n  storing them in fields for later reference.\n- The `Saved Queries Plugin`_ lets you save queries by name for later use.\n\nSpecial Purpose\n---------------\n\nThese plugins are useful to me, but probably not to anyone else.\n\n- The ``musicsource`` plugin just forces me to define a ``source`` field when\n  importing new music, as this is how I organize my library. ``source`` is\n  where the music was acquired, e.g. Amazon, iTunes, Google, etc.\n- The ``picard`` plugin lets me launch MusicBrainz Picard with the items I'm\n  importing, either to use it to tag rather than beets, or as an inspection\n  tool to examine its metadata. This assumes a ``picard`` beets command\n  exists, as this is how it runs it.\n- The ``reimportskipfields`` plugin lets you specify fields from set_fields\n  to also be applied to skipped items on reimport. I use this to facilitate\n  resuming from a reimport, as it lets me apply a ``reimported`` field to\n  anything I tried to reimport, whether I was able to match it to a candidate\n  or not.\n\nPrototype / Proof of Concept plugins\n------------------------------------\n\nThese plugins were thrown together in experimentation. Some may be worth\ncleaning up, but others are useful pretty rarely.\n\n- The ``abcalc`` plugin performs the same calculation as absubmit, but runs it\n  only against non-MusicBrainz tracks, and stores the low level values rather\n  than submitting them. I've used this to populate the acoustic fingerprint\n  tags for use by external de-duplication scripts.\n- The ``existingqueries`` plugin adds a couple queries that originated in the\n  beets source.\n- The ``hasart`` plugin adds a query to check for embedded album art.\n- The ``inlinehook`` plugin lets you define hooks inline in config.yaml with\n  python, much the way ``inline`` does for fields.\n- The ``last_import`` plugin keeps track of the most recently imported items\n  with a flexible field.\n- The ``modifytmpl`` plugin lets you define fields using templates / format\n  strings. This will be going upstream into the main ``modify`` command.\n- The ``otherqueries`` plugin defines other random queries of questionable\n  usefulness at this time.\n- The ``spotifyexplicit`` plugin uses the ``spotify`` plugin to look up items\n  from my library, determines if Spotify considers these items as explicit\n  tracks (Parental Advisory), and prints them if so. I use this to set an\n  ``advisory`` field on my tracks.\n\n\n.. _beets: http://beets.io/\n.. _Alias Plugin: docs/alias.rst\n.. _Import Inspect Plugin: docs/importinspect.rst\n.. _Modify On Import Plugin: docs/modifyonimport.rst\n.. _Replace Format Plugin: docs/replaceformat.rst\n.. _Saved Formats Plugin: docs/savedformats.rst\n.. _Saved Queries Plugin: docs/savedqueries.rst\n",
    'author': 'Christopher Larson',
    'author_email': 'kergoth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kergoth/beets-kergoth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.8.*',
}


setup(**setup_kwargs)
