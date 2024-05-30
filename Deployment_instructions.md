# Deployment instructions

```bash
cd ALGator
docker build -t bj . 
# configure nginx.conf and docker-compose.yml
docker compose up -d # run stack


cd ../ALGatorWeb
docker build -t dj . 
# configure nginx.conf, .env and docker-compose.yml


docker compose up -d # run stack

# One time job
docker exec -it dj python manage.py collectstatic # Django zbere vse statične datoteke v eno mapo (trenutno skonfigurirano na 'assets'); Potem jih Nginx servira.
docker exec -it db mysql -u root -palgator -e "GRANT ALL PRIVILEGES ON algator.* TO algator@'%';" # Daj polne pravice na userja
docker exec -it dj sh -c "export ALGATOR_ROOT='/ALGATOR_ROOT'; python manage.py migrate" # Naredi migracije podatkov
docker exec -it dj sh -c "export ALGATOR_ROOT='/ALGATOR_ROOT'; export DJANGO_SUPERUSER_USERNAME=algator; export DJANGO_SUPERUSER_EMAIL=algator@algator.com; export DJANGO_SUPERUSER_PASSWORD=algator; python manage.py createsuperuser --no-input" # Ustvari superuporabnika za projekt
```