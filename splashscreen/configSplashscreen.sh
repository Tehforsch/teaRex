sudo apt install fbi
sudo cp config.txt /boot/config.txt
sudo cp cmdline.txt /boot/cmdline.txt
sudo systemctl disable getty@tty1
sudo cp splashscreen.service /etc/systemd/system/splashscreen.service
sudo systemctl enable splashscreen
echo "requires reboot!"
