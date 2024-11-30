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
    # Node selected
    {
        "selector": "node:selected",
        "style": {
                    'width': 36, 
                    'height': 36,
                    'border-width': '3px',
                    'border-color': '#10ff00',  # Red border when selected
                    'border-style': 'solid', 
                    "content": "data(label)"
                },
    },
    {
        "selector": "node",
        "style": {
                    'transition-property': 'transform',  # Enable smooth transition
                    'transition-duration': '0.2s',  # Duration for the transition
                },
    },
    # Edge selected
    {
        'selector': 'edge',
        'style': {
            'width': 2,
        }
    },
    {
        'selector': 'edge:selected',
        'style': {
            'width': 4,
            'line-color': '#FF4136',
            'target-arrow-color': '#FF4136',
            'source-arrow-color': '#FF4136',
            'dash-array': '5, 5'
        }
    },
    # Edge selected does not filter
    # {
    #     'selector': 'edge .not_select',
    #     'style': {
    #         'width': 4,
    #         'line-color': '#D0D0D0',
    #         'target-arrow-color': '#D0D0D0',
    #         'source-arrow-color': '#D0D0D0',
    #         'dash-array': '5, 5'
    #     }
    # },
    #node does not filter
    {
        'selector': 'node.not_select',
        'style': {
            "background-color": "#D0D0D0", 
            "content": "data(label)",
            'color': '#D0D0D0',
        }
    },
    {
        'selector': 'edge.not_select',
        'style': {
            'line-color': '#D0D0D0',
            'target-arrow-color': '#D0D0D0',
            'source-arrow-color': '#D0D0D0',
        }
    },
]
