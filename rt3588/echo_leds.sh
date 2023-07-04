#!/usr/bin/env bash
# 每隔一秒打印一次时间循环

leds=(
    "power"   # 蓝
    "user"    # 红
    "user1"   # 绿
)

# close all light
for led in ${leds[@]}
do
    leds_path=/sys/class/leds/:${led_id}/brightness
    echo 0 > ${leds_path}
done


led_id=power
led_id=user1 
led_id=user 

while true
do
    echo "The time is: `date`"
    sleep 1
    echo 0 >/sys/class/leds/:${led_id}/brightness  # 灯灭
    sleep 1
    echo 1 >/sys/class/leds/:${led_id}/brightness  # 灯亮
done