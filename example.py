import logging
import time
from concurrent import futures

import grpc

import example_pb2 as ex_pb
import example_pb2_grpc as ex_grpc


# testable with (in this file's directory):
# grpc_cli --protofiles=example.proto call localhost:50051 Hello "a: 'a'"


class ExampleServicer(ex_grpc.ExampleServicer):
    def Hello(self, request, context: grpc.ServicerContext):
        i = 0
        while context.is_active():
            time.sleep(0.5)
            bar = ex_pb.Bar()
            bar.b = f"bar - {i}"
            print(f"yielding {i}")
            yield bar
            print(f"yielded {i}")
            i += 1
        print("exiting")


def serve():
    servicer = ExampleServicer()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ex_grpc.add_ExampleServicer_to_server(servicer, server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    serve()
