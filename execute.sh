#!/usr/bin/env bash

app_path="`dirname $(realpath $0)`"
$app_path/.venv/bin/python3 $app_path/__main__.py $@