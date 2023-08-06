import grpc

from .lib.rpc_pb2 import PeerTopicInfo, PublishData, Data
from .lib.rpc_pb2_grpc import MeshStub
from .exp import MeshRPCException
from .util import getTopicsFromGeospace

class MeshRPC:
    def __init__(self, endpoint):
        c = grpc.insecure_channel(endpoint)
        self.stub = MeshStub(c)

    def subscribe(self, channel, geospace):
        topicList = getTopicsFromGeospace(channel, geospace)

        m = PeerTopicInfo()
        m.topics.extend(topicList)
        
        s = self.stub.Subscribe(m)

        return s

    def registerToPublish(self, channel, geospace):
        topicList = getTopicsFromGeospace(channel, geospace)

        m = PeerTopicInfo()
        m.topics.extend(topicList)

        try:
            p = self.stub.RegisterToPublish(m)
            return p
        except grpc.RpcError as e:
            raise MeshRPCException(e.details())

    def publish(self, channel, geospace, raw):
        topicList = getTopicsFromGeospace(channel, geospace)

        pd = PublishData()
        
        pd.info.topics.extend(topicList)
        pd.data.raw = raw

        try:
            res = self.stub.Publish(pd)
            return res
        except grpc.RpcError as e:
            raise MeshRPCException(e.details())
