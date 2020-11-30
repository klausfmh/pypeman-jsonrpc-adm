from functools import partial

import requests


class Client:
    def __init__(self, url):
        if "://" not in url:
            url = "http://" + url
        if not url.endswith("/"):
            url += "/"
        self.url = url
        self.ses = None
        self.cnt = 1

    def connect(self):
        self.ses = requests.Session()

    def post(self, data):
        """
        post data to url, add id if missing in data and
        parse result
        """
        if "id" not in data:
            data = dict(data)
            data["id"] = self.cnt
            self.cnt += 1
        rslt = self.ses.post(self.url, json=data)
        assert rslt.status_code == 200
        data = rslt.json()
        return data

    def call(self, method, *args, **kwargs):
        """
        calls a json RPC method with args or kwargs
        """
        assert not (args and kwargs)
        if args:
            params = args
        elif kwargs:
            params = kwargs
        else:
            params = []
        data = dict(
            jsonrpc="2.0",
            method=method,
            id=self.cnt,
            params=params,
            )
        self.cnt += 1
        rslt = self.post(data)
        return rslt

    def __getattr__(self, name):
        return partial(self.call, name)
