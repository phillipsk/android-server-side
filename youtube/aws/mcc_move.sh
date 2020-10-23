#!/bin/bash

python3 /home/bk/api/youtube/PROD/mcc_download.py

sourcedir=/home/bk/api/youtube/PROD
destdir=/var/www/html/god.works/public_html/mp3

for f in "$sourcedir"/*.mp3; do
      printf 'Will move %s to %s\n' "$f" "$destdir"
      mv "$f" "$destdir"
done

#for f in "$destdir"/*.mp3; do
#      printf 'Will move %s to %s\n' "$f" "${f//_//}"
#      rename "s/_///g" *
#done

#rename -n "s/_//g" /var/www/html/god.works/public_html/mp3/*
find /var/www/html/god.works/public_html/mp3/archive/ -type f -name *.mp3 -mtime +21 -exec mv {} /home/bk/mp3_backups \;
find /var/www/html/god.works/public_html/mp3/ -type f -name "*.mp3" -mtime +21 -exec mv {} /var/www/html/god.works/public_html/mp3/archive \;
#find /var/www/html/god.works/public_html/mp3/ -type f -name "*.mp3" -mtime +7 -exec ls -haltr ;
# -mtime +7 -exec mv {} /archive ;
#find . \( -iname '*.mp3' \) -exec mv {} path/to/Directory2/ \;

#  bash /home/bk/api/youtube/PROD/mcc_move.sh
#*/1 * * * * bk echo "job every minute"
*/5  *    *    *    * bash /home/bk/api/youtube/PROD/mcc_move.sh
*/20 *    *    *    *    echo "job every minute"

