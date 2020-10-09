echo "---------"
echo "Collecting static"
echo "---------"
python3 manage.py collectstatic --no-input
echo "---------"
echo "Making migrations"
echo "---------"
python3 manage.py makemigrations
echo "---------"
echo "migrating"
echo "---------"
python3 manage.py migrate --no-input
echo "---------"
echo "Loading data"
echo "---------"
python3 manage.py loaddata data
