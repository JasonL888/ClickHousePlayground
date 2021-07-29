from random import randint, gauss, choice
import json
import string
from datetime import datetime, timedelta

periodicInterval = 15 # minutes

def randMac():
	return( "3c:22:fb:%02x:%02x:%02x" % (randint(0,255),randint(0,255),randint(0,255)) )

def randStr(chars = string.ascii_uppercase + string.digits, N=10):
	return( ''.join(choice(chars) for _ in range(N)) )

def randSignalStrength():
	return( int(gauss(-27,5)) )

class CPE:
	def __init__(self, SerialNumber, Manufacturer, ModelName, HardwareVersion, SoftwareVersion):
		startDate = datetime.now() + timedelta(days=-30 )
		self.EventDate =  startDate.strftime("%Y-%m-%d")
		self.EventDateTime = self.EventDate + " 00:00:00"
		self.SerialNumber = SerialNumber
		self.Manufacturer = Manufacturer
		self.ModelName = ModelName
		self.HardwareVersion = HardwareVersion
		self.SoftwareVersion = SoftwareVersion
		self.MemoryStatus_Total = 64000
		self.MemoryStatus_Free = randint( 32000, int(64000 * 0.8) )
		self.UpTime = randint(1,100000000)
		self._genWiFiAccessPoint()
		# Should be nested within Device.WiFi.AccessPoint
		# but clickhouse has problems with double nest
		self._genWiFiAssociatedDevice()
		self._genWiFiSSID()
		self._genWiFiRadio()
		#        self._genHostEntries();
	def _genWiFiAccessPoint(self):
		securityModeEnabled = [
			"None",
			"WEP-64",
			"WEP-128",
			"WPA-Personal",
			"WPA2-Personal",
			]
		self.WiFi_AccessPointNumberOfEntries = 2
		self.WiFi_AccessPoint = {}
		self.WiFi_AccessPoint['ID'] = [1,2]
		self.WiFi_AccessPoint['Status'] = ["Up","Up"]
		self.WiFi_AccessPoint['SSIDReference'] = ["Device.WiFi.SSID.1", "Device.WiFi.SSID.2"]
		self.WiFi_AccessPoint['Security_ModeEnabled'] = [securityModeEnabled[randint(0,len(securityModeEnabled)-1)],securityModeEnabled[randint(0,len(securityModeEnabled)-1)]]

	def _genWiFiAssociatedDevice(self):
		self.WiFi_AccessPoint['AssociatedDeviceNumberOfEntries'] = []
		self.WiFi_AccessPoint_AssociatedDevice = {}
		self.WiFi_AccessPoint_AssociatedDevice['ID'] = []
		self.WiFi_AccessPoint_AssociatedDevice['AccessPointReference'] = []
		self.WiFi_AccessPoint_AssociatedDevice['MACAddress'] = []
		self.WiFi_AccessPoint_AssociatedDevice['SignalStrength'] = []
		self.WiFi_AccessPoint_AssociatedDevice['Active'] = []
		self.WiFi_AccessPoint_AssociatedDevice['LastDataUplinkRate'] = []
		self.WiFi_AccessPoint_AssociatedDevice['LastDataDownlinkRate'] = []
		self.WiFi_AccessPoint_AssociatedDevice['Retransmissions'] = []
		for i in range(1, self.WiFi_AccessPointNumberOfEntries + 1):
			AssociatedDeviceNumberOfEntries = int(gauss(7, 5))
			if ( AssociatedDeviceNumberOfEntries < 0 ):
				AssociatedDeviceNumberOfEntries = 0;
			self.WiFi_AccessPoint['AssociatedDeviceNumberOfEntries'].append(AssociatedDeviceNumberOfEntries)
			for j in range(1, AssociatedDeviceNumberOfEntries + 1):
				Retransmissions = gauss(0,2)
				self.WiFi_AccessPoint_AssociatedDevice['ID'].append(j)
				self.WiFi_AccessPoint_AssociatedDevice['AccessPointReference'].append("Device.WiFi.AccessPoint." + str(i))
				self.WiFi_AccessPoint_AssociatedDevice['MACAddress'].append(randMac())
				self.WiFi_AccessPoint_AssociatedDevice['SignalStrength'].append(int(gauss(-27,5)))
				self.WiFi_AccessPoint_AssociatedDevice['Active'].append(1)
				self.WiFi_AccessPoint_AssociatedDevice['LastDataUplinkRate'].append(int(gauss(200000,50000)))
				self.WiFi_AccessPoint_AssociatedDevice['LastDataDownlinkRate'].append(int(gauss(200000,50000)))
				self.WiFi_AccessPoint_AssociatedDevice['Retransmissions'].append(int(Retransmissions if Retransmissions > 0 else 0))
	def _genWiFiSSID(self):
		Discard = gauss(0,2)
		Discard2 = gauss(0,2)
		Errors = gauss(0,2)
		Errors2 = gauss(0,2)
		self.WiFi_SSID = {}
		self.WiFi_SSID['ID'] = [1,2]
		self.WiFi_SSID['BSSID']= [randMac(),randMac()]
		self.WiFi_SSID['LowerLayers'] = ["Device.WiFi.Radio.1","Device.WiFi.Radio.2"]
		self.WiFi_SSID['SSID'] = [randStr(),randStr()]
		self.WiFi_SSID['Status'] = ["Up","Up"]
		self.WiFi_SSID['BytesSent'] = [int(gauss(800000,80000)),int(gauss(800000,80000))]
		self.WiFi_SSID['BytesReceived']=[int(gauss(800000,80000)),int(gauss(800000,80000))]
		self.WiFi_SSID['DiscardPacketsReceived']=[int(Discard if Discard > 0 else 0),int(Discard2 if Discard2 > 0 else 0)]
		self.WiFi_SSID['DiscardPacketsSent']=[int(Discard if Discard > 0 else 0),int(Discard2 if Discard2 > 0 else 0)]
		self.WiFi_SSID['ErrorsReceived']=[int(Errors if Errors > 0 else 0),int(Errors2 if Errors2 > 0 else 0)]
		self.WiFi_SSID['ErrorsSent']=[int(Errors if Errors > 0 else 0),int(Errors2 if Errors2 > 0 else 0)]
		self.WiFi_SSID['PacketsReceived']=[int(gauss(1000,10)),int(gauss(1000,10))]
		self.WiFi_SSID['PacketsSent']=[int(gauss(1000,10)),int(gauss(1000,10))]
		self.WiFi_SSIDNumberOfEntries = 2
	def _genWiFiRadio(self):
		channels_5G = [36, 40, 44, 48, 149, 153, 157, 161, 165]
		self.WiFi_Radio = {}
		self.WiFi_Radio['ID'] = [1,2]
		self.WiFi_Radio['AutoChannelEnable'] = [randint(0,1),randint(0,1)]
		self.WiFi_Radio['Channel'] = [randint(1,11),channels_5G[randint(0,len(channels_5G)-1)]]
		self.WiFi_Radio['CurrentOperatingChannelBandwidth'] = ["20MHz", "20MHz"]
		self.WiFi_Radio['Status'] = ["Up","Up"]
		self.WiFi_Radio['MaxBitRate'] = [int(gauss(1000,50)),int(gauss(1000,50))]
		self.WiFi_Radio['OperatingFrequencyBand'] = ["2.4GHz", "5GHz"]
		self.WiFi_RadioNumberOfEntries = 2
	def getJSON(self):
		return( json.dumps(self, default=lambda o: o.__dict__, sort_keys=True) )
	def nextPII(self):
		self.randMemStats()
		self.updateDateTime()
		self.updateUpTime()
		self.updateNetworkStats()
	def randMemStats(self):
		self.MemoryStatus_Free = int( gauss(self.MemoryStatus_Free, self.MemoryStatus_Total * 0.1) )
		if ( self.MemoryStatus_Free > self.MemoryStatus_Total ):
			self.MemoryStatus_Free = self.MemoryStatus_Total
		elif ( self.MemoryStatus_Free < 0 ):
			self.MemoryStatus_Free = 0
	def updateDateTime(self):
		lastDateTime = datetime.strptime(self.EventDateTime, '%Y-%m-%d %H:%M:%S')
		newDateTime = lastDateTime + timedelta(minutes=periodicInterval)
		self.EventDateTime = newDateTime.strftime("%Y-%m-%d %H:%M:%S")
		self.EventDate = newDateTime.strftime("%Y-%m-%d")
	def updateUpTime(self):
		self.UpTime = self.UpTime + (periodicInterval * 60)
	def updateNetworkStats(self):
		for i in range(0, self.WiFi_SSIDNumberOfEntries -1 ):
			Discard = gauss(0,2)
			Errors = gauss(0,2)
			self.WiFi_SSID['BytesSent'][i] = self.WiFi_SSID['BytesSent'][i] + int(gauss(80000,8000))
			self.WiFi_SSID['BytesReceived'][i] = self.WiFi_SSID['BytesReceived'][i] + int(gauss(80000,8000))
			self.WiFi_SSID['DiscardPacketsReceived'][i] = self.WiFi_SSID['DiscardPacketsReceived'][i] + int(Discard if Discard > 0 else 0)
			self.WiFi_SSID['DiscardPacketsSent'][i] = self.WiFi_SSID['DiscardPacketsSent'][i] + int(Discard if Discard > 0 else 0)
			self.WiFi_SSID['ErrorsReceived'][i] = self.WiFi_SSID['ErrorsReceived'][i] + int(Errors if Errors > 0 else 0)
			self.WiFi_SSID['ErrorsSent'][i] = self.WiFi_SSID['ErrorsSent'][i] + int(Errors if Errors > 0 else 0)
			self.WiFi_SSID['PacketsReceived'][i] = self.WiFi_SSID['PacketsReceived'][i] + int(gauss(100,10))
			self.WiFi_SSID['PacketsSent'][i] = self.WiFi_SSID['PacketsSent'][i] + int(gauss(100,10))

#    def _genHostEntries(self):
#        self.Hosts = []
#        self.HostNumberOfEntries = randint( 0, 15 )
#        for i in range(1, self.HostNumberOfEntries+1):
#            self.Hosts.append(
#                {
#                    "ID": i,
#                    "Active": randint(0,1),
#                    "IPAddress": "192.168.1" + str(randint(1,254)),
#                    "HostName" : randStr(),
#                }
#            )

# loop for interval
#    loop for cpe
#        generate EventDateTime, CPE details (serial, SoftwareVersion, etc)
#        generate memory status
#        generate uptime
#        generate Hosts nest
#        generate Ethernet nest
#        generate IP nest
#        generate WiFi_AccessPoint nest
#        generate WiFI_SSID nest
#        export JSON and append to file

if __name__ == "__main__":
	jsonBuffer = {}
	cpe1 = CPE('VDLINNNE1808009701', 'Realtek', 'DL4480V1_2019', "RTL960x", "DL4480V1_2.0.9e")
	print(cpe1.getJSON())
	cpe1.nextPII()
	print(cpe1.getJSON())
	cpe1.nextPII()
	print(cpe1.getJSON())
