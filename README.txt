Here is a simple Python script that is used with a Raspberry Pi to activate and light up a modified NHL Goal Light each time your favorite NHL team scores! You can run the script in the background or have it displayed in the foreground if you have a monitor connected. I have mine running in the background. The script also displays the score of previous, current and recently finished NHL games

!

So what are the delay times between the actual goal being scored and when the horn sounds? All games where watched live on tv, both East Coast & West Coast games, with a sample size of 36 goals:

Min: 3 seconds
Max: 1 minute 2 seconds
Average: 28 seconds

Full list of goal times at end of file.
-----------------------------------------------------------------------------------------


Requirements/Materials
:

-NHL Goal Light purchased from: http://us.thegoallight.com/store/#!/The-Goal-Light-XR/p/55401260/category=1620116
	*I purchased mine from hockey giant and used a 20% off coupon. So you can find it cheaper!

-Raspberry Pi with a WiFi Dongle that has the following installed:
	Operating System: Raspbian
	Python 2.7
 +
	Pip- Pip is already installed if you're using Python 2 >=2.7.9 or Python 3 >=3.4 downloaded from python.org, but you'll need to upgrade pip.
	Requests
- Open the terminal, Install with: pip install requests
	Colorama
- Open the terminal, Install with: pip install colorama

-Power cable for the Raspberry Pi

-At least 2 Dupont cables male to female 200mm+ length (Buy at least 10 so if you mess up, you have others to work with)

-At least 1 Three Pin NPN Transistors 2N3904 (Buy at least 10 so if you mess up, you have others to work with)

-At least 1 15k Ohm Resistors (Buy at least 10 so if you mess up, you have others to work with)

-Soldering Iron & solder

-Optional- Raspberry Pi case
-----------------------------------------------------------------------------------------


Instructions:

Setting up the Raspberry Pi:

Follow this link, https://www.raspberrypi.org/help/noobs-setup/ , to set up your Raspberry Pi if you don't know how. It's a straight forward tutorial and easy to follow. There are many tutorials out there on how to do this. Make sure you connect it to the internet also. Google "How to setup Raspberry Pi WiFi/Wireless". You WILL NEED to set up a Static IP address. If you don't set up a Static IP address, the IP address on the Raspberry Pi is set automatically and it will change. This will give you trouble when connecting remotely. So make sure you set up a Static IP address.

There are two set of instructions inside the Instructions folder. If you purchased/have the older version of the NHL Goal Light follow the 'Remote Instructions'. The older versions of the Goal Light do NOT have a RESET button on the light. If you have the newest version of the Goal Light, your goal light WILL have a reset button. Follow the 'Reset Button Instructions'.

Why does it matter? If you have the newest version of the Goal Light you will notice there is a Reset Button. In order to save electricity or batteries, if the light isn't activated within 3 hours, the goal light will go into 'Sleep Mode' which disables the remote and all of the lights functions until the reset button is pushed. Obviously NHL teams don't play 24/7 so it would be an inconvenience to have to push that reset button every day/3 hours so the program works. The 'Reset Button Instructions' work around that feature so you don't have to press it at all.


-----------------------------------------------------------------------------------------


Tested on
 Raspberry Pi 2 with Raspbian installed via NOOBS_v1_5_0 and Python 2.7.9

If you only want to see games for today you can run the script with the `--today-only` flag

. Example: python /path/Scoreboard.py --today-only

If you want to "set it and forget it" remotely you will have to download this nifty program called Screen onto the Raspberry Pi. Screen allows you to start a processes remotely, disconnect from the SSH, and have the instance continue running even after you disconnect your SSH session. Without this, once you exit the SSH session, all processes are stopped on the Raspberry Pi. Google "Using Screen with Raspberry Pi to avoid leaving SSH sessions open" for more details.


-----------------------------------------------------------------------------------------


Thanks and enjoy!

List of all goals in seconds. The absolute max delay can be 62 seconds. This program refreshes 2 seconds after NHL.com updates their scores. They update their scores every 60 seconds.

3,7,9,10,13,14,15,19,22,25,25,25,26,30,31,32,32,33,34,36,40,45,46,47,50,50,51,54,60,62 


*I changed the code around mid testing to create a more efficient refresh time, here is a small sample size of the restults after I changed the code around.

6,12,27,4,5,11 




-----------------------------------------------------------------------------------------

The MIT License (MIT)
Copyright (c) 2016 Muhamed Catovic


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
