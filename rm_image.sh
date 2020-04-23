#!/bin/bash
#
# only keep the last 5 image files in /var/www/image, and delete the rest older ones
#

find /var/www/image/ -maxdepth 1 -type f -name "image*" -print | sort  | head -n -5 | xargs /bin/rm -f
