RUN_CMD=/usr/local/bin/docker-compose -f /var/lib/mastodon/docker-compose.yml run --rm web

cron:
	$(RUN_CMD) rake mastodon:media:clear
	$(RUN_CMD) rake mastodon:push:refresh
	$(RUN_CMD) rake mastodon:feeds:clear

update:
	docker-compose build
	service docker-mastodon restart
	docker-compose run --rm web rails db:migrate
	docker-compose run --rm web rails assets:precompile
	service docker-mastodon restart
