#!/usr/bin/env bash
# 每隔一秒打印一次时间循环


# "power" 蓝
# "user"  红
# "user1" 绿
led_id=power
led_id=user1
led_id=user

leds=(
    power
    user
    user1
)

function help() {
    echo "Usage: $0 -open-all"
    echo "Usage: $0 -close-all"
    echo "Usage: $0 -location"
    echo "Usage: $0 -reset"
    echo "Usage: $0 -open power|user|user1"
    echo "Usage: $0 -close power|user|user1"
}

function open() {
  led=$1
  echo 1 > /sys/class/leds/:${led}/brightness
}

function close() {
  led=$1
  echo 0 > /sys/class/leds/:${led}/brightness
}

function close_all() {
  # close all light
  for led in ${leds[@]}
  do
    close $led
  done
}

function open_all() {
  # close all light
  for led in ${leds[@]}
  do
    open $led
  done
}


# location
function location() {
  close_all
  led_id=user
  while true
  do
      echo "The time is: `date`"
      sleep 1
      close $led_id
      sleep 1
      open $led_id
  done
}

# check_sub_cmd
function check_sub_cmd() {
   cmd=$1
   led=$2
       # set -x
    if [ "X$cmd" == "X-open-all" ]; then
        open_all
        return $?
    elif [ "X$cmd" == "X-close-all" ]; then
        close_all
        return $?
    elif [ "X$cmd" == "X-location" ]; then
        location
        return $?
    elif [ "X$cmd" == "X-open" ]; then
        open $led
        return $?
    elif [ "X$cmd" == "X-close" ]; then
        close $led
        return $?
    elif [ "X$cmd" == "X-reset" ]; then
        close_all
        open "power"
        return $?
    else
        help
        return 1
    fi
}

# main here
if [ $# -lt 1 ]; then
    help
    exit 1
fi
check_sub_cmd $1 $2
exit $?