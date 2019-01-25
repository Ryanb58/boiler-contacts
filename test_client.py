from __future__ import print_function

import grpc

from protos import contacts_pb2
from protos import contacts_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('0.0.0.0:22222') as channel:
        stub = contacts_pb2_grpc.ContactServiceStub(channel)

        print('-'*20)
        print("LIST:")

        # Test the list endpoint.
        response = stub.List(contacts_pb2.ListContactsRequest(page_size=1, page_token="1"))
        for contact in response.contacts:
            print(contact)

        print('-'*20)


if __name__ == '__main__':
    run()
