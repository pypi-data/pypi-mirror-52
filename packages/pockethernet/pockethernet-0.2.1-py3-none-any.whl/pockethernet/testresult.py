import struct


class WiremapResult:
    def __init__(self, result):
        self.connections = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.shorts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(0, 4):
            a = (i * 2) + 1
            self.connections[a] = result[i] & 15
            self.shorts[a] = result[i + 4] & 15
            b = (i * 2) + 2
            self.connections[b] = (result[i] & 240) >> 4
            self.shorts[b] = (result[i + 4] & 240) >> 4

        self.connections[0] = result[8] & 15
        self.shorts[0] = (result[8] & 240) >> 4

        # Connections to 0 are disconnected at this point in the code, transform to None instead
        # and rewrite connections to 9 (shield) to 0 (shield in output)
        for i in range(0, len(self.connections)):
            if self.connections[i] == 0:
                self.connections[i] = None
            if self.connections[i] == 9:
                self.connections[i] = 0
            if self.shorts[i] == 0:
                self.shorts[i] = None
            if self.shorts[i] == 9:
                self.shorts[i] = 0

        if self.connections[0] == 9:
            self.connections[0] = 0

        self.wiremap_id = result[9]


class PoEResult:
    def __init__(self, result):
        self.pair_volts = result[0:4]
        self.poe_a_volt = result[4]
        self.poe_b_volt = result[5]


class LinkResult:
    def __init__(self, result):
        status, lpab, gbstatus, cssr1, gbskew, gbswap = struct.unpack('<HHHHHH', result)

        self.up = (cssr1 & 8) != 0
        self.mdix = (cssr1 & 64) != 0

        speed = (cssr1 & (16384 + 32768)) >> 14
        speeds = {
            0: "10BASE-T",
            1: "100BASE-T",
            2: "1000BASE-T"
        }
        self.speed = speeds[speed]
        self.duplex = (cssr1 & 8192) != 0

        self.link_partner_10HD = (lpab & 32) != 0
        self.link_partner_10FD = (lpab & 64) != 0
        self.link_partner_100HD = (lpab & 128) != 0
        self.link_partner_100FD = (lpab & 256) != 0
        self.link_partner_1000HD = (gbstatus & 1024) != 0
        self.link_partner_1000FD = (gbstatus & 2048) != 0

        self.skew_pair1 = (gbskew & 0xf) * 8
        self.skew_pair2 = ((gbskew & 0xff) >> 4) * 8
        self.skew_pair3 = ((gbskew & 0xfff) >> 8) * 8
        self.skew_pair4 = ((gbskew & 0xffff) >> 12) * 8
