data = {
    "devices": {
        "0": {
            "device_name": "Gauge",
            "device_type": "Security Camera",
            "device_unprocessed": ["Footage", "Energy usage", "Colour"],
            "raw_data": {
                "Footage": {
                    "action": "Average",
                    "frequency": "Daily",
                    "sensitivity": "Low",
                }
            },
        },
        "1": {
            "device_name": "Smart TV haha",
            "device_type": "Security Camera",
            "device_unprocessed": ["Energy usage", "Temperature", "Activity period"],
            "raw_data": {
                "Activity period": {
                    "action": "Anonymise",
                    "frequency": "Yearly",
                    "sensitivity": "High",
                },
                "Energy usage": {
                    "action": "Average",
                    "frequency": "Daily",
                    "sensitivity": "Low",
                },
                "Temperature": {
                    "action": "Anonymise",
                    "frequency": "Weekly",
                    "sensitivity": "Medium",
                },
            },
        },
        "2": {
            "device_name": "apple watch",
            "device_type": "Light",
            "device_unprocessed": ["Activity period", "Temperature", "Notification"],
            "raw_data": {
                "Activity period": {
                    "action": "Transfer",
                    "frequency": "Weekly",
                    "sensitivity": "Medium",
                },
                "Temperature": {
                    "action": "Average",
                    "frequency": "No fix time",
                    "sensitivity": "Medium",
                },
            },
        },
    },
    "services": {
        "0": {
            "cate_service": {
                "0": {
                    "Footage": {
                        "action": "View Data",
                        "category": "Low",
                        "frequency": "Daily",
                    }
                }
            },
            "service_name": "The8th",
            "service_type": "Advertising Company",
        },
        "1": {
            "cate_service": {
                "1": {
                    "Energy usage": {
                        "action": "Read Data",
                        "category": "Medium",
                        "frequency": "Weekly",
                    },
                    "Temperature": {
                        "action": "View Data",
                        "category": "High",
                        "frequency": "Weekly",
                    },
                },
                "2": {
                    "Activity period": {
                        "action": "Read Data",
                        "category": "Low",
                        "frequency": "Daily",
                    },
                    "Temperature": {
                        "action": "Send Notification",
                        "category": "Low",
                        "frequency": "Daily",
                    },
                },
            },
            "service_name": "Meta",
            "service_type": "Tech Company",
        },
    },
    "tour": 0,
}
