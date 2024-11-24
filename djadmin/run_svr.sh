# 使用uwsgi运行。
#
uwsgi --http 0.0.0.0:6799  --file mysite/wsgi.py --static-map /static=/home/dev/coding/cms-vue/django_admin/static
