# Free Radical Mastodon adminstration stuff

These are the moving parts that go into hosting the [Free Radical](https://freeradical.zone/) Mastodon instance.

## Ansible

Use these [Ansible](https://www.ansible.com) playbooks to go from bare metal to a configured Mastodon instance in a few minutes.

### Before you start

This is currently tailored for deployment to Digital Ocean, particularly the bit about mounting a block device, but will likely work for other VPS hosts.

The playbooks configure a Ubuntu 16.04 server. It may be compatible with newer versions. They certainly won't be compatible with other distros, except perhaps Debian (which isn't tested).

`first_run.yml` assumes you can SSH into your server as root using publickey authentication. This is normal on Digital Ocean when you create a new server.

### Preparing to run

1. Edit `host_vars/mastodon` to suit.

### Installing

Once you're ready:

1. Run `make firstrun`. This installs Python, creates an admin user, and disables SSH as root.
1. Run `make dhparams` to generate your own `dhparams.pem` file. This makes SSL happy. It also takes ages.
1. Run `make install` to do All The Things:
    - Installs required packages and configures them
    - Clones a Mastodon git repo
    - Builds Mastodon
    - If the git repo contains a `.env.production` file, e.g. you cloned your own forked Mastodon instead of the main release:
        - Runs database migrations and compiles assets
        - Starts the Mastodon service
    - Configures Nginx with a valid SSL cert, courtesy of Let's Encrypt

If the winds are blowing right and our friends in [Witches Town](https://witches.town/about) have said the right incantations, you should be able to log into your new Mastodon instance. Congratulations!

### Notes

The `first_run.yml` playbook can only be run one time, because it logs in as root and then disables root logins. You only need to run those steps once ever per server anyway.

The `install_mastodon.yml` playbook is idempotent. It describes the expected state of the running system and only takes the actions necessary to make your Mastodon installation look that way. If neither it nor the state of your server have changed, running it again won't alter your server at all.

## About

This was cobbled together by [Kirk Strauser](https://freeradical.zone/@tek), who is too lazy to look this stuff up each time. If this helps you, please write to say hi!
