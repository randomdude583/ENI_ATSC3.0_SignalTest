#written in Python3 By Alex Collette
#Edge Networks
#5/21/2019
######################################
#           Lifecycle Overview
#
#  Start up StreamScope and begin recieving packets.
#  -Enter Loop-   Loop for set amount of time, pulling data every (interval) seconds
#       Scrape data from web page.
#       Open Storage file and read data.
#       Store data from readings.
#       Update mins, maxs and averages.
#       Close file.
#  -Exit Loop-
#
#  After looping finishes, close StreamScope and exit.
#
######################################


from bs4 import BeautifulSoup
#import requests
import smtplib, ssl
import re



##  Init Variables  ##
recordTime = 300   # Time to run(Seconds)
interval = 5       # Time between recordings

##  Storage Variables  ##
startTime = 0     # Time the program was started
readingsTaken = 0 # Total number of recordings
location = "DEMO" # User input for location
frequency = 0     # Signal frequency
bitrate = 0       # Signal bitrate
snr = 0           # Signal to noise ratio
rssi = 0          # Signal Strength
snq = 0           # Signal Quality
packetLoss = 0    # Packets loss

#################











######################   Start StreamScope   ##################









#########################   Scrape Data    ####################
def scrapeData():

	# Initialize Soup
	url = "localhost"
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'lxml')










#######################    Write to File    ##################
def writeFile():

	## Temp Variables ##
	curMaxBitrate = 5
	curMinBitrate = 5
	curAvgBitrate = 5

	curMaxSNR = 0
	curMinSNR = 0
	curAvgSNR = 0

	curMaxRSSI = 0
	curMinRSSI = 0
	curAvgRSSI = 0

	curMaxSignalQuality = 0
	curMinSignalQuality = 0
	curAvgSignalQuality = 0

	curMaxPacketLoss = 0
	curMinPacketLoss = 0
	curAvgPacketLoss = 0

	####################



	if readingsTaken > 1:
		#Open current datafile
		with open("demofile2.txt") as fp:  
			line = fp.readline()
			cnt = 1
			# skip the first 4 lines
			while line and cnt < 4:
				line = fp.readline
				cnt += 1

			#Capture bitrate data
			line = fp.readline
			line = fp.readline
			#curMaxBitrate = fp.readline
			#curMinBitrate = fp.readline
			#curAvgBitrate = fp.readline

			#Capture SNR data
			line = fp.readline
			line = fp.readline
			curMaxSNR = fp.readline
			curMinSNR = fp.readline
			#curAvgSNR = fp.readline

			#Capture RSSI data
			line = fp.readline
			line = fp.readline
			curMaxRSSI = fp.readline
			curMinRSSI = fp.readline
			#curAvgRSSI = fp.readline

			#Capture Signal Quality data
			line = fp.readline
			line = fp.readline
			curMaxSignalQuality = fp.readline
			curMinSignalQuality = fp.readline
			#curAvgSignalQuality = fp.readline

			#Capture Packet Loss data
			line = fp.readline
			line = fp.readline
			curMaxPacketLoss = fp.readline
			curMinPacketLoss = fp.readline
			#curAvgPacketLoss = fp.readline



	t = open("tempfile.txt", "w")  #Open replacement file
	t.write("Frequency: " + str(frequency))
	t.write("\nTimeStamp: " + str(startTime))
	t.write("\nLocation: " + location)
	t.write("\n#Readings: " + str(readingsTaken))
	t.write("\n\nBitrate")
	if bitrate < curMinBitrate:
		curMinBitrate = bitrate 
	t.write("\n    Min: " + str(curMinBitrate))
	if bitrate > curMaxBitrate:
		curMaxBitrate = bitrate
	t.write("\n    Max: " + str(curMaxBitrate))
	t.write("\n    Avg: " + str((curAvgBitrate*(readingsTaken-1) + bitrate)/readingsTaken))


	t.write("\n\nSNR")
	t.write("\n    Min: ")
	t.write("\n    Max: ")
	t.write("\n    Avg: " + str((curAvgSNR*(readingsTaken-1) + snr)/readingsTaken))
	

	t.write("\n\nRSSI")
	t.write("\n    Min: ")
	t.write("\n    Max: ")
	t.write("\n    Avg: " + str((curAvgRSSI*(readingsTaken-1) + rssi)/readingsTaken))
	

	t.write("\n\nSignal Quality")
	t.write("\n    Min: ")
	t.write("\n    Max: ")
	t.write("\n    Avg: " + str((curAvgSignalQuality*(readingsTaken-1) + snq)/readingsTaken))
	

	t.write("\n\nPacket Loss")
	t.write("\n    Min: ")
	t.write("\n    Max: ")
	t.write("\n    Avg: " + str((curAvgPacketLoss*(readingsTaken-1) + packetLoss)/readingsTaken))


	t.close()

readingsTaken = readingsTaken+1
writeFile()