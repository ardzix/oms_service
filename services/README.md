python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. catalogue.proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. channel.proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. promo.proto