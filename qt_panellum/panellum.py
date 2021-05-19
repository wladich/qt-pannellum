# coding: utf-8
import os
import json
import binascii

import pkg_resources
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl


class Panellum(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings = self.page().settings()
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        html_dir = pkg_resources.resource_filename(__name__, 'html')
        self.setUrl(QUrl('file://' + os.path.join(html_dir, 'index.html')))

    def eval_js(self, func, args=None):
        return self.page().runJavaScript('%s(%s)' % (func, json.dumps(args)))

    def init_viewer(self, config):
        panorama_url = config.get('panorama', '')
        local_prefix = 'file://'
        if panorama_url.startswith(local_prefix):
            with open(panorama_url[len(local_prefix):], 'rb') as f:
                config['panorama'] = 'data:;base64,' + binascii.b2a_base64(f.read()).decode('ascii')
        return self.eval_js('client.newViewer', config)

    def remove_viewer(self):
        self.eval_js('client.destroyViewer')
