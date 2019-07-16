Documentation for Jasper

Introduction:
This project is using the Jasper Voice recognition API developed by Shubhro Saha and Charlie Marsh. Jasper is an open source platform for developing always-on, voice-controlled applications. Jasper is a fully modifiable project that can support other API’s for further functionality in the form of modules. With jasper, I am using witai for the speech to text functionality and eSpeak for text to speech functionality.

How to use Jasper*:
*When using Jasper, make sure that you speak after the beep, otherwise it will cut off the first part of the sentence.
•	Google Calendar 
YOU: Add Calendar event
JASPER: What would you like to add?
YOU: Movie with Jodie Friday at 5 pm
JASPER: Added event Movie with Jodie on June 06 at 5:00 pm
JASPER: Is this what you wanted?
YOU: Yes
JASPER: Okay, I added it to your calendar
YOU: Do I have any Calendar events tomorrow
JASPER: Dinner with Jodie at 6:00 pm
YOU: Do I have any Calendar Events Today
JASPER: Dinner with Jodie at 6:00 pm

•	WolframAlpha 
#Commands WHO, WHAT, HOW MUCH, HOW MANY, HOW OLD
Note: The command WHERE is not included because the API return images, no text

•	Shutdown
YOU: Shutdown
 
•	Reboot
YOU: Reboot
or 
YOU: Restart

•	Wikipedia*
You: Jasper, Wiki OR Article
Jasper: What word would you like to learn about?
You: Apple
Jasper: Reads a Wikipedia summary

*I've limited the sentences that Jasper reads back to the user from the article to 5. Can be changed if too short or long. Also cannot use plural as it will not understand the article title.

•	Evernote
JASPER:  How can I be of service?
YOU:     Note
JASPER:  What would you like me to write down?
YOU:     Don't forget to bring potatoes tomorrow!
JASPER:  I successfully wrote down your note. 
 
Installation guide
Pre installation:
1) Update Pi and install some useful tools
#
	-> sudo apt-get update
	-> sudo apt-get upgrade --yes
	-> sudo apt-get install nano git-core python-dev bison libasound2-dev libportaudio-dev python-pyaudio --yes
	-> sudo apt-get remove python-pip
	-> sudo easy_install pip

2) Plug in the USB microphone and then create an ALSA config file
	-> sudo nano/lib/modprobe.d/jasper.conf
   Add the following lines in the file
	-> # Load USB audio before the internal soundcard
	   options snd_usb_audio index=0
	   options snd_bcm2835 index=1
	
	   # Make sure the sound cards are ordered the correct way in ALSA
	   options snd slots=snd_usb_audio,snd_bcm2835

3) Save and then restart the Pi
	-> sudo shutdown -r now

4) Add the following line to the end of ~/.bash_profile (If not made already run "touch ~/.bash_profile")
	-> export LD_LIBRARY_PATH="/usr/local/lib"
	-> source .bashrc
   And add this to your ~/.bashrc or ~/.bash_profile
	-> LD_LIBRARY_PATH="/usr/local/lib"
	-> export LD_LIBRARY_PATH
	-> PATH=$PATH:/usr/local/lib/
	-> export PATH
Installation steps (Jasper, pocketsphinx and eSpeak):
1) Clone the jasper source code from home dir
	-> git clone https://github.com/jasperproject/jasper-client.get jasper
2) Install python libraries
	-> sudo pip install --upgrade setuptools
	-> sudo pip install -r jasper/client/requirements.txt
3) Make jasper an executable 
	-> chmos +x jasper/jasper.py

Installing dependencies

1) Install pocketshpinx from source
*When downloading pocketsphinx skip the experimental installation guide, it doesnt work and breaks everything. (Only if you are using the installation steps from the website)
	-> wget http://downloads.sourceforge.net/project/cmusphinx/sphinxbase/0.8/sphinxbase-0.8.tar.gz
	-> tar -zxvf sphinxbase-0.8.tar.gz
	-> cd ~/sphinxbase-0.8/
	-> ./configure --enable-fixed
	-> make
	-> sudo make install
	-> wget http://downloads.sourceforge.net/project/cmusphinx/pocketsphinx/0.8/pocketsphinx-0.8.tar.gz
	-> tar -zxvf pocketpshinx-0.8.tar.gz
	-> cd ~/pocketsphinx-0.8/
	-> ./configure
	-> make
	-> sudo make install
	-> cd ..
	-> sudo easy_install pocketsphinx
2) Install CMUCLMTK
	-> sudo apt-get install subversion autoconf libtool automake gfortran g++ --yes
   Move to home dir
	-> svn co https://svn.code.sf.net/p/cmusphinx/code/trunk/cmuclmtk/
	-> cd cmuclmtk/
	-> ./autogen.sh && make && sudo make install
	-> cd ..
3) Install Phonetisaurus, m2m-aligner and MITLM
	-> wget http://distfiles.macports.org/openfst/openfst-1.3.4.tar.gz
	-> wget https://github.com/mitlm/mitlm/releases/download/v0.4.1/mitlm_0.4.1.tar.gz
	-> wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/m2m-aligner/m2m-aligner-1.2.tar.gz
	-> wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/phonetisaurus/is2013-conversion.tgz
   Untar the downloads
	-> tar -xvf m2m-aligner-1.2.tar.gz
	-> tar -xvf openfst-1.3.4.tar.gz
	-> tar -xvf is2013-conversion.tgz
	-> tar -xvf mitlm_0.4.1.tar.gz
4) Build OpenFST
	-> cd openfst-1.3.4/
-> sudo ./configure --enable-compact-fsts --enable-const-fsts --enable-far --enable-lookahead-fsts --enable-pft
	-> sudo make install 		//Will take a long time to build
5) Build MITLMT
	-> cd m2m-aligner-1.2/
	-> sudo make
6) Build MITLMT
	-> cd mitlm-0.4.1/
	-> sudo ./configure
	-> sudo make install
7) Build Phonetisaurus
	-> cd is2013-conversion/phonetisaurus/src
	-> sudo make
8) Move some of the compiled files
	-> sudo cp ~/m2m-aligner-1.2/m2m-aligner /usr/local/bin/m2m-aligner
	-> sudo cp ~/is2013-conversion/bin/phonetisaurus-g2p /usr/local/bin/phonetisaurus-g2p
9) Build the Phonetisaurus FST model
	-> wget https://www.dropbox.com/s/kfht75czdwucni1/g014b2btgz
	-> tar -xvf g014b2b.tgz
10) Build phonetisaurus model
	-> cd g014b2b/
	./compile-fst.sh
	cd ..
11) Rename folder for convenience
	-> mv ~/g014b2b ~/phonetisaurus
12) Restart Pi

Installation source:
http://jasperproject.github.io/documentation/installation/

Configuring jasper
1) Generate a user profile
	-> cd ~/jasper/client
	-> python populate.py 		

Starting Jasper
Run /home/pi/jasper/jasper.py on command terminal

Stopping Jasper
1) -> CRTL C 	//Helps keep the mic working

 
Troubleshooting installation problems:
Possible errors you may encounter and its fixes:
Error: "Cannot convert ostream to bool". Fixed by changing the line bool ret = *strm; to bool ret = static_cast<bool>(*strm);
There may be another error saying gcc will not recognise "W1" and "--no-as-needed". To fix, go to the openfsts folder and use grep -r -- -W1 and grep -r --no-as-needed to find where they are. There is a typo for W1 as it should be the letter l. Change it in each file. As for the "--no-as-needed", find it and delete it but keep the code around it.

When compiling the phonetisaurus, you may get the library not found error. Fix for this is -> sudo /sbin/ldconfig -v then compile again.
When using different mics, be sure to check mic.py if you get invalid sample rate errors. You would need to change the RATE and CHUNK variable to something suitable for the mics sound card. Now it is at RATE: 48000 and CHUNK: 2048

Installing modules for Jasper:
The modules are downloaded from the Official Jasper website.
http://jasperproject.github.io/documentation/modules/
These modules have installation guides inside each one. However they are slightly outdated therefore there may be errors when trying to install them.

Troubleshooting module installation problems:
Evernote should be connected to the swux eamil for note storage. If given EDAM errorcode=8, go to Evernote.py, change 
client = EvernoteClient(token=auth_token, sandbox = false) to client = EvernoteClient(token=auth_token)

How to change the name of the AI:
Search for all "Jasper" name and replace with new name.
Go to jasper/static/keyword_phrases and add the new name in alphabetical order within the list
Go to http://www.speech.cs.cmu.edu/tools/lmtool-new.html and add the keyword_phrases file to create a dictionary and 
language file. Replace the old dictionary and language file with the new ones:
jasper/Jasper.py
Check all jasper/client files
Check all jasper/tests files
jasper/client/alteration.py
jasper/client/app_utils.py
jasper/client/brain.py
jasper/client/diagnose.py
jasper/client/local_mic.py

Developer information:
//Used for everything -> Gmail, google API, Evernote, wolfram alpha, Google Drive, Github
Google voice username: swuxlab123@gmail.com
Google voice password: Swuxlab246!
The Jasper prototype is in Google drive and Github

//For google API - google calendar
Client ID: 180545132631-d8hshjcnjr3ku8jkv41khaiak0e3ov5a.apps.googleusercontent.com 
Client secret: DNLrSCTMUSLTxWolewHv38bK

//For google voice API
API Key: 7f6a75b42ab6b7ba9833fe7449cd55659bfa825f 

//For witai 
access token: 47WABYDCE3U2IXOSDLUIHPJMGDKS4FTH

//WolframAlpha APPID: 5A2L2L-7XA8TPTPTV

//Evernote dev token: S=s1:U=9543a:E=1716905b6b2:C=16a11548950:P=1cd:A=en-devtoken:V=2:H=687818b9cc16d7a86d303aa54e33e35b

 
LEDs
Sources used:
http://wiki.seeedstudio.com/ReSpeaker_4_Mic_Array_for_RIspberry_Pi/

Direction of arrival installation and use:
I combined and rewrote the vad_doa.py and pixels.py files to create a functioning DOA.
For the DOA, working prototype is in DOA.py (home/pi/mic_array)
For DOA to work, you would need to have the whole mic_array folder for imports

Installation:
Install dependancies:
-> git clone https://github.com/respeaker/4mics_hat.git
-> git clone https://github.com/respeaker/mic_array.git
-> cd mic_array
-> nano vad_doa.py 
-> #change CHANNELS = 8 to CHANNELS = 4 @line10 -> You need to change the mic to 4 due to only having 4 mics
-> git clone https://github.com/respeaker/pixel_ring.git
-> cd pixel_ring
-> pip install -U -e .
-> Copy from 4mic_hat folder, alexa_led_pattern.py and google_home_led_pattern.py to the folder mic_array as the test2 will need it for imports

LED dependancies:
-> sudo pip install spidev gpiozero
-> sudo apt-get install portaudio19-dev
-> sudo pip install pyaudio
-> sudo pip install webrtcvad
-> sudo apt-get install python-numpy 
-> sudo pip install pyusb
 
Light command and function use:
-> For the leds, the functions for basic light functions are in the LightCommands.py (home/pi/pixel/pixel_ring).
-> LightCommand needs to import pixel_ring -> would NEED the pixel_ring folder for LightCommand to work
-> LightCommand.py is used in:
-> jasper.py -> inside def run()
-> conversation.py -> inside def handleForever()

Things left to do:
Add the lighting effects to the modules (before, during and after the module has been called). Mostly done, lighting effects would need to be added before it is called and also after it is called.
Merge the functions for DOA.py and jasper.py/lightcommand.py as a loop to make it checks for DOA until jasper is turned off.
Make jasper headless to avoid unnecessary wires when using with the table.


