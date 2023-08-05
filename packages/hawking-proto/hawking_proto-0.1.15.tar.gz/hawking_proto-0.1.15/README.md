# Hawking Protobuf gRPC Package

A package that contains Hawking python proto messages and gRPC stubs.

## Generating *_pb2[_gprc].py

```
pip install grpcio-tools
python run_codegen.py
```

## Python3 Known Issue

The generated _grpc.py reference relative pb2, using grpc from different folder does not work with python3.

The work-around is to add hawking_proto.hawking_pb2 to the import statement.

