#!/bin/sh

echo "<-------------------------->"
echo "< apt-get update & upgrade >"
echo "<-------------------------->"
sudo apt-get update && sudo apt-get upgrade

echo "<-------------------------->"
echo "< Install requirements.txt >"
echo "<-------------------------->"
pip install -r requirements.txt

echo "<------------------------->"
echo "< Installing Postgres SQL >"
echo "<------------------------->"
sudo apt-get install postgresql

echo "<------------------------->"
echo "< Creating Postgres User, >"
echo "<     username: finapp    >"
echo "<------------------------->"
sudo -u postgres createuser --superuser finapp

echo "<------------------------->"
echo "<  Creating Postgres DB,  >"
echo "<     db name: finapp     >"
echo "<------------------------->"
sudo -u finapp createdb finapp

echo "<--------------------------->"
echo "< To access created DB type >"
echo "< psql -U finapp  -d finapp >"
echo "<--------------------------->"

echo "<--------------------------->"
echo "<    To run the app type    >"
echo "<       python run.py       >"
echo "<--------------------------->"
