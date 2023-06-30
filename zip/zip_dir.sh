#!/usr/bin/env bash

# function zip dir with password "654321"
# $1: dir path
# $2: zip file path
# $3: password
function zip_dir() {
    if [ $# -lt 2 ]; then
        echo "Usage: $0 dir_path zip_file_path [password]"
        return 1
    fi

    dir_path=$1
    zip_file_path=$2
    password=$3

    if [ -z "$password" ]; then
        password="654321"
    fi

    if [ ! -d "$dir_path" ]; then
        echo "dir_path: $dir_path is not a dir"
        return 1
    fi

    if [ -f "$zip_file_path" ]; then
        echo "zip_file_path: $zip_file_path is already exist"
        return 1
    fi

    zip -r -P $password $zip_file_path $dir_path
    return $?
}

# function unzip dir with password "654321"
# $1: zip file path
# $2: unzip dir path
# $3: password
function unzip_dir() {
    if [ $# -lt 2 ]; then
        echo "Usage: $0 zip_file_path unzip_dir_path [password]"
        return 1
    fi

    zip_file_path=$1
    unzip_dir_path=$2
    password=$3

    if [ -z "$password" ]; then
        password="654321"
    fi

    if [ ! -f "$zip_file_path" ]; then
        echo "zip_file_path: $zip_file_path is not a file"
        return 1
    fi

    if [ -d "$unzip_dir_path" ]; then
        echo "unzip_dir_path: $unzip_dir_path is already exist"
        return 1
    fi

    unzip -P $password $zip_file_path -d $unzip_dir_path
    return $?
}

# function check cmd for zip_dir or unzip_dir
# $1: cmd
function check_zip_or_unzip()
{
    cmd=$1
    
    # set -x
    if [ "X$cmd" == "X-zip" ]; then
        zip_dir $2 $3 $4
        return $?
    elif [ "X$cmd" == "X-unzip" ]; then
        unzip_dir $2 $3 $4
        return $?
    else
        echo "Usage: $0 -zip dir_path zip_file_path [password]"
        echo "Usage: $0 -unzip zip_file_path dir_path [password]"
        return 1
    fi
}

# main here
if [ $# -lt 3 ]; then
    echo "Usage: $0 -zip dir_path zip_file_path [password]"
    echo "Usage: $0 -unzip zip_file_path dir_path [password]"
    exit 1
fi
check_zip_or_unzip $1 $2 $3 $4
exit $?
