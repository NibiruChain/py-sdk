#!/bin/bash
set -e
pkg_dir="pysdk"
poetry run pdoc $pkg_dir -o=docs-md -f --skip-errors
mv docs-md/$pkg_dir tmp
rm -rf docs-md
mv tmp docs-md
