RUN_CMD=/usr/local/bin/docker-compose -f /var/lib/mastodon/docker-compose.yml run --rm web

cron:
	$(RUN_CMD) rake mastodon:daily
	$(RUN_CMD) rake mastodon:users:clear

update:
	docker-compose build
	service docker-mastodon restart
	docker-compose run --rm web rails db:migrate
	docker-compose run --rm web rails assets:precompile
	service docker-mastodon restart
