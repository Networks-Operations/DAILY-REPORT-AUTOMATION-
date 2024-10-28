# **PRTG Critical Sites Monitoring**

This Python project, created for the UITS-NOID division of KNUST by Kingsley Obo Danquah, a national service personnel, automates the monitoring of PRTG (Paessler Router Traffic Grapher) servers to identify critical sites that have been down for a specified period (15 days or less). The tool fetches sensor data from multiple PRTG servers, compiles it into a report, and filters out critical devices with downtime within the threshold. This project also includes VoIP monitoring to assist in the reporting process.

## **Table of Contents**
- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [How It Works](#how-it-works)
- [Usage](#usage)
- [Configuration](#configuration)
- [Sample Output](#sample-output)
- [Contributing](#contributing)
- [License](#license)

---

## **Project Overview**

This project provides an automated solution for monitoring PRTG servers and identifying critical devices that have been offline for 15 days or less. It creates two reports:
1. **Combined Report**: Lists all devices with downtime, including VoIP devices.
2. **Critical Sites Report**: Filters devices with downtime within the threshold.

## **Prerequisites**

- **Python 3.6+**
- **`requests` library**: Install with `pip install requests`
- **Access to PRTG Servers**: Each PRTG server should support API access with correct credentials.

## **Setup and Installation**

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/prtg-critical-sites-monitoring.git
    cd prtg-critical-sites-monitoring
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure PRTG Servers**:
    - Open the script and update the `prtg_servers` list with your PRTG server IPs, usernames, and passwords.

## **How It Works**

1. **Data Retrieval**: Connects to each PRTG server, retrieves sensors with downtime, and writes the results to `Combined_PRTG_Report.txt`, including VoIP devices.
2. **Critical Sites Filtering**: Parses the combined report to filter only the devices that have been down for 15 days or less, writing these to `Critical_Sites_Report.txt`.

## **Usage**

Run the script by executing:
```bash
python prtg_monitoring_script.py
```

The script will:
1. Fetch data from all specified PRTG servers.
2. Write a combined report to `Combined_PRTG_Report.txt`.
3. Write a filtered critical sites report to `Critical_Sites_Report.txt`.

## **Configuration**

In the script:
- **PRTG Servers**: Update `prtg_servers` list with the IP, username, and password for each server.
- **Downtime Threshold**: Modify the threshold (default is 15 days) in the `generate_critical_sites_report()` function.

Example:
```python
prtg_servers = [
    {"ip": "10.10.1.116", "username": "prtgadmin", "password": "your_password"},
    # Add other servers as needed
]
```

## **Sample Output**

### Combined Report (`Combined_PRTG_Report.txt`)
```
--- Report for PRTG Server 10.10.1.116 ---
Device: Africa-Hall_Switch1_PortersLodge, Last Up: 3 d 2 h 59 m ago
Device: VoIP_Device_1, Last Up: 1 d 5 h 30 m ago
Device: Africa-Hall_Switch2_BlockA, Last Up: 14 d 15 h 5 m ago
```

### Critical Sites Report (`Critical_Sites_Report.txt`)
```
Critical Sites (Down for 15 days or less):

Africa-Hall_Switch1_PortersLodge = 3 d 2 h 59 m ago
VoIP_Device_1 = 1 d 5 h 30 m ago
Africa-Hall_Switch2_BlockA = 14 d 15 h 5 m ago
```

## **Contributing**

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit and push your changes.
4. Submit a pull request.

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to customize any sections further!
