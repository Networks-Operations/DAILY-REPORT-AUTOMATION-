import re

# Path to the input file and output file
input_file_path = r"C:\Users\NOC\Desktop\DAILY REPORT (AUTOMATION)\voipreportdata.txt"
output_file_path = r"C:\Users\NOC\Desktop\DAILY REPORT (AUTOMATION)\Voip_final_report.txt"

def extract_zero_active_sites(file_path):
    critical_sites = []
    zero_pattern = re.compile(r"(.+?)\s*=\s*0/(\d+)")  # Matches sites with 0 active phones and captures total phones

    with open(file_path, "r") as file:
        for line in file:
            match = zero_pattern.search(line)
            if match:
                site_name = match.group(1).strip()
                total_phones = match.group(2).strip()
                critical_sites.append((site_name, total_phones))  # Stores site name and total phones in a tuple

    return critical_sites

def generate_report(critical_sites):
    report = "Critical Sites with No Active Phones:\n\n"
    for idx, (site, total) in enumerate(critical_sites, start=1):
        report += f"{idx}. {site}: 0/{total}\n"  # Adds total phones and numbering to each entry
    return report

def save_report(report, file_path):
    with open(file_path, "w") as file:
        file.write(report)
    print(f"Report saved successfully to {file_path}")

# Extract critical sites and generate report
critical_sites = extract_zero_active_sites(input_file_path)
report = generate_report(critical_sites)

# Save report to a text file
save_report(report, output_file_path)