set -o errexit

pip install -r requirements.txt

cd backend   # <-- add this line

python manage.py collectstatic --no-input
python manage.py migrate --noinput