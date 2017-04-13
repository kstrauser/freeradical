fixme:
	grep -R example.taco .

firstrun:
	ansible-playbook -i hosts first_run.yml

dhparams:
	openssl dhparam -out files/etc/nginx/dhparams.pem2 2048

install:
	ansible-playbook -i hosts install_mastodon.yml
