stylesheet = [
    # Group selector
    {
        "selector": "edge",
        "style": {"curve-style": "bezier"},  # must define to custom relation edge
    },
    # Home node
    {
        "selector": ".home",
        "style": {"background-color": "#3498db", "content": "data(label)"},
    },
    # Device node
    {
        "selector": ".device_normal",
        "style": {"background-color": "#148f77", "content": "data(label)"},
    },
    {
        "selector": ".device_special",
        "style": {"background-color": "#f39c12", "content": "data(label)"},
    },
    # Company node
    {
        "selector": ".company",
        "style": {"background-color": "#592720", "content": "data(label)"},
    },
    # Service node
    {
        "selector": ".service_normal",
        "style": {"background-color": "#e53145", "content": "data(label)"},
    },
    # Device relation
    {
        "selector": '[id *= "relation_"]',
        "style": {
            "line-color": "black",
            "target-arrow-color": "black",
            "target-arrow-shape": "triangle",
        },
    },
]
