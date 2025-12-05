# NGINX

## Installation steps

1. To install nginx on APT (Debian/Ubuntu) based systems:

```
sudo apt update
sudo apt install nginx
```

2. To install NGINX on RPM based systems (CentOS/RHEL/Fedora)

```
sudo yum install epel-release # For CentOS and RHEL
sudo yum install nginx
```

3. Adjust Firewall (if necessary):

```
sudo ufw allow 'Nginx HTTP'
sudo ufw status
```

or alternatively:

```
sudo firewall-cmd --permanent --zone=public --add-service=http
sudo firewall-cmd --permanent --zone=public --add-service=https
sudo firewall-cmd --reload
```

4. To start NGINX:

```
sudo systemctl start nginx
sudo systemctl enable nginx
```

## Set up steps

### Lakehouse Server

1. Create a new file in `/etc/nginx/sites-available` and copy the content from the `lakehouse.conf` file ([link](./sites-available/lakehouse.conf)) to it.

```
sudo nano /etc/nginx/sites-available/lakehouse.conf
```

2. Create the simbolic link to the lakehouse.conf file in the `/etc/nginx/sites-enabled`:

```
sudo ln -s /etc/nginx/sites-available/lakehouse.conf /etc/nginx/sites-enabled/
```

3. Verify the symbolic link:

```
ls -l /etc/nginx/sites-enabled/
```

### Max Body Size (optional)

Change the client_max_body_size to make sure NGINX's allows large files transfer, on all the server blocks.

1. Open the nginx.conf file

```
sudo nano /etc/nginx/nginx.conf # or sudo vim /etc/nginx/nginx.conf
```

2. Add or modify the `client_max_body_size` directive globally

```
http {
    ...
    client_max_body_size 50M;
    ...
}
```

### Restart NGINX

To apply any changes, restart nginx:

```
sudo systemctl restart nginx
```
