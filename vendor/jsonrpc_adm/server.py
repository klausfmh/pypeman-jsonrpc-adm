from inspect import iscoroutinefunction

from aiohttp import web


from vendor.jsonrpc_adm.rpc_methods import RPCMethods


class RPCHandler:
    def __init__(self, rpc_methods):
        self.rpc_methods = rpc_methods
        # identify all coroutine functions or callables
        self.method_dict = methods = {}
        for name in (v for v in dir(rpc_methods) if not v.startswith("_")):
            entry = getattr(rpc_methods, name)
            if iscoroutinefunction(entry):
                methods[name] = entry, True
            elif callable(entry):
                methods[name] = entry, False

    async def post(self, request):
        data = await request.json()
        print("DATA", dict(data))
        version, method_name, id_, params = (data.get(key) for key in (
            "jsonrpc", "method", "id", "params"))
        assert version == "2.0"
        print(method_name)
        print(id_)
        print(params)
        args = params if isinstance(params, list) else []
        kwargs = params if isinstance(params, dict) else {}
        print("ARGS", args, "KWARGS", kwargs)
        methods = self.method_dict
        method_info = methods.get(method_name)
        result = dict(
                jsonrpc="2.0",
                id=id_,
            )
        if method_info is None:
            error = dict(
                code=-32601,
                message="unknown method %s" % method_name,
                )
            result["error"] = error
            return web.json_response(result)

        method, is_async = method_info
        try:
            if is_async:
                rslt = await method(*args, **kwargs)
            else:
                rslt = method(*args, **kwargs)
        except Exception:
            raise

        result["result"] = rslt

        return web.json_response(result)


def server_app(rpc_methods=None, http_args=None):
    if rpc_methods is None:
        rpc_methods = RPCMethods()
    http_args = http_args or {}

    app = web.Application(**http_args)
    rpc_handler = RPCHandler(rpc_methods)
    app.add_routes([
        web.get("/", rpc_handler.post),
        web.post("/", rpc_handler.post),
        ])
    return app
