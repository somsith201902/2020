From command line (terminal):

dependencies:
apt install python3
apt install python-pip3
apt install flask
apt install flask-restful
apt install flask-sqlalchemy
apt install flask-login

run:
python3 database_setup.py    # set up database
python3 app.py               # run server
google-chrome http://localhost:5000/
