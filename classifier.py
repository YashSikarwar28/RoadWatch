# this is used or classifying the road type, converting road type into authority like state highwy or TN highway

def classify_road(highway_type):
    mapping = {
        "motorway": ("National Highway", "NHAI"),
        "trunk": ("National/State Highway", "TN Highways"),
        "primary": ("State Highway", "TN Highways"),
        "secondary": ("Major District Road", "TN Highways"),
        "tertiary": ("City Road", "GCC"),
        "residential": ("Local Road", "GCC"),
        "service": ("Local Road", "GCC"),
    }

    return mapping.get(highway_type, ("Unknown", "Unknown"))