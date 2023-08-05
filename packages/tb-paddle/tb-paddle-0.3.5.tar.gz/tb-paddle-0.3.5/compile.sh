#!/bin/bash
set -ex

DESIRED_PROTO_VERSION="3.6.1"

# Download and use the latest version of protoc.
if [ "$(uname)" == "Darwin" ]; then
  PROTOC_ZIP="protoc-"$DESIRED_PROTO_VERSION"-osx-x86_64.zip"
else
  PROTOC_ZIP="protoc-"$DESIRED_PROTO_VERSION"-linux-x86_64.zip"
fi

WGET_BIN=`which wget`
if [[ ! -z ${WGET_BIN} ]]; then
  ${WGET_BIN} https://github.com/protocolbuffers/protobuf/releases/download/v"$DESIRED_PROTO_VERSION"/${PROTOC_ZIP}
  rm -rf protoc
  python -c "import zipfile; zipfile.ZipFile('"${PROTOC_ZIP}"','r').extractall('protoc')"
  PROTOC_BIN=protoc/bin/protoc
  chmod +x ${PROTOC_BIN}
fi

if [[ -n ${PROTOC_BIN} ]]; then
  echo "Delete all existing Python protobuf (*_pb2.py) output"
  rm -rf tb_paddle/proto/*_pb2.py
  ${PROTOC_BIN} tb_paddle/proto/*.proto --python_out=.
  echo "Done generating tb_paddle/proto/*_pb2.py"
else
  echo "protoc can't be installed, so tb_paddle/proto/*_pb2.py are using the precompiled version."
fi
