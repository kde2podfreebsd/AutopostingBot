up:
	docker compose -f docker-compose-local.yaml up --build

down:
	docker compose -f docker-compose-local.yaml down && docker network prune --force

clean:
	find . -name __pycache__ -type d -print0|xargs -0 rm -r -- && rm -rf .idea/

docker_stop_all:
	docker stop $(sudo docker ps -a -q)

docker_rm_all:
	docker rm $(sudo docker ps -a -q)

prune:
	docker network prune

alembic_init:
	cd DataBase/ & alembic init migrations

alembic_rev:
	cd DataBase/ & alembic revision --autogenerate -m 'init'

alembic_upgrade:
	cd DataBase/ & alembic upgrade heads

git_clean_cache:
	git rm -rf --cached .

pre_commit:
	pre-commit run --all-files
