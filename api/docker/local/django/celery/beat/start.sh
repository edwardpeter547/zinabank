#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

python manage.py migrate django_celery_beat

rm -f './celerybeat.pid'

exec honcho start beat