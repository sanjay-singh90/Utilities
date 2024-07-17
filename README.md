# Resource Utilization Monitor with Cleanup

This script monitors CPU, RAM, and disk usage on a Linux server, sends alerts via email and MS Teams if utilization exceeds thresholds, and performs automated cleanup based on a retention period.

## Requirements

- Python 3
- psutil
- requests
- smtplib

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/sanjay-singh90/Utilities.git
    cd Utilities
    ```

2. **Install dependencies**:
    ```sh
    pip install psutil requests
    ```

## Configuration

1. **Edit the `resource_monitor_with_cleanup.py` script** to configure thresholds, email, and MS Teams settings:
    ```python
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
    ```

## Running the Script

1. **Run manually**:
    ```sh
    python3 resource_monitor_with_cleanup.py
    ```

2. **Run in the background**:
    ```sh
    nohup python3 resource_monitor_with_cleanup.py &
    ```

## Setting up as a systemd Service

1. **Create the systemd service file**:
    ```sh
    sudo nano /etc/systemd/system/resource_monitor.service
    ```

2. **Add the following content**:
    ```ini
    [Unit]
    Description=Resource Utilization Monitor with Cleanup

    [Service]
    ExecStart=/usr/bin/python3 /path/to/resource_monitor_with_cleanup.py
    Restart=always
    User=nobody
    Group=nogroup

    [Install]
    WantedBy=multi-user.target
    ```

3. **Reload systemd daemon**:
    ```sh
    sudo systemctl daemon-reload
    ```

4. **Enable and start the service**:
    ```sh
    sudo systemctl enable resource_monitor.service
    sudo systemctl start resource_monitor.service
    ```

## License

This project is licensed under the MIT License.

