import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from "@jupyterlab/application";
import { URLExt } from "@jupyterlab/coreutils";
import { IFileBrowserFactory, FileBrowser } from "@jupyterlab/filebrowser";
import { ServerConnection } from "@jupyterlab/services";
import { JSONObject } from "@phosphor/coreutils";
import { toArray } from "@phosphor/algorithm";
import { showErrorMessage } from "@jupyterlab/apputils";

// API end point
const API = "download-folder";
// Archive format
const FORMAT = "zip";

namespace CommandIDs {
  export const downloadFolder = "jupyterlab-downloadfolder:download";
}

function zipAndDownload(browser: FileBrowser): void {
  const items = toArray(browser.selectedItems());
  if (items.length > 1) {
    showErrorMessage(
      "Error downloading a folder",
      "Multiple selections for archiving a folder is not supported."
    );
    return;
  }
  const path = items[0].path;

  const settings = ServerConnection.makeSettings();
  let baseUrl = settings.baseUrl;

  let url = URLExt.join(baseUrl, API, URLExt.encodeParts(path));
  let queryArgs: JSONObject = {
    format: FORMAT
  };
  const xsrfTokenMatch = document.cookie.match("\\b_xsrf=([^;]*)\\b");
  if (xsrfTokenMatch) {
    queryArgs["_xsrf"] = xsrfTokenMatch[1];
  }
  url += URLExt.objectToQueryString(queryArgs);

  let element = document.createElement("a");
  document.body.appendChild(element);
  element.setAttribute("href", url);
  // Chrome doesn't get the right name automatically
  const parts = path.split("/");
  const name = parts[parts.length - 1] + "." + FORMAT;
  element.setAttribute("download", name);
  element.click();
  document.body.removeChild(element);
}

/**
 * Initialization data for the jupyterlab-downloadfolder extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: "jupyterlab-downloadfolder",
  autoStart: true,
  activate: (app: JupyterFrontEnd, factory: IFileBrowserFactory) => {
    const { commands } = app;

    commands.addCommand(CommandIDs.downloadFolder, {
      execute: () => {
        zipAndDownload(factory.defaultBrowser);
      },
      iconClass: "jp-MaterialIcon jp-DownloadIcon",
      label: "Download folder as archive"
    });

    app.contextMenu.addItem({
      command: CommandIDs.downloadFolder,
      selector: '.jp-DirListing-item[data-isdir="true"]',
      rank: Infinity
    });
  },
  requires: [IFileBrowserFactory]
};

export default extension;
