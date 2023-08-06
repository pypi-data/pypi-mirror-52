from copy import copy

from scrapyd.utils import native_stringify_dict
from scrapyd.webservice import WsResource

from .eggstorage import FilesystemEggStorage


class ListVersions(WsResource):
    def render_GET(self, txrequest):
        args = native_stringify_dict(copy(txrequest.args), keys_only=False)
        project = args['project'][0]
        versions = FilesystemEggStorage().list(project)
        return {"node_name": self.root.nodename, "status": "ok", "versions": versions}
