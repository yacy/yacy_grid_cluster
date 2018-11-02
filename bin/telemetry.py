#!/usr/bin/python3

# packages needed:
# pip3 install python-daemon

import sys, getopt, json, os, datetime#, daemon
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qsl


# tools to extract metrics
def getHostname():
    return os.popen("cat /etc/hostname").readline().strip()

def getHostip():
    return os.popen("ifconfig | grep inet | awk '/broadcast/ {print $2}'").readline().strip()
    
def getCPUtemperature():
    try:
        res = os.popen('[ `which vcgencmd` ] && vcgencmd measure_temp').readline()
        return float(res.replace("temp=","").replace("'C\n",""))
    except Exception as e:
        return 0.0

def getRAMinfo():
    p = os.popen('free')
    p.readline()
    a = p.readline().split()[1:]
    # free is not available on mac
    return a if len(a) >= 6 else [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

def getCPUuse():
    #return float(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip().replace(",","."))
    #return float(os.popen("grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'").readline().strip().replace(",",".")) 
    try:
        return float(os.popen("mpstat | grep -A 5 \"%idle\" | tail -n 1 | awk -F \" \" '{print 100 -  $ 12}'a").readline().strip().replace(",","."))
    except Exception as e:
        return float(os.popen("ps -A -o %cpu | awk '{s+=$1} END {print s}'").readline().strip())

def getCPUload():
    #return float(os.popen("top -n1 | head -1 | awk -F 'load average' '{print $2}' | awk '{print $2}'").readline().replace(",","").strip())
    return os.popen("uptime | awk -F 'load average' '{print $2}' | awk '{print $2,$3,$4}'").readline().strip().split()

def getCPUfreq():
    try:
        cpufreq = float(os.popen("[ -f /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq ] && cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq").readline().strip()) / 1000.0
        return cpufreq
    except Exception as e:
        try:
            return float(os.popen("lscpu | grep MHz | awk '{print $3}'").readline().strip())
        except Exception as e:
            return 0.0

def getCPUcount():
    try:
        return int(os.popen("nproc").readline().strip())
    except Exception as e:
        return int(os.popen("sysctl -n hw.ncpu").readline().strip())

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
        
def getMetricsJson(pretty):
    cpufreq = getCPUfreq() # do this first to prevent that other tasks cause overclocking
    cpuload = getCPUload()
    RAM_stats = getRAMinfo()
    DISK_stats = getDiskSpace()
    ram_total = float(RAM_stats[0])
    ram_used = float(RAM_stats[1])
    ram_available = float(RAM_stats[5])
    j = {
        "timestamp":datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"), # we are using the "date_hour_minute_second" or "strict_date_hour_minute_second" format of elasticsearch as fornat for the date: yyyy-MM-dd'T'HH:mm:ss.
        "host_name": getHostname(),
        "host_ip": getHostip(),
        "cpu_freq_mhz": cpufreq,
        "cpu_temp_celsius" : getCPUtemperature(),
        "cpu_load_1": float(cpuload[0].replace(",","")),
        "cpu_load_5": float(cpuload[1].replace(",","")),
        "cpu_load_15": float(cpuload[2].replace(",","")),
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
    }
    if pretty:
        return json.dumps(j, sort_keys=True, indent=2)
    else:
        return json.dumps(j, sort_keys=True)
        
# the http server
class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        pr = urlparse(self.path)
        path = pr.path
        query = dict(parse_qsl(pr.query))
        pretty = "pretty" in query
        if path.endswith("/status.json"):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(getMetricsJson(pretty).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run(port = 5055):
    httpd = HTTPServer(("", port), Server)
    #print("Starting httpd on port %d..." % port)
    httpd.serve_forever()

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"pPdD",[])
    except getopt.GetoptError:
        print("telemetry.py -p -P -d")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-p':
            print(getMetricsJson(False))
        elif opt == '-P':
            print(getMetricsJson(True))
        elif opt == '-d':
            run()
#        elif opt == '-D':
#            with daemon.DaemonContext():
#                run()

if __name__ == "__main__":
    main(sys.argv[1:])
