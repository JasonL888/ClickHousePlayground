# Clickhouse Playground
Playground with Clickhouse in docker container


# Pre-requisite
* Docker desktop installed
* Python3 installed
* (Optional) Run script to generate mock data
```
python script\mock_data_gen.py
```


# Start Up
In the folder with docker-compose.yml,
```
docker-compose up
```

# Setup Clickhouse schema
Access bash on container "ch01"
```
docker exec -it ch01 bash
```

Access clickhouse client
```
clickhouse-client --multiline
```

On clickhouse client,
* configure to flatten nested fields (Optional - by default already enabled)
```
SET flatten_nested = 1;
```

* configure to allow nested json import
```
SET input_format_import_nested_json=1;
```

* Create database, cpe
```
CREATE DATABASE IF NOT EXISTS cpe;
```

* Create schema
```
CREATE TABLE cpe.kpi
(
  EventDate Date,
  EventDateTime DateTime,
  HardwareVersion String, -- "RTL960x"
  SoftwareVersion String, -- "DL4480V1_2.0.9e"
  Manufacturer String, --"Realtek"
  ModelName String, -- "DL4480V1_2019"
  SerialNumber String, --"VDLINNNE1808009701"
  MemoryStatus_Free UInt16, --27424
  MemoryStatus_Total UInt16, -- 53528
  UpTime UInt16,
--  HostNumberOfEntries UInt8,
--  Hosts Nested (
--    ID UInt8,
--    Active UInt8,
--    HostName String,
--    IPAddress String,
--    Layer1Interface String, -- Device.Ethernet.Interface.1
--    Layer3Interface String, -- Device.IP.Interface.1
--    PhyAddress String
--  ),
--  Ethernet_InterfaceNumberOfEntries UInt8,
--  Ethernet_Interface Nested (
--    ID UInt8,
--    Name String, -- "eth0.2"
--    Enable UInt8,
--    MACAddress String,
--    Status UInt8,
--    BytesSent UInt64, -- Stats.BytesSent
--    BytesReceived UInt64,
--    DiscardPacketsReceived UInt32,
--    DiscardPacketsSent UInt32,
--    ErrorsReceived UInt32,
--    ErrorsSent UInt32,
--    PacketsReceived UInt64,
--    PacketsSent UInt64
--  ),
--  IP_InterfaceNumberOfEntries UInt8,
--  IP_Interface Nested (
--    ID UInt8,
--    Name String,
--    Enable UInt8,
--    LowerLayers String, -- Device.Ethernet.Link.1
--    Status UInt8, -- Up
--    BytesSent UInt64, -- Stats.BytesSent
--    BytesReceived UInt64,
--    DiscardPacketsReceived UInt32,
--    DiscardPacketsSent UInt32,
--    ErrorsReceived UInt32,
--    ErrorsSent UInt32,
--    PacketsReceived UInt64,
--    PacketsSent UInt64
--  ),
  WiFi_AccessPointNumberOfEntries UInt8,
  WiFi_AccessPoint Nested (
    ID UInt8,
    SSIDReference String, -- Device.WiFi.SSID.1
    Security_ModeEnabled String,
    Status String, -- Enabled
    AssociatedDeviceNumberOfEntries UInt8
  ),
  WiFi_AccessPoint_AssociatedDevice Nested (
      ID UInt8,
      AccessPointReference String, -- Device.WiFi.AccessPoint.1
      MACAddress String,
      SignalStrength Int8,
      Active UInt8,
      LastDataUplinkRate UInt32,
      LastDataDownlinkRate UInt32,
      Retransmissions UInt16
  ),
  WiFi_SSIDNumberOfEntries UInt8,
  WiFi_SSID Nested (
    ID UInt8,
    BSSID String,
    LowerLayers String, -- "Device.WiFi.Radio.1"
    SSID String, -- "netis_95F0_2.4GHz@unifi"
    Status String,
    BytesSent UInt64, -- Stats.BytesSent
    BytesReceived UInt64,
    DiscardPacketsReceived UInt32,
    DiscardPacketsSent UInt32,
    ErrorsReceived UInt32,
    ErrorsSent UInt32,
    PacketsReceived UInt64,
    PacketsSent UInt64
  ),
  WiFi_RadioNumberOfEntries UInt8,
  WiFi_Radio Nested (
    ID UInt8,
    AutoChannelEnable UInt8,
    Channel UInt8,
    CurrentOperatingChannelBandwidth String,
    Status String,
    MaxBitRate UInt32,
    OperatingFrequencyBand String
  )
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(EventDate)
ORDER BY (EventDate, SerialNumber )
SAMPLE BY SerialNumber;
```

* Insert data (eg. the mock data generated earlier)
```
INSERT into cpe.kpi FORMAT JSONEachRow {"EventDate": "2021-06-28", "EventDateTime": "2021-06-28 00:15:00", "HardwareVersion": "RTL960x", "Manufacturer": "Realtek", "MemoryStatus_Free": 37758, "MemoryStatus_Total": 64000, "ModelName": "DL4480V1_2019", "SerialNumber": "VDLINNNE1808009701", "SoftwareVersion": "DL4480V1_2.0.9e", "UpTime": 95382956, "WiFi_AccessPoint": {"AssociatedDeviceNumberOfEntries": [0, 10], "ID": [1, 2], "SSIDReference": ["Device.WiFi.SSID.1", "Device.WiFi.SSID.2"], "Security_ModeEnabled": ["WPA2-Personal", "WEP-128"], "Status": ["Up", "Up"]}, "WiFi_AccessPointNumberOfEntries": 2, "WiFi_AccessPoint_AssociatedDevice": {"AccessPointReference": ["Device.WiFi.AccessPoint.2", "Device.WiFi.AccessPoint.2", "Device.WiFi.AccessPoint.2", "Device.WiFi.AccessPoint.2", "Device.WiFi.AccessPoint.2", "Device.WiFi.AccessPoint.2", "Device.WiFi.AccessPoint.2", "Device.WiFi.AccessPoint.2", "Device.WiFi.AccessPoint.2", "Device.WiFi.AccessPoint.2"], "Active": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], "ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "LastDataDownlinkRate": [200081, 238174, 123201, 295062, 120677, 145592, 201559, 209667, 239328, 300601], "LastDataUplinkRate": [236904, 172565, 218069, 236499, 229662, 184656, 232248, 258566, 149424, 252836], "MACAddress": ["3c:22:fb:13:6f:a9", "3c:22:fb:6a:ef:75", "3c:22:fb:06:16:1f", "3c:22:fb:95:5f:e7", "3c:22:fb:a7:57:37", "3c:22:fb:b3:25:e5", "3c:22:fb:a0:15:09", "3c:22:fb:28:23:0b", "3c:22:fb:06:23:00", "3c:22:fb:5c:35:ec"], "Retransmissions": [1, 0, 1, 0, 0, 2, 2, 2, 0, 0], "SignalStrength": [-26, -34, -31, -30, -21, -30, -30, -21, -33, -30]}, "WiFi_Radio": {"AutoChannelEnable": [1, 0], "Channel": [1, 149], "CurrentOperatingChannelBandwidth": ["20MHz", "20MHz"], "ID": [1, 2], "MaxBitRate": [987, 967], "OperatingFrequencyBand": ["2.4GHz", "5GHz"], "Status": ["Up", "Up"]}, "WiFi_RadioNumberOfEntries": 2, "WiFi_SSID": {"BSSID": ["3c:22:fb:20:a7:31", "3c:22:fb:e7:41:de"], "BytesReceived": [723500, 767541], "BytesSent": [809271, 623992], "DiscardPacketsReceived": [0, 0], "DiscardPacketsSent": [0, 0], "ErrorsReceived": [2, 3], "ErrorsSent": [2, 3], "ID": [1, 2], "LowerLayers": ["Device.WiFi.Radio.1", "Device.WiFi.Radio.2"], "PacketsReceived": [1078, 1008], "PacketsSent": [1095, 1005], "SSID": ["4G3WZ6ZGSN", "ZKJVQJFQ9K"], "Status": ["Up", "Up"]}, "WiFi_SSIDNumberOfEntries": 2};
```

* View data inserted
```
select * from cpe.kpi;
```

# Shut Down
```
docker-compose down
```
