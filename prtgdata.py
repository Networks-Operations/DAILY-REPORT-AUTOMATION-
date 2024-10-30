import requests
import re
from datetime import datetime

# List of PRTG servers with authentication details and group names
prtg_servers = [
    {"ip": "your_server_ip", "username": "your_username", "password": "your_password", "group_name": "your_group_name"},
    {"ip": "your_server_ip", "username": "your_username", "password": "your_password", "group_name": "your_group_name"},
    {"ip": "your_server_ip", "username": "your_username", "password": "your_password", "group_name": "your_group_name"},
    {"ip": "your_server_ip", "username": "your_username", "password": "your_password", "group_name": "your_group_name"},
    {"ip": "your_server_ip", "username": "your_username", "password": "your_password", "group_name": "your_group_name"},
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
            group_name = server["group_name"]
            
            print(f"Fetching data from {ip}...")
            sensors = fetch_sensors_with_last_up(ip, username, password)
            
            if sensors:
                file.write(f"--- {group_name} ({ip}) ---\n")
                for sensor in sensors:
                    device_name = sensor.get("device", "Unknown Device")
                    lastup = sensor.get("lastup", "Unknown Last Up Time")
                    file.write(f"{device_name} = {lastup}\n")
            else:
                file.write(f"No sensors with alarms found on {ip} ({group_name}).\n")
            file.write("\n")  # Add a blank line between groups
    print(f"Combined report saved to {report_filename}")

def generate_critical_sites_report(input_file_path, output_file_path):
    critical_sites = {}
    current_group = None
    
    with open(input_file_path, 'r') as file:
        for line in file:
            if line.startswith("---"):
                current_group = line.strip("- \n")
                critical_sites[current_group] = {}
            elif ' = ' in line and current_group:
                device, status = line.strip().split(' = ')
                
                match = re.search(r'\[(\d+ d)?\s?(\d+ h)?\s?(\d+ m)?\s?(\d+ s)?\s?ago\]', status)
                
                if match:
                    days = int(match.group(1)[:-2]) if match.group(1) else 0
                    hours = int(match.group(2)[:-2]) if match.group(2) else 0
                    minutes = int(match.group(3)[:-2]) if match.group(3) else 0
                    seconds = int(match.group(4)[:-2]) if match.group(4) else 0
                    
                    total_hours = days * 24 + hours + minutes / 60 + seconds / 3600
                    
                    if total_hours <= 15 * 24:  # 15 days or less
                        downtime = ' '.join(filter(None, [match.group(1), match.group(2), match.group(3), match.group(4)])) + ' ago'
                        critical_sites[current_group][device] = downtime

    with open(output_file_path, 'w') as file:
        now = datetime.now()
        file.write(f"Critical Sites and Downtimes as at {now.strftime('%I:%M%p')} on {now.strftime('%A %d %B %Y')}\n\n")
        
        for group, devices in critical_sites.items():
            if devices:
                file.write(f"*{group}*\n")
                for device, downtime in devices.items():
                    file.write(f"{device} = {downtime}\n")
                file.write("\n")
    
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
        print(file.read(5000))  # Print the first 5000 characters for verification