#!/bin/bash
set -e

cd /webprojekti/awards

git pull origin main

sudo docker compose up -d --build

sleep 12

sudo docker compose ps

curl -s https://api.ylff.id.lv/health
