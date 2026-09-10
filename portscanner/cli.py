import argparse
import socket
import sys
from typing import List, Set

from portscanner.scanner import COMMON_PORTS, ScanResult, resolve_host, scan_ports

# ANSI escape codes for terminal styling
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
CYAN = "\033[96m"


def parse_ports(ports_input: str) -> List[int]:
    """Parse comma-separated values and port ranges (e.g., '80,443,8000-8080')."""
    ports: Set[int] = set()

    for item in ports_input.split(","):
        item = item.strip()
        if not item:
            continue

        if "-" in item:
            start_str, end_str = item.split("-", 1)
            start, end = int(start_str), int(end_str)
            if start > end or start < 1 or end > 65535:
                raise ValueError(f"Invalid range: '{item}'")
            ports.update(range(start, end + 1))
        elif item.isdigit():
            port_num = int(item)
            if not (1 <= port_num <= 65535):
                raise ValueError(f"Port out of range (1-65535): {port_num}")
            ports.add(port_num)
        else:
            raise ValueError(f"Invalid port specification: '{item}'")

    return sorted(list(ports))


def on_port_scanned(result: ScanResult) -> None:
    """Real-time console output callback for open ports."""
    if result.is_open:
        print(f" {GREEN}[+] Port {result.port:<5} OPEN  ({result.service}){RESET}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="PortScanner CLI - Fast multithreaded TCP port scanner."
    )
    parser.add_argument(
        "-t",
        "--target",
        default="127.0.0.1",
        help="Target IP address or hostname (default: 127.0.0.1)",
    )
    parser.add_argument(
        "-p",
        "--ports",
        help="Ports to scan (e.g., '80,443' or '20-100'). Defaults to common ports.",
    )
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        default=100,
        help="Maximum concurrent worker threads (default: 100)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="Socket connection timeout in seconds (default: 1.0)",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        target_ip = resolve_host(args.target)
    except socket.gaierror:
        print(f"{RED}[!] Error: Could not resolve hostname '{args.target}'.{RESET}")
        sys.exit(1)

    try:
        ports = parse_ports(args.ports) if args.ports else COMMON_PORTS
    except ValueError as err:
        print(f"{RED}[!] Port configuration error: {err}{RESET}")
        sys.exit(1)

    print(f"{CYAN}==================================================")
    print(" PortScanner CLI")
    print(f"=================================================={RESET}")
    print(f"Target:      {args.target} ({target_ip})")
    print(f"Ports:       {len(ports)} port(s) queued")
    print(f"Workers:     {args.workers}")
    print(f"Timeout:     {args.timeout}s")
    print(f"{CYAN}--------------------------------------------------{RESET}\n")

    try:
        results = scan_ports(
            target_ip=target_ip,
            ports=ports,
            workers=args.workers,
            timeout=args.timeout,
            callback=on_port_scanned,
        )
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Scan aborted by user.{RESET}")
        sys.exit(0)

    open_ports_count = sum(1 for r in results if r.is_open)
    print(f"\n{CYAN}--------------------------------------------------{RESET}")
    print(f"Scan complete. {open_ports_count} open port(s) identified.")


if __name__ == "__main__":
    main()