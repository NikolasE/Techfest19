# Techfest 2019

Winner of Landeshauptstadt München / [Munich Maker Lab](https://munichmakerlab.de/)'s Wild Track at [Techfest 2019](https://techfestmunich.com/) Hackathon.

Presentation [Slides](https://docs.google.com/presentation/d/1Cj1SVs_LXiQ6w6Apk9l8yiHGhnoP5J-KI6mlytDi-2g/edit?usp=sharing)

![20190908_003910_1](https://user-images.githubusercontent.com/11611719/64481326-7d7e0f80-d1da-11e9-8fdc-250e890439a7.gif)

## Demo Videos
Video play/pause based on rowing performance  
https://www.youtube.com/watch?v=G4LVUWbew_E

LED feedback  
https://www.youtube.com/watch?v=Owztq-mSMeI

Rowing with LED suit on  
![image](https://user-images.githubusercontent.com/11611719/64512710-45b0be00-d2e7-11e9-88f3-afdb6ef311c9.png)

## Running

* Launch `PythonControl/Main.py` for LED and "Netflix" demo
* Launch `PythonControl/realtime.py` for live audio feedback on common rowing mistakes

Make sure to install the Udev rule for Concept2 ergometer:
```
echo 'SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", MODE="0666", ATTRS{idVendor}=="17a4"' | sudo tee /etc/udev/rules.d/techfest19_erg.rules
```

