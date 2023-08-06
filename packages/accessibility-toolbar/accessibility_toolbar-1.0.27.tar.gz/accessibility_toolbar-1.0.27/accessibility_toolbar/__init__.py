import pkg_resources

__version__ = pkg_resources.require("accessibility_toolbar")[0].version
version_info = pkg_resources.parse_version(__version__)

def _jupyter_nbextension_paths():
    return [dict(section="notebook",
                 src="static",
                 dest="accessibility_toolbar",
                 require="accessibility_toolbar/static/main")]