set -o errexit      # Exit immediately if any command fails
pip install -r requirements.txt   # Install all dependencies
python manage.py collectstatic --no-input   # Gather static files (CSS, JS, images)
python manage.py migrate            # Apply database migrations