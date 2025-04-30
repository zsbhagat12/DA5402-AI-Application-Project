from flask import Flask, Response
import psutil
import time

app = Flask(__name__)

@app.route("/metrics")
def metrics():
    lines = []
    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent()
    disk = psutil.disk_io_counters()
    net = psutil.net_io_counters()
    files = psutil.num_fds() if hasattr(psutil, "num_fds") else 0

    lines.append(f'system_memory_utilization {mem.percent}')
    lines.append(f'system_cpu_utilization {cpu}')
    lines.append(f'system_disk_read_bytes {disk.read_bytes}')
    lines.append(f'system_disk_write_bytes {disk.write_bytes}')
    lines.append(f'system_net_sent_bytes {net.bytes_sent}')
    lines.append(f'system_net_recv_bytes {net.bytes_recv}')
    lines.append(f'system_open_file_handles {files}')
    return Response("\n".join(lines), mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=18000)
