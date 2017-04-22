firstrun:
	ansible-playbook first_run.yml

dhparams:
	openssl dhparam -out files/as-is/etc/nginx/dhparams.pem2 2048

install:
	ansible-playbook install_mastodon.yml
