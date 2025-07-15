console.log("Script running at:", new Date().toISOString());
const PassiveTracker = (() => {
  const data = {
    userAgent: navigator.userAgent,
    screenResolution: `${screen.width}x${screen.height}`,
    os: navigator.platform || "Unknown",
    language: navigator.language,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    plugins: Array.from(navigator.plugins).map(p => p.name).join(", "),
    browserFingerprinting: "",
    canvasFingerprint: "",
    connectionSpeed: navigator.connection ? navigator.connection.downlink + " Mbps" : "Unknown",
    proxyVPNDetection: "Not Detected",
    mouseMovementPatterns: [],
    clickTimings: [],
    scrollDepth: "Not Tracked Yet",
    touchPressure: "Unavailable",
    pageLoadTimes: [],
    dwellTimes: [],
    inactivityPatterns: [],
    keystrokeDynamics: [],
    smallPointerMovements: [],
    ipAddressMasked: "x.x.x.x",
    cpuThreads: "Unknown",
    gpuInfo: "Unknown",
    cpuBenchmark: "Unknown"
  };

  let lastClickTime = 0;
  let dwellStart = Date.now();
  let inactivityTimer;
  let lastMouseX = null;
  let lastMouseY = null;

  const getGPUInfo = () => {
    const canvas = document.createElement("canvas");
    const gl = canvas.getContext("webgl") || canvas.getContext("experimental-webgl");
    if (!gl) return "WebGL not supported";
    const debugInfo = gl.getExtension("WEBGL_debug_renderer_info");
    if (!debugInfo) return "GPU info not available";
    return gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
  };

  const estimateCPUPerformance = () => {
    const start = performance.now();
    let total = 0;
    for (let i = 0; i < 1e7; i++) total += Math.sqrt(i);
    const end = performance.now();
    return `${(end - start).toFixed(2)} ms`;
  };

  const init = () => {
    console.log("Initializing PassiveTracker...");

    // 🧠 Add CPU/GPU Info
    data.cpuThreads = navigator.hardwareConcurrency || "Unknown";
    data.gpuInfo = getGPUInfo();
    data.cpuBenchmark = estimateCPUPerformance();

    console.log("CPU Threads:", data.cpuThreads);
    console.log("GPU Info:", data.gpuInfo);
    console.log("CPU Benchmark:", data.cpuBenchmark);

    // Mouse movement
    window.addEventListener("mousemove", e => {
      const now = Date.now();
      const dx = lastMouseX !== null ? Math.abs(e.clientX - lastMouseX) : 0;
      const dy = lastMouseY !== null ? Math.abs(e.clientY - lastMouseY) : 0;
      data.mouseMovementPatterns.push({ x: e.clientX, y: e.clientY, t: now });
      if (dx < 3 && dy < 3) data.smallPointerMovements.push({ dx, dy, t: now });
      lastMouseX = e.clientX;
      lastMouseY = e.clientY;
      resetInactivity();
    });

    // Clicks
    window.addEventListener("click", () => {
      const now = Date.now();
      if (lastClickTime !== 0) {
        data.clickTimings.push((now - lastClickTime) / 1000);
      }
      lastClickTime = now;
      resetInactivity();
    });

    // Keystrokes
    window.addEventListener("keydown", e => {
      data.keystrokeDynamics.push({ key: e.key, time: Date.now() });
      resetInactivity();
    });

    // Scroll
    window.addEventListener("scroll", () => {
      const scrollPosition = window.scrollY + window.innerHeight;
      const pageHeight = document.documentElement.scrollHeight;
      const percentScrolled = (scrollPosition / pageHeight) * 100;
      data.scrollDepth = percentScrolled >= 100 ? "Full Scroll" : percentScrolled >= 50 ? "Partial Scroll" : "Minimal Scroll";
      resetInactivity();
    });

    // Canvas Fingerprint
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    ctx.textBaseline = "top";
    ctx.font = "14px 'Arial'";
    ctx.fillText("Passive CAPTCHA Canvas", 2, 2);
    data.canvasFingerprint = canvas.toDataURL();
    data.browserFingerprinting = btoa(data.userAgent + data.plugins + data.language).slice(0, 12);

    // Page Load Times
    setTimeout(() => {
      const timing = window.performance.timing;
      const loadTime = (timing.loadEventEnd - timing.navigationStart) / 1000;
      const domLoad = (timing.domContentLoadedEventEnd - timing.domLoading) / 1000;
      data.pageLoadTimes = [loadTime, domLoad];
    }, 3000);

    // Dwell time
    window.addEventListener("beforeunload", () => {
      const now = Date.now();
      data.dwellTimes.push(((now - dwellStart) / 1000).toFixed(2));
    });

    // Send periodically
    setInterval(sendData, 10000);
  };

  const resetInactivity = () => {
    clearTimeout(inactivityTimer);
    inactivityTimer = setTimeout(() => {
      data.inactivityPatterns.push({ start: Date.now(), duration: "5s+" });
    }, 5000);
  };

  async function sendData() {
    console.log("Sending data to the backend...");
    try {
      const response = await fetch("http://127.0.0.1:8000/api/verify", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": "e5a74d0c291f4603f99de0cf607492a6"
        },
        body: JSON.stringify(data)
      });

      if (response.ok) {
        console.log("Data sent successfully:", data);
      } else {
        console.error("Failed to send data:", await response.text());
      }
    } catch (err) {
      console.error("Error sending data:", err);
    }
  }

  return { init };
})();

window.addEventListener("load", () => {
  PassiveTracker.init();
});
