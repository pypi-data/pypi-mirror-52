"""
Python module to initialize Server Extension
"""
from ._version import __version__
from .handler import setup_handlers
from notebook.notebookapp import NotebookWebApplication


def _jupyter_server_extension_paths():
    """
    Function to declare Jupyter Server Extension Paths.
    """
    return [{
        'module': 'jupyterlab_downloadfolder',
    }]


def load_jupyter_server_extension(nbapp: NotebookWebApplication):
    """
    Function to load Jupyter Server Extension.
    Args:
        nbapp (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    setup_handlers(nbapp.web_app)
