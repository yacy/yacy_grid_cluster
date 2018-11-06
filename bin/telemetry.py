#!/usr/bin/python3

# packages needed:
# sudo apt-get install python3-pip net-tools sysstat
# sudo pip3 install flask flask-cors psutil

# to run this as systemd service, copy the file telemetry.service
# into /lib/systemd/system/telemetry.service and do
# sudo systemctl daemon-reload
# sudo systemctl enable telemetry.service

import sys, getopt, json, os, datetime, psutil
from flask import Flask, request, jsonify, abort
from flask_cors import CORS, cross_origin

# tools to extract metrics
def getHostname():
    hostname = os.popen("cat /etc/hostname").readline().strip()
    if (hostname == ""):
        hostname = os.popen("hostname").readline().strip()
    return hostname

def getHostip():
    ip = os.popen("ifconfig | grep inet | awk '/broadcast/ {print $2}'").readline().strip()
    if ip != "":
        return ip
    ip = os.popen("ifconfig | grep inet | awk '/Bcast/ {print $2}'").readline().strip().split(':')[1]
    return ip

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
    if len(a) >= 6:
        return a
    else:
        vm = psutil.virtual_memory()
        return [vm.total / 1024, vm.used / 1024, vm.free / 1024, 0, 0, vm.available / 1024]
        # total_kb, used_kb, free_kb, shared_kb, cache_kb, available_kb        

def getCPUuse():
    #return float(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip().replace(",","."))
    #return float(os.popen("grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'").readline().strip().replace(",",".")) 
    try:
        return float(os.popen("mpstat | grep -A 5 \"%idle\" | tail -n 1 | awk -F \" \" '{print 100 -  $ 12}'a").readline().strip().replace(",","."))
    except Exception as e:
        return float(os.popen("ps -A -o %cpu | awk '{s+=$1} END {print s}'").readline().strip().replace(",","."))

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
            return psutil.cpu_freq().current

def getCPUcount():
    try:
        return int(os.popen("nproc").readline().strip())
    except Exception as e:
        return int(os.popen("sysctl -n hw.ncpu").readline().strip())

def getDiskSpace():
    return os.popen("df -h / | tail -1").readline().strip().split()[1:5]

def parseXB2GB(space):
    if (space.endswith("T")): return float(space[:-1].replace(",",".")) * 1024.0
    if (space.endswith("Ti")): return float(space[:-2].replace(",",".")) * 1024.0
    if (space.endswith("G")): return float(space[:-1].replace(",","."))
    if (space.endswith("Gi")): return float(space[:-2].replace(",","."))
    if (space.endswith("M")): return float(space[:-1].replace(",",".")) / 1024.0
    if (space.endswith("Mi")): return float(space[:-2].replace(",",".")) / 1024.0
    if (space.endswith("K")): return float(space[:-1].replace(",",".")) / 1024.0 / 1024.0
    if (space.endswith("Ki")): return float(space[:-2].replace(",",".")) / 1024.0 / 1024.0
    if (space.endswith("B")): return float(space[:-1].replace(",",".")) / 1024.0 / 1024.0 / 1024.0
    if (space.endswith("Bi")): return float(space[:-2].replace(",",".")) / 1024.0 / 1024.0 / 1024.0
    return 0.0
        
def getMetricsJson():
    cpufreq = getCPUfreq() # do this first to prevent that other tasks cause overclocking
    cpuload = getCPUload()
    RAM_stats = getRAMinfo()
    DISK_stats = getDiskSpace()
    ram_total = float(RAM_stats[0])
    ram_used = float(RAM_stats[1])
    ram_available = float(RAM_stats[5])
    return {
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
        "ram_available_gb": round(ram_available / 1048576.0, 3),
        "ram_percent": int(100.0 * (ram_total - ram_available) / ram_total),
        "disk_total_gb": parseXB2GB(DISK_stats[0]),
        "disk_used_gb": parseXB2GB(DISK_stats[1]),
        "disk_free_gb": parseXB2GB(DISK_stats[2]),
        "disk_percent": int(DISK_stats[3].replace("%",""))
    }
    
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
methods = (['GET'])

@app.route('/status.json', methods=methods)
@cross_origin()
def status():
    return jsonify(getMetricsJson())

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"pPdD",[])
    except getopt.GetoptError:
        print("telemetry.py -p -P -d")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-p':
            print(json.dumps(getMetricsJson(), sort_keys=True))
        elif opt == '-P':
            print(json.dumps(getMetricsJson(), sort_keys=True, indent=2))
        elif opt == '-d':
            app.run(host="0.0.0.0", port=5055, debug=False)

if __name__ == "__main__":
    main(sys.argv[1:])
