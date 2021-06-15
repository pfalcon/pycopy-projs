D=$(dirname $0)
sudo sh -c "nohup pycopy -X strict -X heapsize=40wK $D/disk_sleep_mon.py /dev/sda >>/run/disk_sleep_mon.log 2>&1" &
