#! /bin/bash

if test -e ~/.git-credentials
then
    echo '!!~/.git-credentials already exist!'
else
    echo 'Create ~/.git-credentials..'
    touch ~/.git-credentials
fi


if [$# == 2];then
    username = $1
    password = $2
    echo https://${username}:${password}@github.com > ~/.git-credentials
fi

if [$# == 1];then
    username = $1
    echo "input password"
    read password
    echo https://${username}:${password}@github.com > ~/.git-credentials
fi

if [$# == 0];then
    echo "input username"
    read username
    echo "input password"
    read password
    echo https://${username}:${password}@github.com > ~/.git-credentials
fi


echo 'Configure username and password..'
echo "http://$username:$password@$localhost" >> ~/.git-credentials
git config --global credential.helper store
echo 'Sucess!'
