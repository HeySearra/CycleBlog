source activate dj
echo "=> source dj venv successfully, make migrations..."
python Cuby/manage.py makemigrations
python Cuby/manage.py migrate
echo "=> db migrated successfully, run server..."
python Cuby/manage.py runserver
echo "=> server exited"
