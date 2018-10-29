#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os 

# tools to extract metrics
def getHostname():
    return os.popen("cat /etc/hostname").readline().strip()

def getHostip():
    return os.popen("ifconfig | grep inet | awk '/broadcast/ {print $2}'").readline().strip()

def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return float(res.replace("temp=","").replace("'C\n",""))

def getRAMinfo():
    p = os.popen('free')
    p.readline()
    return(p.readline().split()[1:])

def getCPUuse():
    return float(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip())
def getCPUload():
    return float(os.popen("top -n1 | head -1 | awk -F 'load average' '{print $2}' | awk '{print $2}'").readline().replace(",","").strip())
def getCPUfreq():
    return float(os.popen("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq").readline().strip()) / 1000.0
def getCPUcount():
    return int(os.popen("nproc").readline().strip())

def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])

def parseXB2GB(space):
    if (space.endswith("T")): return float(space[:-1]) * 1024.0
    if (space.endswith("G")): return float(space[:-1])
    if (space.endswith("M")): return float(space[:-1]) / 1024.0
    if (space.endswith("K")): return float(space[:-1]) / 1024.0 / 1024.0
    return 0.0
        
def getMetricsJson():
    cpufreq = getCPUfreq() # do this first to prevent that other tasks cause overclocking
    RAM_stats = getRAMinfo()
    DISK_stats = getDiskSpace()
    ram_total = float(RAM_stats[0])
    ram_used = float(RAM_stats[1])
    ram_available = float(RAM_stats[5])
    return json.dumps({
        "host_name": getHostname(),
        "host_ip": getHostip(),
        "cpu_freq_mhz": cpufreq,
        "cpu_temp_celsius" : getCPUtemperature(),
        "cpu_load": getCPUload(),
        "cpu_usage_percent": getCPUuse(),
        "cpu_count": getCPUcount(),
        "ram_total_gb": round(ram_total / 1048576.0, 3),
        "ram_used_gb": round(ram_used / 1048576.0, 3),
        "ram_free_gb": round(float(RAM_stats[2]) / 1048576.0, 3),
        "ram_shared_gb": round(float(RAM_stats[3]) / 1048576.0, 3),
        "ram_cache_gb": round(float(RAM_stats[4]) / 1048576.0, 3),
        "ram_available_gb": round(ram_available / 1048576.0, 3),
        "ram_percent": int(100.0 * (ram_total - ram_available) / ram_total),
        "disk_total_gb": parseXB2GB(DISK_stats[0]),
        "disk_used_gb": parseXB2GB(DISK_stats[1]),
        "disk_free_gb": parseXB2GB(DISK_stats[2]),
        "disk_percent": int(DISK_stats[3].replace("%",""))
    }, sort_keys=True, indent=2)
        
# the http server
class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
    def do_HEAD(self):
        self._set_headers()
        
    def do_GET(self):
        self._set_headers()
        self.wfile.write(getMetricsJson().encode())
                
def run(port = 5055):
    httpd = HTTPServer(("", port), Server)
    print("Starting httpd on port %d..." % port)
    httpd.serve_forever()

print("metrics   : " + getMetricsJson())

run()
