from pathlib import Path
import re
import json
import mimetypes
import logging
import aiohttp
from aiohttp import web
from aiohttp.client_exceptions import ClientConnectorError


class WebpackManifest:
    MSG_1 = 'Webpack is compiling'
    MSG_404 = 'Webpack manifest file not found'
    MSG_502 = 'Can\'t connect to webpack server'

    def __init__(self, path,
                 static_url='/static/',
                 static_path='./static/',
                 assets_path=None):

        self.log = logging.getLogger()
        self.path = Path(path)
        self.data = None
        self.check_status()

        self.assets_path = Path(assets_path) if assets_path else self.path.parent / 'assets'
        self.static_url = static_url
        self.static_path = Path(static_path)
        self.public_path = None
        self.update()
        self.default_entry = 'app'

    def check_status(self):
        if not self.path.exists():
            self.log.warning(f"WARN! {self.MSG_404}: '{self.path}'")
            return self.make_message(self.MSG_404)

        if not self.data:
            return self.make_message(self.MSG_1)

        return 'ready'

    @staticmethod
    def make_message(text):
        return {
            'css': f'<style>body::before{{ \
                                    content: "{text}!";\
                                    font: 2rem bold;\
                                }}</style>',
            'js': f'<script>console.warn("{text}!")</script>',
        }

    def load_data(self):
        if self.path.exists():
            return json.loads(self.path.read_bytes().decode()).get('chunks')

    def update(self):
        if not self.public_path and self.path.exists():
            manifest = json.loads(self.path.read_bytes().decode())
            if 'error' in manifest:
                self.log.error(
                    f'Webpack Manifest Error: {manifest["error"]}\n{manifest.get("message")}')

            self.public_path = manifest.get('publicPath')
        self.data = self.load_data()

    def _get_tag(self, ext, entry=None):
        entry = entry or self.default_entry

        for item in self.data[entry]:
            if item['name'].endswith(ext):
                src = (self.static_url + item['name']).replace('//', '/')
                if ext == '.js':
                    return f'<script src="{src}"></script>'
                if ext == '.css':
                    return f'<link rel="stylesheet" type="text/css" href="{src}" />'

    def get_js_tag(self, entry=None):
        return self._get_tag('.js', entry) or ''

    def get_css_tag(self, entry=None):
        return self._get_tag('.css', entry) or ''

    def find(self, path):
        for entry in self.data:
            for item in self.data[entry]:
                if path == item['name'] or path == item['publicPath']:
                    return item['publicPath']

    def get_links(self):
        self.update()

        status = self.check_status()
        if status != 'ready':
            return status

        return {
            'css': self.get_css_tag(),
            'js': self.get_js_tag(),
        }

    @staticmethod
    def _get_static(path):
        file_path = Path(path)

        if file_path.exists():
            return {
                'body': file_path.read_bytes(),
                'content_type': mimetypes.MimeTypes().guess_type(str(file_path))[0],
            }

    async def proxy(self, request, path=None):
        if not path:
            path = self.public_path + re.sub(r'^/', '', request.raw_path)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(path) as res:
                    raw = await res.text()

                    return web.Response(text=raw,
                                        status=res.status,
                                        headers=res.headers)
        except ClientConnectorError:
            self.log.error(f'ERROR! {self.MSG_502}! path: {path}')
            return web.Response(text='', status=502)

    async def handle_static(self, request):
        path = request.match_info['path']

        if not path:
            return web.Response(status=404)

        static = self._get_static(self.static_path / path)
        if static:
            return web.Response(**static)

        static = self._get_static(self.assets_path / path)
        if static:
            return web.Response(**static)

        self.update()

        if self.data:
            wb_path = self.find(path)

            if wb_path and wb_path.startswith('http'):
                return await self.proxy(request, wb_path)

        return web.Response(text='', status=404)
