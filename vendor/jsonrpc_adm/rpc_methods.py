from pypeman import channels
from pypeman import nodes
from pypeman.conf import settings
from pypeman.graph import mk_graph


class RPCMethods:
    def __init__(self):
        pass

    def ping(self):
        """
        ping function (mostly for debug)
        """
        return "pong"

    async def pinga(self):
        """
        asynchronous ping function (mostly for debug)
        """
        return "ponga"

    def graph(self, dot=False, json=False):
        """
        returns pypeman graph
        :param dot: if true text lines will be for a dot file
        :param json: return graph as json object. NOT IMPLEMENTED SO FAR
        """
        if json:
            raise NotImplementedError("json graph not implemented so far")
        lines = list(mk_graph(dot=dot))
        return lines

    def channels(self, name=None):
        """
        return info about all channels
        """
        chan_by_uuid = {}
        to_uuid = {}
        # TODO as code seems to force unique names, perhaps
        # better make  to_name and by_name ??
        rslt = dict(
            by_uuid=chan_by_uuid,
            to_uuid=to_uuid,
            )
        for channel in channels.all_channels:
            if name and name != channel.name:
                continue
            print(vars(channel).keys())
            uuid=channel.uuid.hex
            to_uuid[channel.name] = uuid
            if hasattr(channel, "as_json"):
                chan_by_uuid[uuid] = channel.as_json()
                continue
            parent = channel.parent
            nodes = []
            for node in channel._nodes:
                nodes.append(node.name)
            if parent:
                parent = parent.name
            as_dict = channel.to_dict()
            data = dict(
                name=channel.name,
                uuid=channel.uuid.hex,
                parent=parent,
                parent_uids=channel.parent_uids,
                status=as_dict["status"],
                has_message_store=as_dict["has_message_store"],
                processed_msgs=channel.processed_msgs,
                nodes=nodes,
                )
            chan_by_uuid[uuid] = data
        return rslt

    def nodes(self, name=None):
        """
        return info about all nodes
        """
        by_name = {}
        rslt = dict(
            by_name=by_name,
            )
        for node in nodes.all_nodes:
            name = node.name
            print(vars(node).keys())
            if hasattr(node, "as_json"):
                by_name[name] = node.as_json()
                continue
            data = dict(
                name=name,
                cls=node.__class__.__module__ + "." + node.__class__.__name__,
                fullpath=node.fullpath(),
                processed=node.processed,
                )
            by_name[name] = data
        return rslt

    def channel_info(self, name=None, uuid=None):
        """
        gets detailed channel info
        """
        return "NotImplemented"

    async def channel_start(self, name=None, uuid=None):
        """
        starts a given channel
        """
        return "NotImplemented"

    async def channel_stop(self, name=None, uuid=None):
        """
        stops a given channel
        """
        return "NotImplemented"

    async def channel_process(self, name=None, uuid=None):
        """
        let channel process a given message
        """
        return "NotImplemented"

    def node_info(self, name):
        """
        get detailed info about a node
        """
        return "NotImplemented"

    async def node_process(self, name, msg=None):
        return "NotImplemented"

    async def node_inject(self, name, msg=None):
        """
        inject message into a node and let it ripple through
        """
        return "NotImplemented"

    async def node_process(self, name, msg=None):
        """
        let node process a given message
        """
        return "NotImplemented"

    async def clear_break(self, name=None, uuid=None):
        """
        set breakpoint for a given node
        """
        return "NotImplemented"

    async def set_break(self, name):
        """
        set breakpoint for a given node
        """
        return "NotImplemented"

    async def step(self):
        """
        perform a single step
        """
        return "NotImplemented"

    async def continue_processing(self):
        """
        continues exection till next break
        """
        return "NotImplemented"

    def settings(self):

