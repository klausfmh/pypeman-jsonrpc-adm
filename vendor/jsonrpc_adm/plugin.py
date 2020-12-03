# import asyncio
import logging

# from inspect import getmembers
# from inspect import isfunction

# from ajsonrpc import __version__ as ajsonrpc_version
# from ajsonrpc.dispatcher import Dispatcher
# from ajsonrpc.manager import AsyncJSONRPCResponseManager
# from ajsonrpc.core import JSONRPC20Request

from pypeman.conf import settings
from pypeman.endpoints import SocketEndpoint
from pypeman.plugins.base import BasePlugin

from vendor.jsonrpc_adm.server import server_app
from vendor.jsonrpc_adm.rpc_methods import RPCMethods


logger = logging.getLogger(__name__)
DEFAULT_SETTINGS = dict(
    sock="0.0.0.0:8899",
    reuse_port=False,
    verify=False,
    )


class JsonRPCAdmin(BasePlugin):
    """
    service providing a JSON RPC service to control pypeman
    """
    def __init__(self):
        super().__init__()
        cfg = dict(DEFAULT_SETTINGS)
        cfg.update(dict(settings.JSON_RPC_ADMIN_CFG))
        logger.debug("CFG = %s", cfg)
        self.sock = SocketEndpoint.normalize_socket(cfg["sock"])
        self.reuse_port = cfg["reuse_port"]
        self.http_args = cfg.get("http_args") or {}
        self.ssl_context = self.http_args.pop("ssl_context", None)
        self.verify = cfg["verify"]
        self.app = None

    def ready(self):
        rpc_methods = RPCMethods()
        self.app = server_app(
            http_args=self.http_args,
            rpc_methods=rpc_methods,
            )

    async def start(self):
        logger.debug("do_start")
        sock = SocketEndpoint.mk_socket(self.sock, self.reuse_port)
        self.srv = await self.loop.create_server(
            protocol_factory=self.app.make_handler(),
            sock=sock,
            ssl=self.ssl_context,
            )
        logger.debug("server created")
        return self.srv

    async def stop(self):
        logger.debug("do_stop")
