import math
import os
import matplotlib.pyplot as plt

file = 'out.txt'
# file1 = "throughput.txt"
# file2 = "delay.txt"
# file3 = "delivery_ratio.txt"
# file4 = "drop_ratio.txt"

throughput_dict = dict()
delay_dict = dict()
delivery_ratio_dict = dict()
drop_ratio_dict = dict()

node_flow = ((20, 10), (40, 20), (60, 30), (80, 40), (100, 50))
sizes = (250, 500, 750, 1000, 1250)
throughput = 0
delay = 0
delivery_ratio = 0
drop_ratio = 0
os.system('rm out.txt')
f = open(file, 'a')
y1 = []
y2 = []
y3 = []
y4 = []
x = list(sizes)
xi = list(range(len(x)))


def parsing():
    received = 0
    sent = 0
    dropped = 0
    total_delay = 0
    received_bytes = 0

    start_time = float('inf')
    end_time = 0
    header_bytes = 0

    file_name = 'trace.tr'
    send_time_dict = dict()

    def line_parse(line):
        return line.split()

    with open(file_name) as fileobject:
        for line in fileobject:
            strings = line.split()

            event = strings[0]
            time_sec = strings[1]
            node = strings[2]
            layer = strings[3]
            packet_id = strings[5]
            packet_type = strings[6]
            packet_bytes = strings[7]

            if start_time > float(strings[1]):
                start_time = float(strings[1])

            if end_time < float(strings[1]):
                end_time = float(strings[1])

            if layer == 'AGT' and packet_type == 'tcp':
                if event == 's':
                    send_time_dict[packet_id] = float(time_sec)
                    sent += 1

                elif event == 'r':
                    delay = float(time_sec) - send_time_dict[packet_id]
                    total_delay += delay
                    bytes = int(packet_bytes) - int(header_bytes)
                    received_bytes += bytes
                    received += 1

            if packet_type == 'tcp' and event == 'D':
                dropped += 1

    simulation_time = end_time - start_time
    throughput = (received_bytes * 8) / simulation_time
    delay = (total_delay / received)
    delivery_ratio = received / sent
    drop_ratio = dropped / sent
    return (throughput, delay, delivery_ratio, drop_ratio)


for item in node_flow:
    y1.clear()
    y2.clear()
    y3.clear()
    y4.clear()
    nodes = item[0]
    flow = item[1]

    for size in sizes:
        command = 'ns offline.tcl ' + str(size) + ' ' + str(nodes) + ' ' + str(flow)
        # print(command)
        f.write(command + '\n')
        os.system(command)
        out = parsing()
        throughput = out[0]
        delay = out[1]
        delivery_ratio = out[2]
        drop_ratio = out[3]
        y1.append(throughput)
        y2.append(delay)
        y3.append(delivery_ratio)
        y4.append(drop_ratio)
        f.write(str(throughput) + ' ' + str(delay) + ' ' + str(delivery_ratio) + ' ' + str(drop_ratio) + '\n')
        # print (throughput, delay, delivery_ratio, drop_ratio)

    # throughput
    plt.plot(x, y1)
    plt.xlabel('size(m)')
    plt.ylabel('throughput(bits/sec)')
    # plt.xticks(xi, x)
    plt.title('Throughput graph for node = ' + str(nodes) + ' flow = ' + str(flow))
    plt.show()

    # average delay
    plt.plot(x, y2)
    plt.xlabel('size(m)')
    plt.ylabel('average delay(seconds)')
    # plt.xticks(xi, x)
    plt.title('Average delay graph for node = ' + str(nodes) + ' flow = ' + str(flow))
    plt.show()

    # delivery ration
    plt.plot(x, y3)
    plt.xlabel('size(m)')
    plt.ylabel('delivery ratio')
    # plt.xticks(xi, x)
    plt.title('Delivery ratio graph for node = ' + str(nodes) + ' flow = ' + str(flow))
    plt.show()

    # drop ratio
    plt.plot(x, y4)
    plt.xlabel('size(m)')
    plt.ylabel('drop ratio')
    # plt.xticks(xi, x)
    plt.title('Drop ratio graph for node = ' + str(nodes) + ' flow = ' + str(flow))
    plt.show()

f.close()

