import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Callable, Iterable, List, Optional

COMMON_PORTS: List[int] = [21, 22, 25, 80, 443, 8080, 8443]


@dataclass(frozen=True)
class ScanResult:
    port: int
    is_open: bool
    service: str


def resolve_host(target: str) -> str:
    """Resolve a hostname to its IPv4 address or raise socket.gaierror."""
    return socket.gethostbyname(target)


def get_service_name(port: int) -> str:
    """Identify the standard service associated with a TCP port."""
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return "unknown"


def probe_port(target_ip: str, port: int, timeout: float = 1.0) -> ScanResult:
    """Attempt a TCP handshake on a specific port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            is_open = sock.connect_ex((target_ip, port)) == 0
    except OSError:
        is_open = False

    service = get_service_name(port) if is_open else ""
    return ScanResult(port=port, is_open=is_open, service=service)


def scan_ports(
    target_ip: str,
    ports: Iterable[int],
    workers: int = 100,
    timeout: float = 1.0,
    callback: Optional[Callable[[ScanResult], None]] = None,
) -> List[ScanResult]:
    """Scan ports concurrently using ThreadPoolExecutor."""
    results: List[ScanResult] = []

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(probe_port, target_ip, port, timeout): port
            for port in ports
        }
        for future in as_completed(futures):
            res = future.result()
            results.append(res)
            if callback:
                callback(res)

    return sorted(results, key=lambda r: r.port)