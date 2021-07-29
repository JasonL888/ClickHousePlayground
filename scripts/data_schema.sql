
-- clickhouse-client --multiline
--CREATE DATABASE IF NOT EXISTS cpe;

--SET input_format_import_nested_json=1;
--SET flatten_nested = 1;
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
