import os
import io
import zipfile

from notebook.base.handlers import APIHandler, path_regex
from notebook.notebookapp import NotebookWebApplication
from notebook.utils import url2path, url_path_join


def setup_handlers(web_app: NotebookWebApplication):
    """Setup all handlers for the CoSApp project actions.

    Parameters
    ----------
    web_app : notebook.notebookapp.NotebookWebApplication
        The notebook web application
    """
    host_pattern = ".*$"

    def build_url(url_extension: str) -> str:
        return url_path_join(web_app.settings["base_url"], url_extension)

    # End point order is important because they determine the order of resolution; knowing that the
    # latest catches every match of the previous ones.
    web_app.add_handlers(
        host_pattern,
        [
            (build_url(r"/download-folder{:s}".format(path_regex)), DownloadFolderHandler),
        ],
    )

class DownloadFolderHandler(APIHandler):
    
    def get(self, path):
        cm = self.contents_manager
        fullpath = os.path.join(cm.root_dir, url2path(path))

        # Headers
        paths = os.path.split(fullpath)
        name = paths[-1]
        zip_filename = name + '.zip'
        self.set_attachment_header(zip_filename)
        self.set_header('Content-Type', 'application/zip')

        # Prepare the zip file
        zip_buffer = io.BytesIO()
        zipf = zipfile.ZipFile(zip_buffer, mode='w', compression=zipfile.ZIP_DEFLATED)

        prefix = os.path.join(*paths[:-1])
        for root, dirs, files in os.walk(fullpath):
            relative = os.path.relpath(root, prefix)
            for file in files:
                zipf.write(os.path.join(root, file), os.path.join(relative, file))

        zipf.close()

        # Return the buffer value as the response
        self.finish(zip_buffer.getvalue())
