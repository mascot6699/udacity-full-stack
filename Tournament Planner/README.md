# Movie Trailer Website: Fresh Tomatoes

This is the second project for the fulfillment of Udacity's [Full-Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)

### How to run

This directory can be initiated with [Vagrant](https://www.vagrantup.com/) by executing the command `vagrant up` within the `vagrant/` directory.

- `vagrant ssh`
- `cd /vagrant/tournament`

The database will be created by running the following commands:

- `chmod 700 tournament_db.sh`
- `sh tournament_db.sh`

The tables will be created by running:

- `psql tournament < tournament.sql`

The test cases can be run by executing the following commands:

- `python tournament_test.py`

