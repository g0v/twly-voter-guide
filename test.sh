#!/bin/bash
coverage run manage.py test --settings=ly.test
coverage html --include="$(pwd)*" --omit="admin.py, local_settings.py"
