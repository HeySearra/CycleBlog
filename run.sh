cd Cuby
source activate dj
echo "=> source dj venv successfully, rm caches..."
rm -rf **/migrations/00*
rm -rf **/migrations/__pycache__/*
echo "=> rm caches successfully, make migs..."
python manage.py makemigrations
python manage.py migrate
echo "=> db migrated successfully, run server..."
python manage.py runserver
echo "=> server exited"
