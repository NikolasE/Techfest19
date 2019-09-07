# Techfest 2019


```
echo 'SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", MODE="0666", ATTRS{idVendor}=="17a4"' | sudo tee /etc/udev/rules.d/techfest19_erg.rules
```

