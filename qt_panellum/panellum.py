# coding: utf-8
import binascii
import json
import os

import pkg_resources
from PyQt5.QtCore import QUrl
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebView


def file_to_data_url(path):
    with open(path, "rb") as f:
        raw_data = f.read()
        encoded = binascii.b2a_base64(raw_data, newline=False)
        return "data:image/jpeg;base64," + encoded.decode()


class Panellum(QWebView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings = self.page().settings()
        settings.setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        settings.setAttribute(QWebSettings.LocalContentCanAccessFileUrls, False)
        settings.setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True)

        html_dir = pkg_resources.resource_filename(__name__, "html")
        self.setUrl(QUrl("file://" + os.path.join(html_dir, "index.html")))

    def eval_js(self, func, args=None):
        js_script = "%s(%s)" % (func, json.dumps(args))
        return self.page().mainFrame().evaluateJavaScript(js_script)

    def init_viewer(self, config):
        panorama_url = config.get("panorama", "")
        local_prefix = "file://"
        if panorama_url.startswith(local_prefix):
            path = panorama_url[len(local_prefix) :]
            config["panorama"] = file_to_data_url(path)
        return self.eval_js("client.newViewer", config)

    def remove_viewer(self):
        self.eval_js("client.destroyViewer")

    def viewer_command(self, method, *args):
        return self.eval_js("client.viewerCommand", [method] + list(args))
