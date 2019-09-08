# Techfest 2019

![20190908_003910_1](https://user-images.githubusercontent.com/11611719/64481326-7d7e0f80-d1da-11e9-8fdc-250e890439a7.gif)


Udev rule for Concept2 ergometer:
```
echo 'SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", MODE="0666", ATTRS{idVendor}=="17a4"' | sudo tee /etc/udev/rules.d/techfest19_erg.rules
```

