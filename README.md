1. Clone this repo
2. `cp env.template .env`
3. `date | md5sum` to generate passwords for .env file
4. Fill in ip address field `ip addr` or `ifconfig`
5. `docker-compose -f development.yml up`
6. `./init-host.sh`
7. `DOMAIN_NAME=whatever.com ./init-selfsigned.sh`
8. Setup Wordpress: Visit https://whatever.com/wp-admin 
9. Login, activate plugins, pick a theme, create menu called primary and add pages to it
10. Set permalinks to Post name
11. Create django database and user, enter `dc exec db mysql -u root -p`, password is mysql root password in .env
12. `CREATE USER 'django'@'%' IDENTIFIED BY 'password from .env';`
13. `CREATE DATABASE django;`
14. `GRANT ALL PRIVILEGES ON django . * TO 'django'@'%';`
15. `dc exec django python manage.py migrate`
16. `dc exec django python manage.py createsuperuser`
17. The `frontend` service doesn't reliably build. Try duplicating `RUN npm install'.
18. ...

At this point you should be up and running. Check with `dc ps` to see if aany services aren't running. Optionally, `DOMAIN_NAME=whatever.com ./init-letsencrypt.sh`