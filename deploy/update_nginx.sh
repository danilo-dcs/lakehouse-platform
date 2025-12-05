#!/bin/bash

CONF_PATH="$(pwd)"
cp $CONF_PATH/nginx/lakehouse.conf /etc/nginx/sites-available/lakehouse_infra.conf # copying the file
ln -s /etc/nginx/sites-available/lakehouse_infra.conf /etc/nginx/sites-enabled/ # creating the symbolic link
nginx -t
systemctl restart nginx
