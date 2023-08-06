import argparse
import logging
from pockethernet import Pockethernet, WiremapResult, PoEResult, LinkResult


def print_wiremap(wiremap):
    print(wiremap.connections)
    print(wiremap.shorts)
    if not isinstance(wiremap, WiremapResult):
        return

    if sum(wiremap.connections) == 0 and sum(wiremap.shorts) == 0:
        print("All connections open (no cable inserted, no wiremap adapter connected or full break)")
        return

    if sum(wiremap.connections) == 0 and wiremap.shorts == [0, 3, 6, 0, 7, 8, 0, 0, 0]:
        print("Wiremap adapter inserted wrong way around")
        return

    if sum(wiremap.connections) == 0 and wiremap.shorts == [0, 2, 0, 1, 1, 1, 1, 1, 1]:
        print("Cable inserted into ethernet port")
        return

    if sum(wiremap.shorts) > 0:
        print("Cable shorted")
        return

    if wiremap.connections == [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        print("Straight cable")
        return

    if wiremap.connections == [0, 8, 7, 6, 5, 4, 3, 2, 1]:
        print("Rollover cable (for serial console")
        return

    print("Unknown or wrong cable")


def print_poe(poe):
    if not isinstance(poe, PoEResult):
        return

    print("Pair voltages:")
    for v in poe.pair_volts:
        print("- {}V".format(v))
    print("PoE A: {}V".format(poe.poe_a_volt))
    print("PoE B: {}V".format(poe.poe_b_volt))


def print_link(link):
    if not isinstance(link, LinkResult):
        return

    if not link.up:
        print("No link established")
        return

    duplexity = "half duplex"
    if link.duplex:
        duplexity = "full duplex"
    print("Got {} {} link".format(link.speed, duplexity))

    print("Link partner advertises:")
    print("            HD  FD")
    print("  10 MBIT   {:d}   {:d}".format(link.link_partner_10HD, link.link_partner_10FD))
    print(" 100 MBIT   {:d}   {:d}".format(link.link_partner_100HD, link.link_partner_100FD))
    print("1000 MBIT   {:d}   {:d}".format(link.link_partner_1000HD, link.link_partner_1000FD))


def main():
    parser = argparse.ArgumentParser(description='Pockethernet shell client')
    parser.add_argument('mac', help='Bluetooth MAC of the Pockethernet')
    parser.add_argument('--debug', help='Enable debug output', action='store_true')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    client = Pockethernet()
    client.connect(args.mac)
    wiremap = client.get_wiremap()

    print_wiremap(wiremap)
    print_poe(client.get_poe())
    print_link(client.get_link())


if __name__ == '__main__':
    main()
