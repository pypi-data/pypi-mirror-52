#!/bin/sh

scheme="@scheme@"
git init
if [ $scheme = "https" ];then
    git remote add origin https://github.com/@username@/@projname@.git
    git remote add origin-git git@github.com:@username@/@projname@.git
    git remote add origin-https https://github.com/@username@/@projname@.git
fi

if [ $scheme = "git" ];then
    eval `ssh-agent`
    ssh-add
    git remote add origin git@github.com:@username@/@projname@.git
    git remote add origin-git git@github.com:@username@/@projname@.git
    git remote add origin-https https://github.com/@username@/@projname@.git
fi

git config --local user.name @username@
git config --local credential.username @username@
git config --local user.email @email@
git remote -v
git pull origin master
git add .
git commit -m "first commit"
git push origin master

