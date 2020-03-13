# Kindler - An E-Ink Display Frame In Your Photo Frame

## Introduction

A couple of months ago I've started a little project that involved some Raspberry Pis and some of that type of equipment. One of the items we've purchase is a small [E-Ink display, 2.13",](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_(D)) to be used as a diagnostics pane. So about a week ago i was cleaning up my work space to remove all those fancy useless bits from the work surface coming upon this little E-Ink display. That night i was trying to think about what to do with it.

This is what i came up with and how to build one yourself really fast:

Take a photo frame you already have of your loved ones and add a little caption to it with changing texts. In this case i took our family's photo and added some alternating quotes.

**Disclaimer** - This is **not** a sponsored post neither are any of the products promoted in anyway. Other than the Raspberry Pi because i love it.

## Built Details
Since the display is only 2.13" it really can't be too much in and of itself. Since it's also not that durable and i'm pretty sure that after 10 minutes with our kids this thing will turn into a colored useless strip i was going from something more decorative. So i've commenced building a picture frame with our own favorite picture that will have an alternative text on it. For the text i chose quotes.

This is how it looks:

![](https://raw.githubusercontent.com/ytisf/Kindler/master/images/6.jpg)

### What You'll Need
I really wanted this to be durable, resilient and long lasting. We have a few picture frames in our house and some just died, some just reboot occasionally and some just shut-off from time to time waiting for someone to start them. Hence i wanted something that once plugged in, even with no internet, will continue working.

#### Equipment:

1. Raspberry Pi of any kind. I started with a Raspberry Pi W Zero but for some reason it chose not to work with my display (although it should have) so i've switched to a Raspberry Pi 3.
1. E-Ink display using SPI. I've used WaveShare 2.13 D but really any would do.
1. Some duct tape.
1. A Photo frame.
1. Your Photo.
1. *Optionally - Raspberry Pi Case.*

**Project Work Time**: ~15 minutes if your Raspberry Pi is ready, ~1 hour if it needs flushing.

![](https://raw.githubusercontent.com/ytisf/Kindler/master/images/0.jpg)

## Instructions

### Step 1 - Get Your Raspberry Pi ready
No need for me here.
https://www.raspberrypi.org/documentation/installation/installing-images/

Remember to `touch ssh` and edit your network configurations to have a way to deploy code on it. [This](https://raspberrypi.stackexchange.com/a/57023) worked just fine.

### Step 2 - Prep your Pi for Display
Depending on your display. I've worked by [this](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_(D)) and here's a summary:

```
# Enable SPI
sudo raspi-config
# Choose Interfacing Options -> SPI -> Yes  to enable SPI interface
# Restart

# Install BCM2835 libraries
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.60.tar.gz
tar zxvf bcm2835-1.60.tar.gz
cd bcm2835-1.60/
sudo ./configure
sudo make
sudo make check
sudo make install

# Wiring Pi
sudo apt-get install wiringpi

# Python2 setup
sudo apt-get update
sudo apt-get install python-pip
sudo apt-get install python-pil
sudo apt-get install python-numpy
sudo pip install RPi.GPIO
sudo pip install spidev

# e-Paper libs
sudo git clone https://github.com/waveshare/e-Paper
cd e-Paper/RaspberryPi\&JetsonNano/
cd python
sudo python setup.py install

# Image Libraries
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
```

### Step 3 - Connection Setup

Now that we have the tools and everything needed to have the code communicate with the display we need to connect it. This part is relatively simple - the adapter to the display should come with a full IDE female connector to connect to the Raspberry Pi's male IDE connector. Just snap that in on top of your RaspberryPi and is should be ready to go.

In my case, i also wanted a small fan to circulate some air in the case of the device. Since all of the IDE pins are locked i've used an 8-pin connector from the adapter (came in the box for me) and then took pin-0 (VNN) and pin-1 (GND) and connected the fan to that.

![](https://raw.githubusercontent.com/ytisf/Kindler/master/images/1.jpg)

![](https://raw.githubusercontent.com/ytisf/Kindler/master/images/2.jpg)


### Step 3.5 - [Optional] Configuring WiFi

This step is optional and the `Kindler` will be operating the same way regardless if you take this step or not. This is just if you want to have an option to update your quotes remotely or SSH into the RaspberryPi.

Edit the file `wifi_conf` to have the same WiFi configurations and the network you want it conneting to. After that, upload this configuration to: `wpa_supplicant.conf` on the root directory of the RaspberryPi and create a file named `ssh` on the same directory.

The `ssh` empty file on the root directory will instruct the RaspberryPi to open up the SSH Server when booting, and a parsing of the `wpa_supplicant.conf` will have the RaspberryPi load the WiFi network configurations and attempt to connect to the network.


### Step 3.7 - [Optional] Editing The Text

You can edit the texts to be displayed however you want. Just keep the first line (header) of the CSV and make sure you're inputting two elements even if the 2nd one is going to be an empty one. For example, if you want to have just one or two lines displayed the `quotes.csv` file should look like this:

```csv
quote,author
"This is line #1 with no 'Author'", ""
"Line #2 with Author", "Tony"
```

### Step 4 - Upload the Code

At this point you want to upload your code to the Raspberry Pi. You can so that with `scp`. This should be **after** you've put your lovely quotes in `quotes.csv`.

`scp -r ~/Kindler/. pi@pi_ip:/home/pi/Kindler/`

### Step 5 - Adding to Boot

At this point you want to make sure that even if the device reboots for some reason, power break, accidentally disconnecting it or anything else, when it starts up again it will continue operating as if nothing happened. Reiterating that the main point here is not to have another device you need to maintain but rather have it work without any maintenance.

Edit the `rc.local` file like this:

`sudo nano /etc/rc.local`

Add the following line before the `exit` line at the end:

`sudo python /home/pi/Kindler/main.py & `

To exit `nano` use `Ctrl+O` and `Return/Enter` to save and `Ctrl+X` to exit. Be sure to keep the `&` at the end or your Raspberry Pi will be stuck on boot loop. You need it to make sure that the `rc.local` does not stuck waiting on input but continue to the next line.

At this point you have added `Kindler` to the start up of the device and it should execute on the next boot (and any following).

### Step 6 - Casing In the Photo

When i measured this particular eInk display the size was 2[cm] on 3.5[cm]. Yours might be different depending on the EInk display you're using. Use a box cutter to cut the image and paste your display on the spot. Use some duct tape to join the RaspberryPi with the back of the photo. Make sure it has some clear surface space to disperse of aggregated heat.

![](https://raw.githubusercontent.com/ytisf/Kindler/master/images/3.jpg)

![](https://raw.githubusercontent.com/ytisf/Kindler/master/images/4.jpg)

![](https://raw.githubusercontent.com/ytisf/Kindler/master/images/5.jpg)
