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
import smtplib, ssl
import re
import datetime
import os
from time import gmtime, strftime




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

fileName = ""     # Target filename for storing data. This is generated programatically.

#################











######################   Start Program   ##################
currentDT = datetime.datetime.now()
startTime = str(currentDT.strftime("%Y-%m-%d %H:%M:%S"))
formatted = str(currentDT.strftime("%Y-%m-%d_%H%M"))
fileName = location + "_" + formatted + "_TEST"".txt"









#########################   Scrape Data    ####################
def scrapeData():

	# Initialize Soup
	url = "localhost"
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'lxml')










#######################    Write to File    ##################
def writeFile(bitrate, snr, rssi, snq, packetLoss):

	## Temp Variables ##
	curMaxBitrate = -1
	curMinBitrate = -1
	curAvgBitrate = -1

	curMaxSNR = -1
	curMinSNR = -1
	curAvgSNR = -1

	curMaxRSSI = -1
	curMinRSSI = -1
	curAvgRSSI = -1

	curMaxSignalQuality = -1
	curMinSignalQuality = -1
	curAvgSignalQuality = -1

	curMaxPacketLoss = -1
	curMinPacketLoss = -1
	curAvgPacketLoss = -1

	####################



	if readingsTaken > 1:
		#Open current datafile
		with open(fileName) as fp:  
			line = fp.readline()
			cnt = 1
			# skip the first 4 lines
			while line and cnt < 4:
				line = fp.readline()
				cnt += 1

			#Capture bitrate data
			line = fp.readline()
			line = fp.readline()
			curMinBitrate = float(re.sub('[a-z,A-Z, ,:]', '', str(fp.readline())))
			curMaxBitrate = float(re.sub('[a-z,A-Z, ,:]', '', str(fp.readline())))
			curAvgBitrate = float(re.sub('[a-z,A-Z, ,:]', '', str(fp.readline())))

			#Capture SNR data
			line = fp.readline()
			line = fp.readline()
			curMinSNR = float(re.sub('[a-z,A-Z, ,:]', '', str(fp.readline())))
			curMaxSNR = float(re.sub('[a-z,A-Z, ,:]', '', str(fp.readline())))
			curAvgSNR = float(re.sub('[a-z,A-Z, ,:]', '', str(fp.readline())))

			#Capture RSSI data
			line = fp.readline()
			line = fp.readline()
			curMinRSSI = float(re.sub('[a-z,A-Z, ,:]', '', str(fp.readline())))
			curMaxRSSI = float(re.sub('[a-z,A-Z, ,:]', '', str(fp.readline())))
			curAvgRSSI = float(re.sub('[a-z,A-Z, ,:]', '', str(fp.readline())))

			#Capture Signal Quality data
			line = fp.readline()
			line = fp.readline()
			curMinSignalQuality = float(re.sub('[a-z,A-Z, ,:]', '', str(fp.readline())))
			curMaxSignalQuality = float(re.sub('[a-z,A-Z, ,:]', '', str(fp.readline())))
			curAvgSignalQuality = float(re.sub('[a-z,A-Z, ,:]', '', str(fp.readline())))

			#Capture Packet Loss data
			line = fp.readline()
			line = fp.readline()
			curMinPacketLoss = float(re.sub('[a-z,A-Z, ,:]', '', str(fp.readline())))
			curMaxPacketLoss = float(re.sub('[a-z,A-Z, ,:]', '', str(fp.readline())))
			curAvgPacketLoss = float(re.sub('[a-z,A-Z, ,:]', '', str(fp.readline())))

			fp.close()



	t = open("tempfile.txt", "w")  #Open replacement file
	t.write("Frequency: " + str(frequency))
	t.write("\nTimeStamp: " + str(startTime))
	t.write("\nLocation: " + location)
	t.write("\n#Readings: " + str(readingsTaken))



	#Update Mins, Maxs and Avgs

	t.write("\n\nBitrate")
	if bitrate < curMinBitrate or curMinBitrate == -1:
		curMinBitrate = bitrate 
	t.write("\n    Min: " + str(curMinBitrate))
	if bitrate > curMaxBitrate:
		curMaxBitrate = bitrate
	t.write("\n    Max: " + str(curMaxBitrate))
	t.write("\n    Avg: " + str((curAvgBitrate*(readingsTaken-1) + bitrate)/readingsTaken))


	t.write("\n\nSNR")
	if snr < curMinSNR or curMinSNR == -1:
		curMinSNR = snr
	t.write("\n    Min: " + str(curMinSNR))
	if snr > curMaxSNR:
		curMaxSNR = snr
	t.write("\n    Max: " + str(curMaxSNR))
	t.write("\n    Avg: " + str((curAvgSNR*(readingsTaken-1) + snr)/readingsTaken))
	

	t.write("\n\nRSSI")
	if rssi < curMinRSSI or curMinRSSI == -1:
		curMinRSSI = rssi
	t.write("\n    Min: " + str(curMinRSSI))
	if rssi > curMaxRSSI:
		curMaxRSSI = rssi
	t.write("\n    Max: " + str(curMaxRSSI))
	t.write("\n    Avg: " + str((curAvgRSSI*(readingsTaken-1) + rssi)/readingsTaken))
	

	t.write("\n\nSignal Quality")
	if snq < curMinSignalQuality or curMinSignalQuality == -1:
		curMinSignalQuality = snq
	t.write("\n    Min: " + str(curMinSignalQuality))
	if snq > curMaxSignalQuality:
		curMaxSignalQuality = snq
	t.write("\n    Max: " + str(curMaxSignalQuality))
	t.write("\n    Avg: " + str((curAvgSignalQuality*(readingsTaken-1) + snq)/readingsTaken))
	

	t.write("\n\nPacket Loss")
	if packetLoss < curMinPacketLoss or curMinPacketLoss == -1:
		curMinPacketLoss = packetLoss
	t.write("\n    Min: " + str(curMinPacketLoss))
	if packetLoss > curMaxPacketLoss:
		curMaxPacketLoss = packetLoss
	t.write("\n    Max: " + str(curMaxPacketLoss))
	t.write("\n    Avg: " + str((curAvgPacketLoss*(readingsTaken-1) + packetLoss)/readingsTaken))




	# Copy over all Previous readings
	if readingsTaken > 1:
		with open(fileName) as fp2:  
			lineread = fp2.readline()
			cnt = 1
			# skip the stuff we already wrote to file
			while lineread:
				if cnt < 29:
					lineread = fp2.readline()

					#Copy the rest of the file into the new file
				elif cnt == 29:
					t.write("\n")
				else:
					lineread = fp2.readline()
					t.write(lineread)

				cnt += 1



	else:
		t.write("\n\n\n\nResults:\n-----------------------------------------------------------------")

	# Write new data to file
	currentDT = datetime.datetime.now()
	t.write("\nTimeStamp: " + str(currentDT.strftime("%Y-%m-%d %H:%M:%S"))) # Write Timestamp
	t.write("\nBitrate: " + str(bitrate)) # Write Bitrate
	t.write("\nSNR: " + str(snr)) # Write SNR
	t.write("\nRSSI: " + str(rssi)) # Write RSSI
	t.write("\nSignal Quality: " + str(snq)) # Write Signal Quality
	t.write("\nPacket Loss: " + str(packetLoss)) # Write Packet Loss
	t.write("\n")
	t.write("\n-----------------------------------------------------------------")




	t.close()
	try:
		os.remove(fileName)
	except:
		pass
	os.rename('tempfile.txt', fileName)

readingsTaken = readingsTaken+1  #TODO: Remove this line, will be replaced by an incrementer in the scrape section
writeFile(10, 20, 14, 17, 12)
readingsTaken = readingsTaken+1  #TODO: Remove this line, will be replaced by an incrementer in the scrape section
writeFile(15, 5, 19, 14, 3)
readingsTaken = readingsTaken+1  #TODO: Remove this line, will be replaced by an incrementer in the scrape section
writeFile(30, 36, 25, 31, 9)

readingsTaken = readingsTaken+1  #TODO: Remove this line, will be replaced by an incrementer in the scrape section
writeFile(30, 36, 25, 31, 9)