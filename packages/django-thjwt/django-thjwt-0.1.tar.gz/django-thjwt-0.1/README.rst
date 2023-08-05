=====
thjwt
=====

thapi is a simple app to connect to th-ciloud platform applcations

detauk documentation is in the "docs" directory

Quick start

-----------

1. Add "thjwt" to your INSTALLED_APPS setting like this::

    INSTALL_APPS = [
        ...
        'thjwt',
    ]

2. Include the thapi URLconf in your project urls.py like this::

    url(r'^thjwt/',include('thjwt.urls')),

3. Run `python manage.py migrate` to create thapi models

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a thapi (you'll need the Admin app enabled).

5. Visti http://127.0.0.1:8000/thjwt/ to participate int he thapi