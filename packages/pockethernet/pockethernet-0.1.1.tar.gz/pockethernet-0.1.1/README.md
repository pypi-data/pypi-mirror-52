# Pockethernet Protocol reverse-engineering

Because I want a desktop app

## Contents

* Panasonic PAN1026 Bluetooth 4.0/BLE module
* 3.3V <-> 5V UART level shifter
* STM32F207 main MCU
* TI TLC59116 i2c controlled led driver
* Marvell 88E1111 Gigabit ethernet transceiver
* TPS65217x PMIC/Battery controller

## Protocol

You need the latest firmware (I'm using v29) so the device uses BLE GATT instead of BT4 RFCOMM. 

It provides the Generic Access service (0x1800) and a vendor specific service 59710d3d-d96a-4666-ac17-e7f61ba52480 and
the characteristic 6c741b59-f88f-4a3f-a5c4-2223d2958378