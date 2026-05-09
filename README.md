# Python Network Scanner

A lightweight ARP-based network scanner written in Python using Scapy.

This tool scans the local network, discovers active devices, identifies open ports, and displays device information such as IP address and MAC address.

---

# Features

- ARP network scanning
- Detect active devices on LAN
- Display IP and MAC addresses
- Ping verification
- Multi-port scanning
- Colored terminal output
- Virtual environment support
- Logging support
- Export-ready structure

---

# Technologies Used

- Python 3
- Scapy
- Colorama
- Socket Programming

---

# Requirements

- Linux/macOS
- Python 3
- Root privileges (required for ARP scanning)

---

# Installation

## 1. Clone or Download Project

```bash
git clone <repository-url>

cd network-scanner
```

---

## 2. Create Virtual Environment

```bash
python3 -m venv venv
```

---

## 3. Activate Virtual Environment

```bash
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
run ./setup.sh
```

---

# Running the Scanner

Run using:

```bash
sudo venv/bin/python scanner.py
```

---

# Example Output

```text
Your IP Address: 192.168.1.5

Scanning network: 192.168.1.0/24

--------------------------------------------------------------------------------
IP ADDRESS       MAC ADDRESS         STATUS      OPEN PORTS
--------------------------------------------------------------------------------

192.168.1.1      aa:bb:cc:dd:ee:ff  ONLINE      80(HTTP), 443(HTTPS)
192.168.1.10     11:22:33:44:55:66  ONLINE      22(SSH)
```

---

# Project Structure

```text
network-scanner/
│
├── scanner.py
├── README.md
├── venv/
└── network_scanner.log
```

---

# How It Works

The scanner uses ARP broadcast packets to discover devices on the local network.

Flow:

1. Detect local IP
2. Calculate subnet range
3. Send ARP broadcast requests
4. Receive ARP responses
5. Scan common ports
6. Display discovered devices

---

# Common Ports Scanned

| Port | Service |
|------|----------|
| 22   | SSH      |
| 80   | HTTP     |
| 443  | HTTPS    |

---

# Dependencies

| Package | Purpose |
|----------|---------|
| scapy | Packet crafting and ARP scanning |
| colorama | Colored terminal output |
| mac-vendor-lookup | MAC vendor detection |

---

# Troubleshooting

## ModuleNotFoundError

Activate the virtual environment first:

```bash
source venv/bin/activate
```

Then run:

```bash
sudo venv/bin/python scanner.py
```

---

## Permission Errors

Run with sudo:

```bash
sudo venv/bin/python scanner.py
```

---

## Externally Managed Environment Error

Use a virtual environment instead of system-wide pip installation.

---

# Security Notice

Use this tool only on:

- networks you own
- lab environments
- authorized systems

Unauthorized scanning may violate network policies or laws.

---

# Future Improvements

- Hostname detection
- Vendor lookup
- CSV/JSON export
- Threading
- Continuous monitoring
- Web dashboard
- Vulnerability scanning

---

# Learning Concepts

This project demonstrates:

- ARP protocol
- Layer 2 networking
- Socket programming
- Port scanning
- Network discovery
- Python automation
- SRE troubleshooting basics

---

# License

MIT License