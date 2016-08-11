import statsd
import time
import psutil
import multiprocessing
import sys

SLEEP_TIME = 10
HOST_NAME = 'null_name'

def disk():
    c = statsd.StatsClient('monitor', 8125, prefix=HOST_NAME + '.system.disk')
    while True:
        disk_usage = psutil.disk_usage('/srv/node/sdb/')
        c.gauge('root.total', disk_usage.total)
        c.gauge('root.used', disk_usage.used)
        c.gauge('root.free', disk_usage.free)
        c.gauge('root.percent', disk_usage.percent)

        disk_io_c = psutil.disk_io_counters(perdisk=False)
        c.gauge('root.read_count', disk_io_c.read_count)
        c.gauge('root.write_count', disk_io_c.write_count)
        c.gauge('root.read_bytes', disk_io_c.read_bytes)
        c.gauge('root.write_bytes', disk_io_c.write_bytes)
        c.gauge('root.read_time', disk_io_c.read_time)
        c.gauge('root.write_time', disk_io_c.write_time)
        c.gauge('root.busy_time', disk_io_c.busy_time)
            
        time.sleep(SLEEP_TIME)

def cpu_times():
    c = statsd.StatsClient('monitor', 8125, prefix=HOST_NAME + '.system.cpu')
    while True:
        cpu_times = psutil.cpu_times()
        c.gauge('system_wide.times.user', cpu_times.user)
        c.gauge('system_wide.times.nice', cpu_times.nice)
        c.gauge('system_wide.times.system', cpu_times.system)
        c.gauge('system_wide.times.idle', cpu_times.idle)
        c.gauge('system_wide.times.iowait', cpu_times.iowait)
        c.gauge('system_wide.times.irq', cpu_times.irq)
        c.gauge('system_wide.times.softirq', cpu_times.softirq)
        c.gauge('system_wide.times.steal', cpu_times.steal)
        c.gauge('system_wide.times.guest', cpu_times.guest)
        c.gauge('system_wide.times.guest_nice', cpu_times.guest_nice)
        
        time.sleep(SLEEP_TIME)

def cpu_times_percent():
    c = statsd.StatsClient('monitor', 8125, prefix=HOST_NAME + '.system.cpu')
    while True:
        value = psutil.cpu_percent(interval=1)
        c.gauge('system_wide.percent', value)

        cpu_times_percent = psutil.cpu_times_percent(interval=1)
        c.gauge('system_wide.times_percent.user', cpu_times_percent.user)
        c.gauge('system_wide.times_percent.nice', cpu_times_percent.nice)
        c.gauge('system_wide.times_percent.system', cpu_times_percent.system)
        c.gauge('system_wide.times_percent.idle', cpu_times_percent.idle)
        c.gauge('system_wide.times_percent.iowait', cpu_times_percent.iowait)
        c.gauge('system_wide.times_percent.irq', cpu_times_percent.irq)
        c.gauge('system_wide.times_percent.softirq', cpu_times_percent.softirq)
        c.gauge('system_wide.times_percent.steal', cpu_times_percent.steal)
        c.gauge('system_wide.times_percent.guest', cpu_times_percent.guest)
        c.gauge('system_wide.times_percent.guest_nice', cpu_times_percent.guest_nice)
        time.sleep(SLEEP_TIME)

def memory():
    c = statsd.StatsClient('monitor', 8125, prefix=HOST_NAME + '.system.memory')
    while True:
        swap = psutil.swap_memory()
        c.gauge('swap.total', swap.total)
        c.gauge('swap.used', swap.used)
        c.gauge('swap.free', swap.free)
        c.gauge('swap.percent', swap.percent)

        virtual = psutil.virtual_memory()
        c.gauge('virtual.total', virtual.total)
        c.gauge('virtual.available', virtual.available)
        c.gauge('virtual.used', virtual.used)
        c.gauge('virtual.free', virtual.free)
        c.gauge('virtual.percent', virtual.percent)
        c.gauge('virtual.active', virtual.active)
        c.gauge('virtual.inactive', virtual.inactive)
        c.gauge('virtual.buffers', virtual.buffers)
        c.gauge('virtual.cached', virtual.cached)

        time.sleep(SLEEP_TIME)

def network():
    c = statsd.StatsClient('monitor', 8125, prefix=HOST_NAME + '.system.network')
    while True:
        net = psutil.net_io_counters()
        c.gauge('net.bytes_recv', net.bytes_recv)
        c.gauge('net.bytes_sent', net.bytes_sent)
        c.gauge('net.packets_recv', net.packets_recv)
        c.gauge('net.packets_sent', net.packets_sent)
        c.gauge('net.errin', net.errin)
        c.gauge('net.errout', net.errout)
        c.gauge('net.dropin', net.dropin)
        c.gauge('net.dropout', net.dropout)

        time.sleep(SLEEP_TIME)

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print 'usage : statsd-agent.py <host_name>\n'
        sys.exit(1)

    HOST_NAME = sys.argv[1]
    multiprocessing.Process(target=disk).start()
    multiprocessing.Process(target=cpu_times).start()
    multiprocessing.Process(target=cpu_times_percent).start()
    multiprocessing.Process(target=memory).start()
    multiprocessing.Process(target=network).start()


