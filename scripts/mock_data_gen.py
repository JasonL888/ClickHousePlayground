from random import randint, gauss, choice
import json
import string
from datetime import datetime

def randMac():
	return( "3c:22:fb:%02x:%02x:%02x" % (randint(0,255),randint(0,255),randint(0,255)) )

def randStr(chars = string.ascii_uppercase + string.digits, N=10):
	return ''.join(choice(chars) for _ in range(N))

class CPE:
	def __init__(self, SerialNumber, Manufacturer, ModelName):
		today = datetime.now()
		self.eventDate =  today.strftime("%Y-%m-%d")
		self.eventDateTime = today.strftime("%Y-%m-%d %H:%M:%S")
		self.SerialNumber = SerialNumber
		self.Manufacturer = Manufacturer
		self.ModelName = ModelName
		self.MemoryStatus_Total = 64000
		self.MemoryStatus_Free = randint( 32000, int(64000 * 0.8) )
		self.UpTime = randint(1,100000000)
		self._genWiFiAccessPoint()
		self._genWiFiSSID()
		self._genWiFiRadio()
		#        self._genHostEntries();
	def _genWiFiAccessPoint(self):
		self.WiFi_AccessPoint = []
		self.WiFi_AccessPointNumberOfEntries = 2
		securityModeEnabled = [
			"None",
			"WEP-64",
			"WEP-128",
			"WPA-Personal",
			"WPA2-Personal",
			]
		for i in range(1, self.WiFi_AccessPointNumberOfEntries + 1):
			AssociatedDeviceNumberOfEntries = int(gauss(7, 5))
			AssociatedDevices = []
			for j in range(1, AssociatedDeviceNumberOfEntries - 1):
				Retransmissions = gauss(0,2)
				AssociatedDevices.append(
					{
					    "ID": j,
						"MACAddress": randMac(),
						"SignalStrength": int(gauss(-27,5)),
						"Active": 1,
						"LastDataUplinkRate": int(gauss(200000,50000)),
						"LastDataDownlinkRate": int(gauss(200000,50000)),
						"Retransmissions": int(Retransmissions if Retransmissions > 0 else 0)
					}
				)
			self.WiFi_AccessPoint.append(
				{
					"ID": i,
					"Status": "Up",
					"SSIDReference": "Device.WiFi.SSID." + str(i),
					"SecurityModeEnabled" : securityModeEnabled[randint(0,len(securityModeEnabled)-1)],
					"AssociatedDevices": AssociatedDevices
				}
			)
	def _genWiFiSSID(self):
		self.WiFi_SSID = []
		self.WiFi_SSIDNumberOfEntries = 2
		for i in range(1, self.WiFi_SSIDNumberOfEntries + 1):
			Discard = gauss(0,2)
			Errors = gauss(0, 2)
			self.WiFi_SSID.append(
				{
					"ID":i,
					"BSSID": randMac(),
					"Enable": 1,
					"LowerLayers": "Device.WiFi.Radio" + str(i),
					"SSID": randStr(),
					"Status": "Up",
					"BytesSent": int(gauss(800000,80000)),
					"BytesReceived": int(gauss(800000,80000)),
					"DiscardPackaetsReceived": int(Discard if Discard > 0 else 0),
					"DiscardPacketsSent": int(Discard if Discard > 0 else 0),
					"ErrorsReceived": int(Errors if Errors > 0 else 0),
					"ErrorsSent": int(Errors if Errors > 0 else 0),
					"PacketsReceived": int(gauss(1000,10)),
					"PacketsSent": int(gauss(1000,10)),
				}
			)
	def _genWiFiRadio(self):
		channels_5G = [36, 40, 44, 48, 149, 153, 157, 161, 165]
		self.WiFi_Radio = []
		self.WiFi_Radio.append(
			{
				"ID": 1,
				"AutoChannelEnable": randint(0,1),
				"Channel": randint(1,11),
				"CurrentOperatingChannelBandwidth": "20MHz",
				"Status": "Up",
				"MaxBitRate": int(gauss(1000,50)),
				"OperatingFrequencyBand": "2.4GHz"
			}
		)
		self.WiFi_Radio.append(
			{
				"ID": 2,
				"AutoChannelEnable": randint(0,1),
				"Channel": channels_5G[randint(0,len(channels_5G)-1)],
				"CurrentOperatingChannelBandwidth": "20MHz",
				"Status": "Up",
				"MaxBitRate": int(gauss(1000,50)),
				"OperatingFrequencyBand": "5GHz"
			}
		)
		self.WiFi_RadioNumberOfEntries = len(self.WiFi_Radio)
	def getJSON(self):
		return( json.dumps(self, default=lambda o: o.__dict__, sort_keys=True) )
	def randMemStats(self):
		self.MemoryStatus_Free = int( gauss(self.MemoryStatus_Free, self.MemoryStatus_Total * 0.1) )
		if ( self.MemoryStatus_Free > self.MemoryStatus_Total ):
			self.MemoryStatus_Free = self.MemoryStatus_Total
		elif ( self.MemoryStatus_Free < 0 ):
			self.MemoryStatus_Free = 0

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
	cpe1 = CPE('VDLINNNE1808009701', 'Realtek', 'DL4480V1_2019')
	cpe1.randMemStats()
	print(cpe1.getJSON())
