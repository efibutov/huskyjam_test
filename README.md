# Garage application server

In order to operate the server, do the following (all the commands should run from the root project directory)

1. On the first time you run the server, initialize the system with this command:

    `docker-compose up --build -d; docker exec -it garage_web /bin/bash /init_system.sh`

    The script will ask for admin username, email and password (which will give the full access to the application database).
    
    Now open [server home page](http://localhost:80/) in your browser. If everything is OK, you'll see the server home page

2. To stop the server, run
    
    `docker-compose stop`

2. In every following running use similar command:

    `docker-compose up -d`
    
    If you want to see the system logs, run
    
    `docker-compose logs -f`

##For more info about docker see [official documentation](https://www.docker.com/)
##Documentation about [docker-compose](https://docs.docker.com/compose/)

#Testing app

To verify the app is functioning properly, run tests:

1. If the app is not running, run it (as described above)

2. Run this command:

    `docker exec -it garage_web python /app/manage.py test garage`
