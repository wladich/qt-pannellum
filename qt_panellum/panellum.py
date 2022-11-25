# coding: utf-8
import binascii
import json
import os
from typing import TypeAlias

import pkg_resources
from PyQt5.QtCore import QUrl
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QWidget
from typing_extensions import NotRequired, TypedDict


class Hotspot(TypedDict):
    yaw: float
    pitch: float
    type: str
    text: NotRequired[str]


PanellumConfig: TypeAlias = dict[str, float | str | list[Hotspot]]


def file_to_data_url(path: str) -> str:
    with open(path, "rb") as f:
        raw_data = f.read()
        encoded = binascii.b2a_base64(raw_data, newline=False)
        return "data:image/jpeg;base64," + encoded.decode()


class Panellum(QWebView):
    css: str | None = None

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        settings = self.page().settings()
        settings.setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        settings.setAttribute(QWebSettings.LocalContentCanAccessFileUrls, False)
        settings.setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True)

        html_dir = pkg_resources.resource_filename(__name__, "html")
        self.setUrl(QUrl("file://" + os.path.join(html_dir, "index.html")))
        if self.css:
            self.insert_style(self.css)

    def eval_js(self, func: str, args: object = None) -> object:
        js_script = "%s(%s)" % (func, json.dumps(args))
        result: object = self.page().mainFrame().evaluateJavaScript(js_script)
        return result

    def init_viewer(self, config: PanellumConfig) -> None:
        panorama_url = config.get("panorama", "")
        assert isinstance(panorama_url, str)
        local_prefix = "file://"
        if panorama_url.startswith(local_prefix):
            path = panorama_url[len(local_prefix) :]
            config["panorama"] = file_to_data_url(path)
        self.eval_js("client.newViewer", config)

    def remove_viewer(self) -> None:
        self.eval_js("client.destroyViewer")

    def viewer_command(self, method: str, *args: object) -> object:
        cmd_args = [method] + list(args)
        return self.eval_js("client.viewerCommand", cmd_args)

    def insert_style(self, css: str) -> None:
        func = """
        (function(css){
            function insertCss() {
                document.head.insertAdjacentHTML("beforeend", "<style>" + css + "</style>");
            }
            window.addEventListener('load', insertCss);
        })"""
        self.eval_js(func, css)
