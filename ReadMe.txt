This package is done to enable streaming of the pupil tracking and empatica data.
-------------------------------------------------------------------------------------
Before Using the package make sure :

--> Python is installed on your computer, create a venv and install required packages:
		(in the repository path)
		--> python3 -m venv venv/
		--> ./venv/script/activate (IN case of error you will probably have to enable powershell script :
				{
					run powershell in admin mode and type :
					Set-ExecutionPolicy RemoteSigned
					then YES 
				}
		--> pip install -r requirements.txt

--> Install Empatica Streaming server https://developer.empatica.com/windows-streaming-server.html ,  if an API key is needed 

--> Install BLE library :
as said on the empatica install guide : https://developer.empatica.com/windows-streaming-server-usage.html, you need to install BLE library, to do it :
	--> go to https://www.silabs.com/wireless/bluetooth/bluegiga-low-energy-legacy-modules/device.bled112 and download "Bluetooth Low Energy Software and SDK v.1.6.0" & "BLED112 Windows Driver"
	--> extract the files of BLED112 Windows driver and then go to windrv, then right click on both INF files anc select "install" from from menu.
	--> run Bluegiga_ble-1.6.0-140.exe and install it.
	--> Restart your computer

--> Install Pupil core software from https://docs.pupil-labs.com/core/

--> (in the repository path) Create a short link to pupil_capture.exe and name it Pupil_Capture

--> plug an ethernet cable to connect your computer to your router

--> you need to create an exception for python in your firewall or disable your firewall

--> The Raspberry has been set up on the network and has mjpg_streamer installed on it. Create a script file and put stream_cam.script in the folder such as ~/script/stream_cam.script gives access to script. Do the same for Comm_rasp_client.py.

--> You need to modify the Record_client.py to write the name of your Empatica device in the string variable "device".
------------------------------------------------------------------------------------
FOR EACH SUBJECT
	Step 0 -> Find your IP adress and the Raspberry IP adress

	Step 1 -> plug the pupil device to raspberry, plug BLE dongle to computer

	Step 2 -> (in the repository path) type in powershell .\start_stream.ps1 <IP_computer_that_receives_stream> <Comm_port_rasp (12345)> <IP_rasbperry> <path_to_launch_capture (use a shortlink)(.\Pupil_Capture.lnk)>

	Step 3 -> Wait for stream to be redirected and for capture to start

	FOR EACH SESSION

		Step 4 -> (Check) Adjust Cameras, adjust settings in campture and calibrate (on a TV screen probably)

		Step 5 -> Run empatica streaming server on your computer

		Step 6 -> Turn on empatica E4 and connect it to the empatica streaming server check the name of the device connected you will need it later

		Step 7 -> Create a directory in the directory of record_client.py, call it Subject_X (X is whatever number you want eg Subject_0) in that directory create 3 directory named : Session_1,Session_2,Session_3

		Step 8 -> Start a new powershell and Run : (Except for tutorial)
		(in the repository path)
 		        --> .\venv\Scripts\activate
				--> python .\Record_client.py <Subject_X> <Session_1/Session_2/Session_3> 0 (Check that the powershell tells you "Receiving data from Empatica" & "Receiving data from pupil" (if not maybe restart Empatica & streaming server)
				--> type record

		TO STOP RECORDING

		Step 9 -> type in powershell (colelction empatica and pupil) : end_rec (Except for tutorial) turn off the empatica