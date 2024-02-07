pkill -f runserver
cd backend
source env/bin/activate
nohup python3 manage.py runserver&
