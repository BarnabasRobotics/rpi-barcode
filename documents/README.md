Instructions to get pi and barcode scanner to interact:

	1)Enable Serial
		1.a) In terminal type `sudo raspi-config`
		1.b) Go to advanced options and select/enable 'Serial'
		
	2)Python code to pi
		2.a) Install dependencies
			 `sudo pip install requests`
			 `sudo pip install python-firebase`
		2.b) Download the python code to the pi from github
			 https://github.com/BarnabasRobotics/rpi-barcode
		2.c) Go into the folder that says 'pi code' and download 'barcode.py'
		
	3)Run the code
		3.a) Go into the pi terminal and enter `sudo python barcode.py`
		3.b) Enter students name
		3.c) Scan any barcode
		3.d) Repeat