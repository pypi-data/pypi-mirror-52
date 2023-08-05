# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from grakn_protocol.session import Session_pb2 as session_dot_Session__pb2


class SessionServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.open = channel.unary_unary(
        '/session.SessionService/open',
        request_serializer=session_dot_Session__pb2.Session.Open.Req.SerializeToString,
        response_deserializer=session_dot_Session__pb2.Session.Open.Res.FromString,
        )
    self.close = channel.unary_unary(
        '/session.SessionService/close',
        request_serializer=session_dot_Session__pb2.Session.Close.Req.SerializeToString,
        response_deserializer=session_dot_Session__pb2.Session.Close.Res.FromString,
        )
    self.transaction = channel.stream_stream(
        '/session.SessionService/transaction',
        request_serializer=session_dot_Session__pb2.Transaction.Req.SerializeToString,
        response_deserializer=session_dot_Session__pb2.Transaction.Res.FromString,
        )


class SessionServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def open(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def close(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def transaction(self, request_iterator, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_SessionServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'open': grpc.unary_unary_rpc_method_handler(
          servicer.open,
          request_deserializer=session_dot_Session__pb2.Session.Open.Req.FromString,
          response_serializer=session_dot_Session__pb2.Session.Open.Res.SerializeToString,
      ),
      'close': grpc.unary_unary_rpc_method_handler(
          servicer.close,
          request_deserializer=session_dot_Session__pb2.Session.Close.Req.FromString,
          response_serializer=session_dot_Session__pb2.Session.Close.Res.SerializeToString,
      ),
      'transaction': grpc.stream_stream_rpc_method_handler(
          servicer.transaction,
          request_deserializer=session_dot_Session__pb2.Transaction.Req.FromString,
          response_serializer=session_dot_Session__pb2.Transaction.Res.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'session.SessionService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
