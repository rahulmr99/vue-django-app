#!/usr/bin/env bash
echo "Copy nginx config..."
cp easy_nginx.conf /etc/nginx/sites-available/easy_nginx.conf
echo "Copy caddy config..."
cp Caddyfile /etc/caddy/caddyfile
echo "Copy supervisor config..."
cp easy_uwsgi.conf /etc/supervisor/conf.d/easy_uwsgi.conf
echo "Copy celary supervisor config..."
cp easy_preiodic_task.conf /etc/supervisor/conf.d/easy_preiodic_task.conf
echo "Copy celary flower config..."
cp easy_flower.conf /etc/supervisor/conf.d/easy_flower.conf
echo "Reread configuration supervisor config..."
supervisorctl reread
echo "Update configuration supervisor config..."
supervisorctl update
echo "Enable back-end site..."
sudo rm -v /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/easy_nginx.conf /etc/nginx/sites-enabled/easy_nginx.conf
