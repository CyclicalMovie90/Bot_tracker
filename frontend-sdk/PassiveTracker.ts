export const PassiveTracker = () => {
  const data: any = {
    "User-Agent": navigator.userAgent,
    "Screen Resolution": `${screen.width}x${screen.height}`,
    "OS": navigator.platform,
    "Language": navigator.language,
    "Plugins": Array.from(navigator.plugins).map(p => p.name).join(", "),
    "Canvas Fingerprint": (() => {
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d")!;
      ctx.textBaseline = "top";
      ctx.font = "14px Arial";
      ctx.fillText("Fingerprint Check", 2, 2);
      return canvas.toDataURL();
    })(),
    "Timezone": Intl.DateTimeFormat().resolvedOptions().timeZone,
    "IP Address (Masked)": "x.x.x.x", // backend determines this
    "Connection Speed": (navigator as any).connection?.downlink + " Mbps" || "Unknown",
    "Proxy/VPN Detection": "Not Detected",
    "Mouse Movement Patterns": [],
    "Click Timings": [],
    "Scroll Depth": "Not Tracked Yet",
    "Touch Pressure": "Unavailable",
    "Page Load Time": performance.timing.loadEventEnd - performance.timing.navigationStart,
    "Dwell Time": 0,
    "Inactivity Patterns": [],
    "Keystroke Dynamics": [],
    "Small Pointer Movements": [],
    "Browser Fingerprinting": btoa(navigator.userAgent + navigator.language).slice(0, 12)
  };

  window.addEventListener("mousemove", e => {
    data["Mouse Movement Patterns"].push({ x: e.clientX, y: e.clientY, t: Date.now() });
  });

  setTimeout(() => {
    fetch("http://localhost:5000/api/verify", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": "e5a74d0c291f4603f99de0cf607492a6"
      },
      body: JSON.stringify(data)
    });
  }, 5000);

  return { startTracking: () => {} };
};
