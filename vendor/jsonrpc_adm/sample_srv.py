from aiohttp import web

from vendor.jsonrpc_adm.server import server_app


class RPCMethods:
    def ping(self):
        return "pong"

    async def aping(self):
        return "ponga"


if __name__ == "__main__":
    methods = RPCMethods()
    app = server_app(methods)
    web.run_app(app)
