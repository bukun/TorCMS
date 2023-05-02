sudo rm /etc/nginx/sites-enabled/ng_torcms_amis.nginx
sudo rm /etc/supervisor/conf.d/spv_torcms.conf


sudo ln -s `pwd`/ng_torcms_amis.nginx /etc/nginx/sites-enabled/ng_torcms_amis.nginx
sudo ln -s `pwd`/spv_torcms.conf /etc/supervisor/conf.d/spv_torcms.conf

sudo chmod 755 /etc/nginx/sites-enabled/ng_torcms_amis.nginx
sudo chmod 755 /etc/supervisor/conf.d/spv_torcms.conf


