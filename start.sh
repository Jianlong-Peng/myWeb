source ENV/bin/activate
uwsgi --socket 0.0.0.0:8080 --protocol=http -w wsgi:app

