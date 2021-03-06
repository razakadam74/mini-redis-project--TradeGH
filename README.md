# Mini Redis Project by TradeGH
This is the Take-Home Project specification for candidates for Engineering @ Trade
This is a server that enables clients to create, query, and manipulate three basic data structures
 (​String​, L​ist<String>​, ​Map<String, String>​) via commands issued over the network.

##considerations
speed
intuition
Easy to understand


 
##Install and start redis
```bash
$ brew install redis
```

Start Redis server using configuration file.
```bash
$ redis-server /usr/local/etc/redis.conf
```

#####configure Redis Server connection
modify REDIS_URL in config.py

#####Run the API without Docker Container (running app)
```sh
pip install --trusted-host pypi.python.org -r requirements.txt   #install project dependencies
python run.py                                                   # run api
```


##Build docker Image

1. Install docker from [https://www.docker.com/](https://www.docker.com/)
2. Start docker application on your computer

#####Run the following command to build the docker image infer from web directory
```sh
docker build -t api_v1 .
```


#####Run the Docker Container (running app)
```sh
docker run -d -p 5000:5000 api_v1
```

#####You can find the container runtime details as shown below
```bash
$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS                    NAMES
e1db3bcb1513        api_v1               "python run.py"     About a minute ago   Up About a minute   0.0.0.0:5000->5000/tcp   heuristic_hopper

```

#####View logs of container
```
$ docker logs e1db3bcb1513
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 268-732-459
```


#####Access the application at the address [http://localhost:5000/](http://localhost:5000/)

## Testing
```bash

```

##Python dependencies are found in requirements.txt file









