import psutil
import smtplib
from email.mime.text import MIMEText
import requests
import json
import time
import os

# Configuration
THRESHOLDS = {
    'cpu': 80,  # CPU usage threshold in percentage
    'ram': 80,  # RAM usage threshold in percentage
    'disk': 80  # Disk usage threshold in percentage
}
CHECK_INTERVAL = 60  # Check every 60 seconds
ALERT_PERIOD = 300  # Trigger alert if threshold exceeded for 5 minutes

EMAIL_CONFIG = {
    'enabled': True,
    'smtp_server': 'smtp.example.com',
    'smtp_port': 587,
    'username': 'user@example.com',
    'password': 'password',
    'from_addr': 'alert@example.com',
    'to_addr': 'admin@example.com'
}

TEAMS_CONFIG = {
    'enabled': True,
    'webhook_url': 'https://outlook.office.com/webhook/your-webhook-url'
}

CLEANUP_CONFIG = {
    'enabled': True,
    'retention_period_days': 7,  # Retention period for cleanup
    'cleanup_path': '/path/to/logs'
}

# Monitor functions
def check_cpu():
    return psutil.cpu_percent(interval=1)

def check_ram():
    return psutil.virtual_memory().percent

def check_disk():
    return psutil.disk_usage('/').percent

# Alert functions
def send_email(subject, message):
    if not EMAIL_CONFIG['enabled']:
        return
    
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = EMAIL_CONFIG['from_addr']
    msg['To'] = EMAIL_CONFIG['to_addr']
    
    with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
        server.starttls()
        server.login(EMAIL_CONFIG['username'], EMAIL_CONFIG['password'])
        server.sendmail(EMAIL_CONFIG['from_addr'], EMAIL_CONFIG['to_addr'], msg.as_string())

def send_teams_alert(message):
    if not TEAMS_CONFIG['enabled']:
        return

    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'text': message
    }
    
    response = requests.post(TEAMS_CONFIG['webhook_url'], headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        print(f"Failed to send alert to Teams: {response.status_code}, {response.text}")

# Cleanup function
def cleanup_logs():
    if not CLEANUP_CONFIG['enabled']:
        return
    
    retention_period = CLEANUP_CONFIG['retention_period_days'] * 86400  # Convert days to seconds
    now = time.time()
    
    for filename in os.listdir(CLEANUP_CONFIG['cleanup_path']):
        file_path = os.path.join(CLEANUP_CONFIG['cleanup_path'], filename)
        if os.stat(file_path).st_mtime < now - retention_period:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted {file_path}")

# Main monitoring function
def monitor_resources():
    alert_counter = {
        'cpu': 0,
        'ram': 0,
        'disk': 0
    }

    while True:
        cpu_usage = check_cpu() if 'cpu' in THRESHOLDS else None
        ram_usage = check_ram() if 'ram' in THRESHOLDS else None
        disk_usage = check_disk() if 'disk' in THRESHOLDS else None

        if cpu_usage and cpu_usage > THRESHOLDS['cpu']:
            alert_counter['cpu'] += CHECK_INTERVAL
        else:
            alert_counter['cpu'] = 0

        if ram_usage and ram_usage > THRESHOLDS['ram']:
            alert_counter['ram'] += CHECK_INTERVAL
        else:
            alert_counter['ram'] = 0

        if disk_usage and disk_usage > THRESHOLDS['disk']:
            alert_counter['disk'] += CHECK_INTERVAL
        else:
            alert_counter['disk'] = 0

        for resource, counter in alert_counter.items():
            if counter >= ALERT_PERIOD:
                message = f"Alert: {resource.upper()} usage is above {THRESHOLDS[resource]}% for more than {ALERT_PERIOD // 60} minutes."
                send_email(f"{resource.upper()} Usage Alert", message)
                send_teams_alert(message)
                alert_counter[resource] = 0  # Reset the counter after sending the alert

        cleanup_logs()  # Perform cleanup
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_resources()
