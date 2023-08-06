from ._version import version_info, __version__

from .scdgviewer import *

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'scdg-viewer',
        'require': 'scdg-viewer/extension'
    }]
