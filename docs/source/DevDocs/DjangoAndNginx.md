# Django and Nginx

Using nginx to be a web server for a Django project.

## Requirements

*   Install uwsgi library with pip into the Django virtual environment.

*   Install nginx (I used homebrew)

*   Configure the nginx configuration file
    * Nginx only looks for configuration files in certain places
    * Nginx only writes log files in certain places
        *   I needed to manually create the log directory.

### Nginx configuration file (sample)

```
    worker_processes 2;
    
    error_log  logs/error.log;
    error_log  logs/error.log  notice;
    error_log  logs/error.log  info;
    
    pid        logs/nginx.pid;
    
    events {
        worker_connections  1024;
    }
    
    http {
        include       mime.types;
        default_type  application/octet-stream;
    
        log_format  main  '$remote_addr - $remote_user [$time_local] "$request" | '
                          '$status | $body_bytes_sent | "$http_referer" | '
                          '"$http_user_agent" | "$http_x_forwarded_for"';
    
        access_log  logs/access.log  main;
    
        sendfile        on;
        #tcp_nopush     on;
    
        #keepalive_timeout  0;
        keepalive_timeout  65;
    
        #gzip  on;
    
        server {
            listen 127.0.0.1:8080;
            server_name  localhost;
    
            access_log  logs/host.access.log  main;
    
            location / {
                include uwsgi_params;
                uwsgi_pass 127.0.0.1:8765;
            }
    
        }
    }
```

*   Uwsgi Info

Uwsgi provides the link between Django and the web server(e.g. nginx)



### uwsgi

* uwsgi command line for following configuration

``` 
    uwsgi --yaml uwsgi_conf.yaml 
``` 

* uwsgi Configuration File (e.g. sample)

```
    # uwsgi_conf.yaml - Configure wsgi
    %YAML 1.2
    ---
    version: 1
    
    uwsgi:
        # Django-related settings
        # chdir : '/Volumes/MBPC/Dvl/Python/PythonProjects/Food-Pantry-Inventory
        # -Others/Food-Pantry-Inventory-Jan/'
    
        # Django's wsgi file'
        wsgi-module : 'FPIDjango/wsgi.py'
        # home : '/Volumes/MBPC/Dvl/Python/PythonProjects/Food-Pantry-Inventory
        # -Others/Food-Pantry-Inventory-Jan/'
        # Enable python threading
        enable-threads : True
    
        # process-related settings
        # master
        master : True
    
        # maximum number of worker processes
        processes : 4
    
        # use http style interface on a particular port
        http : 8765

```
