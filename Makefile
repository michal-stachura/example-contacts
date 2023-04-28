migrations:
	sudo docker-compose -p contacts -f local.yml run --rm django python manage.py makemigrations

migrate:
	sudo docker-compose -p contacts -f local.yml run --rm django python manage.py migrate

run:
	sudo docker-compose -p contacts -f local.yml up

build:
	sudo docker-compose -p contacts -f local.yml build

test:
	sudo docker-compose -p contacts -f local.yml run --rm django pytest -x

shell:
	sudo docker-compose -p contacts -f local.yml run --rm django python manage.py shell

cleardocker:
	sudo docker-compose -p contacts -f local.yml down --volumes --remove-orphans --rmi all
	
pgbash:
	sudo docker exec -it example_contacts_local_postgres /bin/bash
	
bash:
	sudo docker exec -it example_contacts_local_django /bin/bash

seed:
	docker-compose -p contacts -f local.yml build; \
	docker-compose -p contacts -f local.yml run --rm django python manage.py migrate; \
	docker-compose -p contacts -f local.yml run --rm django python manage.py shell < example_contacts/utils/seed.py
	