# Boot with docker

If you need to set up the project in Docker, do the following:

```sh
cp ./docker-compose/example.env ./docker-compose/.env
```

Edit the .env file if necessary (By default, the settings should be functional).
If you are using macOS with M1/M2 processors and are experiencing issues starting the project,
replace the contents of the root requirements.txt with macOS_requirements.txt (only the contents, not the files themselves).


Go to docker path and run with up command:
```sh
cd ./docker-compose/
```
```sh
docker-compose up --build
```
