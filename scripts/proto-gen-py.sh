#!/usr/bin/env bash
set -e pipefail # see https://stackoverflow.com/a/68465418/13305627

# ------------------------------------------------ CONFIG
PKG_DIR_NAME="nibiru_proto"
nibiru_cosmos_sdk_version="v0.47.4"
nibiru_chain_version="v0.21.10"
# ------------------------------------------------

init_globals() {
  GEN_PY_REPO=$(pwd)
  PKG_PATH=$GEN_PY_REPO/$PKG_DIR_NAME
  cd ../nibiru
  NIBIRU_PATH=$(pwd)
  echo "GEN_PY_REPO: $GEN_PY_REPO"
  echo "PKG_PATH: $PKG_PATH"
  echo "NIBIRU_PATH: $NIBIRU_PATH"
}

init_globals

# Add PKG_PATH as dir if it doesn't exist.
clean_repo() {
  cd $GEN_PY_REPO
  rm -rf ./proto/
  rm -rf ./nibiru/
  rm -rf $PKG_PATH
  mkdir $PKG_PATH

  # add directories to package path for Python imports
  echo > $PKG_PATH/__init__.py
  printf "import os\n\
import sys\n\n\
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))\n\
version = '${nibiru_chain_version:1}'\n" > $PKG_PATH/__init__.py
}

copy_nibiru_protobuf_from_remote() {
  git clone --depth 1 --branch $nibiru_chain_version https://github.com/NibiruChain/nibiru.git
  cp -r ./nibiru/proto/ ./proto/
  cp ./nibiru/go.mod go.mod
  cp ./nibiru/go.sum go.sum
}

copy_nibiru_protobuf_from_local() {
  cd $NIBIRU_PATH      # move to nibiru
  git checkout $nibiru_chain_version
  cd $GEN_PY_REPO      # move to py-sdk
  cp -r $NIBIRU_PATH/proto $GEN_PY_REPO/$PKG_DIR_NAME
  cp $NIBIRU_PATH/go.mod $GEN_PY_REPO/go.mod
  cp $NIBIRU_PATH/go.sum $GEN_PY_REPO/go.sum
}

create_py_typed_file() {
  # A `py.typed` file should be included in any distribution at the root of the
  # package whenever you want to signal that the package is "type hinted" or
  # "type annotated", meaning that it supports type checking.
  #
  # This is part of PEP 561 -- Distributing and Packaging Type information See:
  # https://peps.python.org/pep-0561/
  #
  # Without the `py.typed` file, a package is assumed not to be type-safe such
  # that, even if the pacakge has type annotations, type checkers like mypy and
  # most LSPs will ignore them when type checking other projects that use the
  # package in question.
  #
  # The py.typed file itself can be empty; its presence is the important part.
  cd $GEN_PY_REPO      # move to py-sdk
  touch $GEN_PY_REPO/$PKG_DIR_NAME/py.typed
}

go_get_from_cosmos() {
  if ! grep "github.com/gogo/protobuf => github.com/regen-network/protobuf" go.mod &>/dev/null; then
    echo -e "\tPlease run this command from somewhere inside the cosmos-sdk folder."
    return 1
  fi

  # get protos: cosmos-sdk
  go get github.com/cosmos/cosmos-sdk@$nibiru_cosmos_sdk_version
  # get protos: cosmos-proto
  go get github.com/cosmos/cosmos-proto

  # get protoc gocosmos plugin
  # DEPRECATED: cosmos-proto was previously maintained by regen network.
  # go get github.com/regen-network/cosmos-proto/protoc-gen-gocosmos@latest 2>/dev/null
}

code_gen() {
  echo "grabbing cosmos-sdk proto file locations from disk"
  cd $NIBIRU_PATH
  go_get_from_cosmos
  dir_cosmos_sdk=$(go list -f '{{ .Dir }}' -m github.com/cosmos/cosmos-sdk)

  echo "grab all of the proto directories"
  cd $GEN_PY_REPO

  proto_dirs=()
  proto_dirs+=("$dir_cosmos_sdk/proto")
  proto_dirs+=("$NIBIRU_PATH/proto")

  echo "Proto Directories: "
  echo $proto_dirs

  # generate the protos for each directory
  for proto_dir in "${proto_dirs[@]}"; do
    string=$proto_dir
    prefix=$HOME/go/pkg/mod/github.com/
    prefix_removed_string=${string/#$prefix/}
    echo "------------ generating $prefix_removed_string ------------"
    # echo "$dir_cosmos_sdk"

    echo "proto_dir: ${proto_dir}"

    echo "NIBIRU_PATH: $NIBIRU_PATH"
    local out_dir=$PKG_PATH
    echo "out_dir: $out_dir"

    if [ ! buf ]; then
      echo "Please install buf to generate protos."
      exit 1
    fi
    buf generate $proto_dir --template $NIBIRU_PATH/proto/buf.gen.py.yaml \
      -o $out_dir \
      --config $NIBIRU_PATH/proto/buf.yaml \
      --include-imports
  done

  echo "Complete - generated Python types from proto"
}

final_cleanup() {
  echo "final cleanup"
  cd $GEN_PY_REPO
  # -z "$var" to check for empty
  # -n "$var" to check for not empty
  if [ -n "$GEN_PY_REPO" ]; then
    rm -rf $GEN_PY_REPO/$PKG_DIR_NAME/home
    rm go.mod go.sum
  fi
  rm -rf $GEN_PY_REPO/$PKG_DIR_NAME/proto
}

rewrite_misnamed_import() {
  if [ ! find ]; then
    echo "Please install find."
    exit 1
  fi
  if [ ! sed ]; then
    echo "Please install sed."
    exit 1
  fi

  find . -name "*.py" -type f -exec sed -i "" 's/from nibiru\./from nibiru_proto.nibiru./g' {} \;

  find . -name "*.py" -type f -exec sed -i "" 's/import nibiru\./import nibiru_proto.nibiru./g' {} \;
}

# ------------------------------------------------
# __main__ : Start of script execution
# ------------------------------------------------


main() {
  clean_repo

  # copy_nibiru_protobuf_from_remote
  copy_nibiru_protobuf_from_local

  code_gen

  final_cleanup

  create_py_typed_file

  poetry run python scripts/pkg_create_inits.py
  rewrite_misnamed_import
}

if main; then
  echo "🔥 Generated Python proto types successfully. "
else
  echo "❌ Generation failed."
fi
