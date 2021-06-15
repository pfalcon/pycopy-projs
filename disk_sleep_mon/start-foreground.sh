D=$(dirname $0)
sudo sh -c "PYCOPYPATH=$HOME/.pycopy/lib $HOME/bin/pycopy -X strict -X heapsize=40wK $D/disk_sleep_mon.py $1"
