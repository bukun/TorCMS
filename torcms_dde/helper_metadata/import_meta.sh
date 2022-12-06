cd ~/deploy/pycsw
more ~/deploy/dde/helper_metadata/import_meta.sh
source ~/vpy_csw/bin/activate && pycsw-admin.py load-records -c default.cfg -p  \
  /home/bk/deploy/dde/helper_metadata/dde_dby/xx_xml
cd ~/deploy/dde