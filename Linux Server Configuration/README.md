## Server Address
User : grader
ssh port : 2200
IP address : http://35.162.192.16/
Application url : http://35.162.192.16/

## Software installed
1) apache2
2) postgresql
3) libapache2-mod-wsgi
4) git
5) other dependencies of flask project

## Changes made
1) Added grader user with sudo privilege
2) Added personal ssh key
3) Changed ssh port to 2200
4) Configured ufw to allow specified ports only(2200, 123, 80)
5) Setup apache conf to serve flask application using reference 2 stated below.

## References used were
1) https://www.digitalocean.com/community/tutorials/how-to-setup-a-firewall-with-ufw-on-an-ubuntu-and-debian-cloud-server
2) https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps