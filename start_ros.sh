#!/bin/bash
# Создаем структуру папок
mkdir -p ros_ws/src

# Запускаем контейнер
docker-compose up -d

# Заходим в контейнер
docker exec -it ros_development bash -c "
    cd /home/ros/ws &&
    source /opt/ros/noetic/setup.bash &&
    catkin_make &&
    bash"