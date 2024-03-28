# 2024_Vision_Project

## Installing linux service

1. `sudo ln -s $(pwd)/vision1038.service /lib/systemd/system/vision1038.service`
2. `sudo systemctl daemon-reload`
3. `sudo systemctl enable vision1038`

## Boot to CLI by default

`sudo systemctl set-default multi-user.target`

## Boot to GUI by default

`sudo systemctl set-default graphical.target`

## Boot GUI for one-time use

`startx`

## Stopping the service

`sudo systemctl stop vision1038`

## Starting the service

`sudo systemctl start vision1038`