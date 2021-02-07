sudo cp config.txt /boot/config.txt
sudo cp cmdline.txt /boot/cmdline.txt
sudo systemctl disable getty@tty1
sudo cp splashscreen.service /etc/systemd/system/splashscreen.service
sudo systemctl enable splashscreen
sudo cp ../pics/splash.png /opt/splash.png
sudo apt install fbi
echo "requires reboot!"
