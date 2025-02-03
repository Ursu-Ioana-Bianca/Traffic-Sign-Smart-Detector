def load_ontology():
    global categories, signs_name, signs_properties
    categories = {
        "Warning Signs": [
            {
                "name": "Yield",
                "image": "http://example.com/yield.png",
                "description": "Yield to oncoming traffic",
                "shape": "Triangle",
                "background": "White",
                "contour": "Red",
                "associatedSigns": [
                    {
                        "name": "Stop",
                        "image": "http://example.com/stop.png"
                    }
                ]
            }
        ]
    }

    signs_name = ["Yield", "Stop", "Speed Limit"]
    signs_properties = {
        "Yield": [{"image": "http://example.com/yield.png", "description": "Yield to oncoming traffic",
                   "category": "Warning"}],
        "Stop": [
            {"image": "http://example.com/stop.png", "description": "Stop your vehicle", "category": "Regulatory"}],
    }
