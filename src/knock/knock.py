import argparse
from os import path
import socket
import sys
import time

from . import __version__


FILE = path.basename(__file__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        epilog=f"example: {FILE} host.domain 123:tcp 456:udp 789:tcp"
    )
    parser.add_argument("host", help="the host to knock")
    parser.add_argument(
        "ports", nargs="+", help="one or more ports or port:protocol pairs"
    )
    parser.add_argument(
        "-d",
        "--delay",
        default=5,
        type=int,
        help="wait <DELAY> milliseconds between knocks [default: 5 ms]",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        default=0.5,
        type=float,
        help="time out after <TIMEOUT> seconds [default: 0.5 s]",
    )
    parser.add_argument(
        "-u",
        "--udp",
        action="store_true",
        help="use UDP unless specified [default: TCP]",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        help="show the version and exit",
        version=f"{FILE} {__version__}",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="print debugging information during execution",
    )
    # parser.add_argument(
    #     "-6", "--ipv6", action="store_true", help="use IPv6 [default: IPv4]"
    # )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    while args.ports:
        tokens = args.ports.pop(0).split(":")
        port = int(tokens[0])
        if len(tokens) > 1:
            if tokens[1].upper() not in ["TCP", "UDP"]:
                print(f"Unsupported protocol {tokens[1]}")
                return 1
            protocol = tokens[1].upper()
        elif args.udp:
            protocol = "UDP"
        else:
            protocol = "TCP"

        if args.verbose:
            print(
                f"Knocking on {args.host}:{port} using {protocol} ...",
                end="",
                flush=True,
            )

        try:
            # TODO(jeffreyc): add IPv6 support.
            if protocol == "UDP":
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(args.timeout)
            sock.connect((args.host, port))
            status = "open"
            sock.close()
        except ConnectionRefusedError:
            status = "connection refused"
        except TimeoutError:
            status = "timeout"
        except OSError as e:
            print(f" FAILED ({args.host}:{port}:{protocol}) - {e}")
            return 1

        if args.verbose:
            print(f" OK ({status})", flush=True)

        if args.ports:
            if args.verbose:
                print(
                    f"Waiting {args.delay} milliseconds between port hits", flush=True
                )
            time.sleep(args.delay * 0.001)

    if args.verbose:
        print("OPEN SESAME")
    return 0


if __name__ == "__main__":
    sys.exit(main())
