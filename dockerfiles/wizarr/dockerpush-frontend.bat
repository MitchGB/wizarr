@ECHO OFF

docker build -t registry.mitchg.dev/wizarr:latest .
docker tag wizarr:latest registry.mitchg.dev/wizarr:latest
docker push registry.mitchg.dev/wizarr:latest