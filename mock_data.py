data = {
    "devices": {
        "0": {
            "device_name": "Gauge",
            "device_type": "Smart Meter",
            "device_unprocessed": ["Footage"],
        },
        "1": {
            "device_name": "smart meter",
            "device_type": "Security Camera",
            "device_unprocessed": ["Footage", "activity"],
            "raw_data": {
                "Footage": {
                    "action": "Average",
                    "frequency": "Daily",
                    "sensitivity": "Low",
                }
            },
        },
    },
    "services": {
        "0": {
            "cate_service": {
                "1": {
                    "Footage": {
                        "action": "View Data",
                        "category": "Low",
                        "frequency": "Daily",
                    }
                }
            },
            "service_name": "Meta",
            "service_type": "Advertising Company",
        },
        "1": {"service_name": "Meta_(1)", "service_type": "Tech Company"},
    },
}