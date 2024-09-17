# !/bin/sh

echo "<<<<<<<<<<<<<<< running migrations >>>>>>>>>>>>>"
python3 -m manage makemigrations --no-input
python3 -m manage migrate --no-input
echo "<<<<<<<<<<<<<<< starting consumer >>>>>>>>>>>>>"
python3 -m manage start_consumer
echo "<<<<<<<<<<<<<<< starting server >>>>>>>>>>>>>>>>"
python3 -m manage runserver 0.0.0.0:8002