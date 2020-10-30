#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# find . -type f -name "*.py[co]" -delete
# find . -type d -name "__pycache__" -delete

# python manage.py compilemessages
python manage.py migrate users
python manage.py migrate
python manage.py collectstatic --noinput
