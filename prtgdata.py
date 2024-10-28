import requests
import re
from datetime import datetime

# List of PRTG servers with authentication details
prtg_servers = [
    {"ip": "10.10.1.116", "username": "prtgadmin", "password": "Kozmik123"},
    {"ip": "10.10.1.117", "username": "prtgadmin", "password": "Kozmik123"},
    {"ip": "10.10.1.118", "username": "prtgadmin", "password": "Kozmik123"},
    {"ip": "10.10.1.120", "username": "prtgadmin", "password": "Kozmik123"},
    {"ip": "10.10.1.122", "username": "prtgadmin", "password": "Kozmik123"},
]

def fetch_sensors_with_last_up(prtg_ip, username, password):
    url = f"https://{prtg_ip}/api/table.json"
    params = {
        "content": "sensors",
        "columns": "device,lastup",
        "filter_status": "5",
        "username": username,
        "password": password
    }
    response = requests.get(url, params=params, verify=False)
    sensors = response.json().get("sensors", [])
    return sensors

def write_combined_report(prtg_servers):
    report_filename = "Combined_PRTG_Report.txt"
    with open(report_filename, "w") as file:
        for server in prtg_servers:
            ip = server["ip"]
            username = server["username"]
            password = server["password"]
            
            print(f"Fetching data from {ip}...")
            sensors = fetch_sensors_with_last_up(ip, username, password)
            
            if sensors:
                file.write(f"--- Report for PRTG Server {ip} ---\n")
                for sensor in sensors:
                    device_name = sensor.get("device", "Unknown Device")
                    lastup = sensor.get("lastup", "Unknown Last Up Time")
                    file.write(f"{device_name} = {lastup}\n")
            else:
                file.write(f"No sensors with alarms found on {ip}.\n")
    print(f"Combined report saved to {report_filename}")

def generate_critical_sites_report(input_file_path, output_file_path):
    critical_sites = {}
    
    with open(input_file_path, 'r') as file:
        for line in file:
            if ' = ' in line:
                device, status = line.strip().split(' = ')
                
                # Use regex to extract the downtime in brackets (e.g., "[3 d 2 h 59 m ago]")
                match = re.search(r'\[(\d+ d)?\s?(\d+ h)?\s?(\d+ m)?\s?(\d+ s)?\s?ago\]', status)
                
                if match:
                    # Clean and format the extracted time
                    days = match.group(1) or ''
                    hours = match.group(2) or ''
                    minutes = match.group(3) or ''
                    seconds = match.group(4) or ''
                    
                    # Combine into a single string (without unnecessary spaces)
                    downtime = ' '.join(filter(None, [days, hours, minutes, seconds])) + ' ago'
                    
                    # Calculate total hours to filter by 15 days
                    total_hours = (int(match.group(1)[:-1]) if match.group(1) else 0) * 24 + \
                                  (int(match.group(2)[:-1]) if match.group(2) else 0) + \
                                  (int(match.group(3)[:-1]) if match.group(3) else 0) / 60 + \
                                  (int(match.group(4)[:-1]) if match.group(4) else 0) / 3600
                    
                    if total_hours <= 15 * 24:  # 15 days or less
                        critical_sites[device] = downtime

    with open(output_file_path, 'w') as file:
        file.write("Critical Sites (Down for 15 days or less):\n\n")
        for device, downtime in critical_sites.items():
            file.write(f"{device} = {downtime}\n")
    
    print(f"Critical sites report generated: {output_file_path}")

# Main Execution
if __name__ == "__main__":
    combined_report_path = "Combined_PRTG_Report.txt"
    critical_sites_report_path = "Critical_Sites_Report.txt"
    
    # Step 1: Generate the combined report
    write_combined_report(prtg_servers)
    
    # Step 2: Generate the critical sites report based on the combined report
    generate_critical_sites_report(combined_report_path, critical_sites_report_path)
    
    # Optional: Print the critical sites report
    print("\nFirst few lines of the critical sites report:")
    with open(critical_sites_report_path, 'r') as file:
        print(file.read(50000))  # Print the first 500 characters for verification
