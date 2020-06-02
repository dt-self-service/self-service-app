# self-service-app 🐳
> Please use the [dt-self-service-docker](https://github.com/dt-self-service/self-service-docker) to deploy. Standalone docker-compose, app and default configs for deploying self-service-app with nginx and postgres.

## Table of Contents 📋
* [Introduction](#introduction)
* [Screenshots](#screenshots)
* [Technologies](#technologies)
* [Setup](#setup)
* [Features](#features)
* [Status](#status)
* [Credit](#credit)
* [Contact](#contact)

## Introduction ℹ
This repo contains an example configuration that **REQUIRE CHANGES**.
Please copy the contents of app/config_template to app/config directory. Be sure to go through each config.
The sections in settings.py that need to be adjust are labelled with #CHANGEME.
Copy the .env.template files to .envs and update the variable values as needed.

## Screenshots 📸
![Login](https://github.com/dt-self-service/self-service-app/blob/master/screenshots/login.PNG)
![Dashboard](https://github.com/dt-self-service/self-service-app/blob/master/screenshots/dashboard.PNG)
![Create Maintenance Window](https://github.com/dt-self-service/self-service-app/blob/master/screenshots/create-mwindow.PNG)

## Technologies 👨‍💻
* Python 3.8+
* Django
* Docker
* nginx
* Bootstrap
* PostgreSQL

## Setup 🚀
> ### Prerequisites:
>
> - Docker

1. Clone the latest version of the self-service-docker application:

> `git clone git@github.com:dt-self-service/self-service-docker.git`

2. Switch into the application's directory:

> `cd self-service-docker/app/`

3. Edit django.template.env using your favorite editor to configure admin and host and save it as django.env. If SMTP is used, the corresponding settings should be uncommented and assigned values here:

> `vim django.template.env`

> `:wq! django.env`

4. Edit db.template.env using your favorite editor to configure database user and password db.env:

> `vim db.template.env`

> `:wq! db.env`

5. Copy everything in this folder into ../config

> `cp -r config_template config`

6. Switch into the config directory and edit user_variables.py to connect to your Dynatrace environment:

> `cd config`

> `vim user_variables.py`

7. *OPTIONAL: Configuring SSO - Switch into the saml folder and configure SAML inside settings.json. Cert and Key files for the SP (This App) go into the $PROJECT_ROOT/app/config/cert directory as "sp.crt" and "sp.key", respectively.*

8. Navigate to the root of the project and enter the nginx directory

9. Copy nginx.template.conf to nginx.conf

> `cp nginx.template.conf nginx.conf`

10. Open nginx.conf for editing to search and replace "www.example.com" with the correct url. For example in vim:

> `%s/www.example.conf/<application_url_here>/g`

11. Edit nginx.conf port 80 block to redirect to the published port and then close the file

> `return 302 https://www.example.com;` to `return 302 https://www.example.com:8443`;

12. *OPTIONAL: To use your own certs instead of a Self-Signed, add the cert and key as cert.pem and key.pem, repectively, in the folder $PROJECT_ROOT/nginx/ssl*

13. *OPTIONAL: To change the default ports the applications runs on you can change it in docker-compose.yml*

14. Switch back to the root of the project and start the services using docker-compose:

> `docker-compose up -d`

15. Using your browser navigate to your host https://HOST:8443 and login using the admin account you created.
  
## Features 🤖
* Maintenance Windows
* Local Authentication
* SSO
* Requests Logging for Auditing

To-do list:
* Filter Down Views based on Permissions in Dynatrace
* Install Wizard
* Alerting Profiles
* Problem Notification Integration

## Status 📝
Project is: _in progress_

## Credit ✨
Special thanks to Joe Nguyen for developing test cases for this project!

## Contact 🤝
Created by George Teodorescu and Aaron Philipose - feel free to contact us!
