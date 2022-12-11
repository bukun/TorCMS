
#. ~/usr/vpy_csw/bin/activate && cd zz_pycsw_drr \
#	&& pycsw-admin.py load-records -c default_svr.cfg -p ~/gitee/TorCMS/torcms_dde/helper_metadata/catalogued/xx_xml/
#

# DRRKS本身

#. ~/usr/vpy_csw/bin/activate && cd zz_pycsw_drr \
#	&& pycsw-admin.py load-records -c default_svr.cfg -p /home/bk/gitee/TorCMS/xx_xml

# WDCRRE 到DRR库


. ~/usr/vpy_csw/bin/activate && cd zz_pycsw_drr \
	&& pycsw-admin.py load-records -c default_svr.cfg -p /home/bk/gitee/TorCMS/torcms_dde/helper_metadata/wdcrre/xx_xml



# WDCRRE,到独立库

#. ~/usr/vpy_csw/bin/activate && cd zz_pycsw_wdc \
#	&& pycsw-admin.py load-records -c default_wdc.cfg -p /home/bk/gitee/TorCMS/torcms_dde/helper_metadata/wdcrre/xx_xml
