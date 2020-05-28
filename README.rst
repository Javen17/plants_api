plants_api
==========

a Rest api on top of Django , that hopefully will be used in the 

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: MIT


Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy plants_api

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html





Deployment
----------

The following details how to deploy this application.

#Primero que nada creamos un nuevo usuario 
#Seteamos y revisamos firewall

sudo ufw app list
Allow OpenSSH
sudo ufw allow OpenSSH

# Activamos
sudo ufw enable

#Revisamos el estado
sudo ufw status


1 - Asegurarnos de tener los paquetes de repositorio de ubuntu actualizados asi mismo tener python3

sudo apt update

sudo apt upgrade

sudo apt install python-pip

#Seteamos nombre host
sudo hostnamectl set-hostname django-server

hostname

nano /etc/hosts

#agregamos la direccion ip a usar y ponemos el nombre designado a nuestro host
#o usamos una ya enlistada y cambiamos el host al nuevo

#ejemplo

127.0.0.1 localhost
127.0.1.1 django-server

#salimos y guardamos


#acontinuacion creamos un nuevo usuario para manejar django (como buena practica)

adduser 'nombre'

#llenamos la información
#salimos 
exit

#le damos root permisos 

sudo usermod -aG sudo 'nombre'

#y entramos 

ssh nombre@'direccion asignada a nuestro host'

#ejemplo

ssh usuarionuevo@127.0.1.1

sudo apt-get install ufw



sudo ufw default allow outgoing

sudo ufw allow ssh

sudo ufw allow 8000 

#o cual sea el port a correr

sudo ufw enable

sudo ufw status

#volvemos al usuario oficial
#Clonamos proyecto desde rama "release"

git clone --single-branch --branch release https://github.com/Javen17/plants_api

Entramos al proyecto y vemos las dependencias

cd plants_api

pip freeze

#ahora debemos crear un ambiente virtual 

sudo apt-get install python3-venv

#hacemos el ambiente en nuestra carpeta

python3 -m venv plants_api/venv

#le activamos

cd plants_api

source venv/bin/activate

#instalamos los requisitos

pip install -r requirements.txt



#Cambiamos configuraciones

sudo nano plants_api/base.py

#MODIFICAMOS EL ARRAY DE ALLOWED_HOSTS, E INCLUIMOS LA IP A USAR, O DOMINIO #EJEMPLO

ALLOWED_HOSTS = ['127.0.1.1']

TAMBIEN PUEDE USARSE '*', AUNQUE NO ES RECOMENDADO

#luego bajamos y justo sobre STATIC_URL, definimos STATIC_ROOT, que es donde los assets se #almacenaran

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#SALIMOS Y GUARDAMOS


python manage.py collectstatic


#vovlemos al origen

cd

#instalamos y configuramos apache2
sudo apt-get install apache2

sudo cd /etc/apache2/sites-available/
ls

#Usar uno de los archivos de configuración como punto de entrada del proyecto
#ejemplo

sudo cp 000-default.conf plants_api.conf

sudo nano plants_api.conf 


#bajar hasta justo antes de  </VirtualHost>
#y poner

Alias /static /home/"usuario"/plants_api/static
<Directory /home/"usuario"/plants_api/static>
Require all granted
</Directory>

Alias /media /home/"usuario"/plants_api/media
<Directory /home/"usuario"/plants_api/media>
Require all granted
</Directory>

<Directory /home/"usuario"/plants_api/media>
<Files wsgi.py>
Require all granted
</Files>
</Directory>

WSGIScriptAlias / /home/"usuario"/plants_api/plants_api/wsgi.py
WSGIDaemonProcess django_app python-path=/home/"usuario"/plants_api python-home=/home/"usuario"/plants_api/venv
WSGIProcessGroup django_app

#Guardamos
# regresamos al directorio root
cd

sudo a2ensite plants_api

sudo a2dissite 000-default.conf

sudo chown :www-data plants_api/db.sqlite3

sudo chmod 664 plants_api/db.sqlite3

sudo chown :www-data plants_api/

ls -la

sudo chown -R :www-data plants_api/media/

sudo chmod -R 775 plants_api/media
sudo chown :www-data plants_api/

#Mover llaves y datos sensibles a variables de ambiente

sudo chmod 775 plants_api/

#Reiniciamos apache2
sudo service apache2 restart


Guia de referencia: https://www.youtube.com/watch?v=Sa_kQheCnds&t=1816s


