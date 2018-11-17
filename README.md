## Getting Started

	1) Enable Serial:
		1.a) In terminal type `sudo raspi-config`
		1.b) Go to advanced options and select/enable 'Serial'
		
	2) Dependencies
		2.a) Install dependencies
			 `sudo pip install requests`
			 `sudo pip install python-firebase`
	3) Barcode script
		3.a) Download the code from GitHub:
			There are three methods to download the code, choose one based on accessibility and ease of use.
			3.a.i) A download agent like `wget` or `curl -O`
				You can obtain a `.zip` archive version of this repo by downloading from `https://github.com/BarnabasRobotics/rpi-barcode/archive/master.zip`.
			3.a.ii) Git, or another SCM
				If you have `git` installed, (check by typing `git --version` and ensuring the command is found), you may simply `clone` this repo; `git clone https://github.com/BarnabasRobotics/rpi-barcode`
			3.a.iii} Download from web browser
				Finally, you can also simply visit the repo page (that's https://github.com/BarnabasRobotics/rpi-barcode), hit the green "Clone or Download", and click "Download ZIP".
		3.b) Extracting
			3.a.i) If you used a method other that `git`, you will need to also unzip the resulting archive. You may do so using a graphical file browser, or using the command line.
	4) Running the code
		4.a) Open up a terminal, and `cd` to the repo folder, then in the `pi-code` subdir.
		4.b) The time has come! You may now execute the code with `sudo python barcode.py`.
		4.b) Finally, just follow the instructions on the screen!
	5) Problems?
		5.a) Feel free to open an issue on this repo if you encounter any hairy issues!