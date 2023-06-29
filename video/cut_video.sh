#!/usr/bin/env bash
# usage: bash cut_video.sh video_file
# cut video file to 10s

# default params
video_file=${1:-"test20230628T201755Z_20230628T202000Z.mp4"}
start=${2:-"0:0"}
keep_time=${3:-10}

echo "${video_file} ${start} ${keep_time}"


# get date string
date_str=$(date "+%Y%m%d%H%M%S")

# function for cut_video use ffmpeg with hwacc
function cut_video()
{
    video_file=$1
    start=$2
    keep_time=$3

    ffmpeg -ss ${start} -t ${keep_time} \
        -i ${video_file} \
        -y v${date_str}_t10_${video_file}
}

# run main here
cut_video ${video_file} ${start} ${keep_time}