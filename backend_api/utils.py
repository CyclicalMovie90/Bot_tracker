def extract_features(data):
    # Parse screen resolution
    screen_resolution = data.get("screenResolution", "0x0")
    try:
        width, height = map(int, screen_resolution.split("x"))
        total_resolution = width * height
    except ValueError:
        total_resolution = 0

    # Parse connection speed
    connection_speed = data.get("connectionSpeed", "0 Mbps")
    try:
        speed = float(connection_speed.split(" ")[0])
    except ValueError:
        speed = 0.0

    return [
        len(data.get("userAgent", "")),  # Length of User-Agent string
        total_resolution,  # Total screen resolution (width * height)
        len(data.get("os", "")),  # Length of OS string
        len(data.get("language", "")),  # Length of language string
        len(data.get("cpuGpuSpecs", "")),  # Length of CPU/GPU specs
        len(data.get("browserFingerprinting", "")),  # Length of browser fingerprint
        len(data.get("plugins", "").split(", ")),  # Number of plugins
        len(data.get("canvasFingerprint", "")),  # Length of canvas fingerprint
        len(data.get("timezone", "")),  # Length of timezone string
        len(data.get("ipAddressMasked", "")),  # Length of masked IP address
        speed,  # Connection speed in Mbps
        1 if data.get("proxyVPNDetection") == "Detected" else 0,  # Proxy/VPN detection flag
        len(data.get("mouseMovementPatterns", [])),  # Number of mouse movements
        len(data.get("clickTimings", [])),  # Number of click timings
        1 if data.get("scrollDepth") == "Full Scroll" else 0,  # Full scroll flag
        1 if data.get("touchPressure") != "Unavailable" else 0,  # Touch pressure availability
        len(data.get("pageLoadTimes", [])),  # Number of page load times
        len(data.get("dwellTimes", [])),  # Number of dwell times
        len(data.get("inactivityPatterns", [])),  # Number of inactivity patterns
        len(data.get("keystrokeDynamics", [])),  # Number of keystroke dynamics
        len(data.get("smallPointerMovements", [])),  # Number of small pointer movements
    ]