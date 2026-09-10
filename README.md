# PortScanner CLI

A lightweight, concurrent TCP port scanner built with Python. Designed for rapid network diagnostics, host availability checks, and security auditing without external runtime dependencies.

---

## Architecture

The project follows a decoupled, modular design:

```text
portscanner/
├── portscanner/
│   ├── __init__.py     # Package initialization and metadata
│   ├── cli.py          # CLI argument parsing, input validation, and stdout formatting
│   └── scanner.py      # Core network logic, socket handshakes, and thread orchestration
├── tests/
│   └── test_scanner.py # Unit test suite covering input validation and range parsing
├── LICENSE
└── README.md
```

## Features

- **Concurrent Execution:** Utilizes Python's `ThreadPoolExecutor` for parallel socket probes.
- **Flexible Port Specification:** Supports individual ports, comma-separated lists, and continuous ranges (e.g., `80,443,8000-8080`).
- **Standard Service Resolution:** Translates identified open ports to their registered protocol names via standard system mappings.
- **Robust Input Handling:** Validates IPv4 targets, resolves DNS hostnames, and performs strict boundary checks on port numbers (1–65535).
- **Graceful Termination:** Intercepts `SIGINT` (`Ctrl + C`) to terminate active threads without tracebacks.

---

## 🚀 Getting Started

### Prerequisites
* Python 3.8+
* Git
  
---

## 💻 Usage
### Run the scanner directly as a module:

### Scan default common ports on localhost
python -m portscanner.cli

### Scan specific ports and ranges on a remote target
python -m portscanner.cli -t scanme.nmap.org -p 21-25,80,443 --workers 50 --timeout 1.5

---
## ⚙️ Opções de Linha de Comando (CLI)

| Flag | Long Flag | Description | Default
| :--- | :--- | :--- | :--- |
| `-h` | `--help` | Exibe a mensagem de ajuda e instruções de uso. | 
| `-t` | `--target` | Target IP address or hostname | 127.0.0.1
| `-p` | `--ports` | Ports to scan (e.g., 80,443 or 20-100) | Common ports
| `-w` | `--workers` | Concurrent worker threads | 100
| | `--timeout` | Socket connection timeout in seconds | 1.0

---

## Disclaimer
This tool is intended strictly for educational purposes and authorized network auditing. Scanning networks without explicit prior permission from the owner may violate local laws. The author assumes no liability for misuse.

---
## 📄 License
Distributed under the MIT License. See LICENSE for more information.

developed by Matheus Natal.
