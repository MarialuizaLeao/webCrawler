#!/bin/bash

python3 -m venv pa1
source pa1/bin/activate
pip3 install -r requirements.txt

python3 main.py -s seeds-2020100953.txt -n 100000 -t 100 &
echo $! > 100_thread.pid

# wait for 100 thread to create the file data-100.warc.gz
while [ ! -f data-100.warc.gz ]; do
    sleep 60
done

kill $(cat 100_thread.pid)
rm 100_thread.pid

mkdir -p data_100
mv data-*.warc.gz data_100/
mv download_rate100.csv data_100/

rm -rf data-*.warc.gz

##########################################################

python3 main.py -s seeds-2020100953.txt -n 100000 -t 50 &
echo $! > 50_thread.pid

# wait for 100 thread to create the file data-100.warc.gz
while [ ! -f data-100.warc.gz ]; do
    sleep 60
done

kill $(cat 50_thread.pid)
rm 50_thread.pid

mkdir -p data_50
mv data-*.warc.gz data_50/
mv download_rate50.csv data_50/

rm -rf data-*.warc.gz

##########################################################

python3 main.py -s seeds-2020100953.txt -n 100000 -t 25 &
echo $! > 25_thread.pid

# wait for 100 thread to create the file data-100.warc.gz
while [ ! -f data-100.warc.gz ]; do
    sleep 60
done

kill $(cat 25_thread.pid)
rm 25_thread.pid

mkdir -p data_25
mv data-*.warc.gz data_25/
mv download_rate25.csv data_25/

rm -rf data-*.warc.gz