sudo apt install -y supervisor

#if [ -e /etc/nginx/sites-enabled/ng_torcms_amis.nginx ]
#  then sudo rm /etc/nginx/sites-enabled/ng_torcms_amis.nginx
#fi
#
#if [ -e /etc/supervisor/conf.d/spv_torcms.conf ]
#  then sudo rm /etc/supervisor/conf.d/spv_torcms.conf
#fi

sudo cp `pwd`/ng_torcms_amis.nginx /etc/nginx/sites-enabled/ng_torcms_amis.nginx
sudo cp `pwd`/spv_torcms.conf /etc/supervisor/conf.d/spv_torcms.conf

sudo chmod 755 /etc/nginx/sites-enabled/ng_torcms_amis.nginx
sudo chmod 755 /etc/supervisor/conf.d/spv_torcms.conf


sudo supervisorctl reload
sudo service nginx restart

sudo supervisorctl status