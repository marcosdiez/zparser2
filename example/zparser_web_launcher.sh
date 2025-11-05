#!/bin/bash
set -e
# source web/env/bin/activate
flask --app zparser_web run --host 0.0.0.0 --reload