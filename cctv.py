import requests
import pandas as pd
from datetime import datetime


sites = {
    "Halls ": {
        "Hall outdoor": "http://192.168.1.101/api/status",
        "Camera 2": "http://192.168.1.102/api/status"
    },
    "Exams blocks": {
        "Camera 3": "http://192.168.2.101/api/status",
        "Camera 4": "http://192.168.2.102/api/status"
    }
}

def get_camera_status(camera_ip):
    try:
        response = requests.get(camera_ip)
        response.raise_for_status()
        return response.json()  
    except requests.RequestException:
        return None

report_data = []

for site_name, cameras in sites.items():
    down_cameras = 0
    total_cameras = len(cameras)
    
    for camera_ip, camera_name in cameras.items():
        camera_status = get_camera_status(camera_ip)
        if camera_status and camera_status['status'] == 'down':
            down_cameras += 1
    
    status = "Complete Outage" if down_cameras == total_cameras else "Partial Outage" if down_cameras > 0 else "Fully Operational"
    
    report_data.append({
        "Site": site_name,
        "Down Cameras Count": down_cameras,
        "Total Cameras": total_cameras,
        "Status": status,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Camera Names": [camera_name for camera_name in cameras.values()]
    })

df = pd.DataFrame(report_data)
df.to_excel("camera_report_by_ip.xlsx", index=False)
print("Report saved as 'camera_report_by_ip.xlsx'")
