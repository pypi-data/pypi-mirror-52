#!/usr/bin/env bash

set -ex

wst publish

ssh -T one-bead <<EOF
set -e

sudo su -

echo [ Show what\'s running ]
ps -eaf | grep web-app | grep -v grep

echo [ Updating 1bead.org ]
app update --wait 1bead.org

echo [ Stop apps ]
killall web-app

echo [ Wait a second to make sure apps are down ]
sleep 1

echo [ Show what\'s running ]
ps -eaf | grep web-app | grep -v grep

echo [ Start apps ]
web-app --port 80 &>/tmp/web-app.out &

echo [ Wait a second to make sure apps stay up ]
sleep 1

echo [ Show what\'s running ]
ps -eaf | grep web-app | grep -v grep

EOF
