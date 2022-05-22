#!/bin/bash
source /home/vscode/.profile
poetry install -E doc -E dev -E test
