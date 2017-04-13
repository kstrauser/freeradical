# Mastodon adminstration helpers

## Ansible

Use these [Ansible](https://www.ansible.com) playbooks to go from bare metal to a configured Mastodon instance in a few minutes.

### Before you start

This is currently tailored for deployment to Digital Ocean, particularly the bit about mounting a block device. Delete the "Format the volume", "Make the PostgreSQL directory", and "Mount the volume" tasks if that doesn't apply to you.

The playbooks configure a Ubuntu 16.04 server. It may be compatible with new versions. It certainly won't be compatible with other distros, except perhaps Debian (which isn't tested).

`first_run.yml` assumes you can SSH into your server as root using publickey authentication. This is normal on Digital Ocean when you create a new server.

`first_run.yml` requires that Python 2.7 is already installed on your server. This is the one package Ansible can't install itself.

### Preparing to run

1. Edit `host_vars/mastodon` to suit.
1. The config files are for a fictional site named "example.taco". Find and replace every occurrence of example.taco with your own site domain. `make fixme` can locate these for you.

### Installing

Once you're ready:

1. Run `make firstrun`. This does a few things:
    - Updates all installed packages
    - Installs the distro's Python (in case you're bootstapping with copied-in version) and a proper shell
    - Creates the admin and daemon users
    - Mounts the block device for use by PostgreSQL
    - Disables SSH
    - Reboots the system
1. Run `make dhparams` to generate your own `dhparams.pem` file. This makes SSL happy. It also takes ages.
1. Run `make install` to do All The Things:
    - Installs required packages
    - Clones a Mastodon git repo
    - Builds Mastodon
    - If the git repo contains a `.env.production` file, e.g. you cloned your own forked Mastodon instead of the main release:
        - Runs database migrations and compiles assets
        - Starts the Mastodon service
    - Configures Nginx with a valid SSL cert, courtesy of Let's Encrypt

If the winds are blowing right and our friends in [Witches Town](https://witches.town/about) have said the right incantations, you should be able to log into your new Mastodon instance. Congratulations!

## About

This was cobbled together by [Kirk Strauser](https://freeradical.zone/@tek), who is too lazy to look this stuff up each time. If this helps you, please write to say hi!
