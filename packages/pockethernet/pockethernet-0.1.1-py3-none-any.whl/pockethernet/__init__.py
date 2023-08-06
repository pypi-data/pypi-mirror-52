import socket
import struct
import time
import crc16
from cobs import cobs
import logging

from pockethernet.testresult import WiremapResult, PoEResult, LinkResult

COMMAND_WIREMAP = 48
COMMAND_DEVICEINFO = 1
COMMAND_TDR = 50
COMMAND_TDR_GRAPH = 65
COMMAND_POE = 49
COMMAND_LINK = 52
RESULT_WIREMAP = 4144
RESULT_DEVICEINFO = 4097
RESULT_TDR = 4146
RESULT_TDR_GRAPH = 4161
RESULT_POE = 4145
RESULT_LINK = 4099
RESULT_LLDP = 4352

PHY_UP = 1
PHY_ISOLATE = 2
PHY_NEGOTIATE_MDI = 4
PHY_NEGOTIATE_MDIX = 8
PHY_NEGOTIATE_ANY = 4 + 8
PHY_DTE_DETECT = 16
PHY_AN_ADV = 32
PHY_ADVERTIZE_10BASET = 64
PHY_ADVERTIZE_100BASET = 128
PHY_ADVERTIZE_1000BASET = 256
PHY_ADVERTIZE_ANY = 64 + 128 + 256
PHY_DUPLEX_HALF = 512
PHY_DUPLEX_FULL = 1024
PHY_DUPLEX_ANY = 512 + 1024
PHY_SELF = 2048
PHY_DOWNSHIFT = 4096


class Pockethernet:

    def __init__(self):
        self.sock = None
        self.lastData = {}
        self.mac = None

    def connect(self, mac, max_tries=None):
        """ Connect to a pockethernet device over bluetooth.

        The pockethernet device has to be bound already using something like the bluetooth dialog in gnome

        :param mac: Bluetooth mac address of the pockethernet
        :param max_tries: Max tries to connect, each try is 1-2 seconds
        :return: True if the connection is successful
        """
        self.mac = mac
        tries = 0
        logging.debug('Connecting to {}'.format(mac))

        # Pockethernet seems to use RFCOMM channel 5
        while True:
            try:
                self.sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
                self.sock.bind((socket.BDADDR_ANY, 0))
                self.sock.connect((mac, 5))
                logging.debug('Connection to {} successful'.format(mac))
                return True
            except OSError as e:
                logging.debug(e)
                tries += 1
                if max_tries is not None and tries > max_tries:
                    logging.debug('Max tries exceeded')
                    return False
                time.sleep(1)

    def send_command(self, command, data):
        logging.debug("Sending command {} with {} bytes data".format(command, len(data)))

        # First is command ID, the 0 is reserved space for a checksum
        header = struct.pack('<HH', command, 0)
        data = struct.pack('<{}s'.format(len(data)), data)
        packet = header + data

        # Calculate the checksum and pack the header again with it
        crc = crc16.crc16xmodem(packet, -1)
        header = struct.pack('<HH', command, crc)
        packet = header + data

        # Run COBS encoding on the data and add null bytes for framing
        encoded = cobs.encode(packet)
        raw = b'\0' + encoded + b'\0'

        # Hope that the pockethernet enjoys this packet
        self.sock.send(raw)

    def read_packet(self, until=None):
        logging.debug('Reading a packet')
        while True:
            raw = self.sock.recv(200)
            packets = raw.split(b'\0')
            packets = list(filter(None, packets))
            for packet in packets:
                packet = cobs.decode(packet)
                header = struct.unpack_from('<HH', packet)
                data = struct.unpack_from('<{}s'.format(len(packet) - 4), packet, 4)
                packet_type = header[0]
                self.lastData[packet_type] = data[0]
                logging.debug('Got packet with type {} and length {}'.format(packet_type, len(data[0])))
                if packet_type == until:
                    return data[0]

    def get_device_info(self):
        self.send_command(COMMAND_DEVICEINFO, b'')
        result = self.read_packet(RESULT_DEVICEINFO)
        result = struct.unpack_from('<BBBBBB', result)
        mac = '28:FD:80:{:02X}:{:02X}:{:02X}'.format(result[2], result[1], result[0])
        return {
            'hardware': result[4],
            'firmware': result[5],
            'mac': mac
        }

    def get_wiremap(self):
        self.send_command(COMMAND_WIREMAP, b'')
        result = self.read_packet(RESULT_WIREMAP)
        return WiremapResult(result)

    def get_poe(self):
        config = struct.pack('<HH', 3000, 100)
        self.send_command(COMMAND_POE, config)
        result = self.read_packet(RESULT_POE)
        return PoEResult(result)

    def _make_marvell_link_bitfield(self, speed=PHY_ADVERTIZE_ANY, duplexity=PHY_DUPLEX_ANY,
                                    negotiate=PHY_NEGOTIATE_ANY):
        return PHY_UP + PHY_ISOLATE + PHY_AN_ADV + speed + duplexity + negotiate

    def get_link(self):
        phy = self._make_marvell_link_bitfield()
        config = struct.pack('<IH', phy, 8000)
        self.send_command(COMMAND_LINK, config)
        result = self.read_packet(RESULT_LINK)

        return LinkResult(result)

    def debug(self):
        self.read_packet()

    def get_tdr(self, calibration_mode=False):
        # Magic
        if calibration_mode:
            a = 3
            b = 0
        else:
            a = 0
            b = 21

        # More magic
        config = [1, a, 1, 0, 5, 4, b, 3, 0, 0, 0, 0, 0, 0, 0]
        config = struct.pack('<BBBBBBBBBBBBBBB', *config)

        self.send_command(COMMAND_TDR, config)
        result = self.read_packet(until=RESULT_TDR)
        print(result)
