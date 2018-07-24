sudo pip3 install --upgrade django
sudo rm -rf /etc/nginx/sites-enabled/default
sudo ln -sf /home/box/web/etc/nginx.conf  /etc/nginx/sites-enabled/test.conf
sudo /etc/init.d/nginx restart
# sudo ln -s /home/box/web/etc/hello.conf   /etc/gunicorn.d/hello
# sudo ln -s /home/box/web/etc/django.conf   /etc/gunicorn.d/django
# sudo /etc/init.d/gunicorn restart
# sudo /etc/init.d/mysql start
python3 ask/manage.py makemigrations
python3 ask/manage.py migrate --run-syncdb
python3 ask/manage.py runserver 0.0.0.0:8000