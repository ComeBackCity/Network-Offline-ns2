import math
import os
import matplotlib.pyplot as plt

file = 'out.txt'

throughput_dict = dict()
delay_dict = dict()
delivery_ratio_dict = dict()
drop_ratio_dict = dict()

# node flow graph
sizes = (250, 500, 750, 1000, 1250)

# area flow graph
nodes = (20, 40, 60, 80, 100)

# area node graph
flows = (10, 20, 30, 40, 50)

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
    delay = float('inf') if received == 0 else (total_delay / received)
    delivery_ratio = float ('inf') if sent == 0 else received / sent
    drop_ratio = float('inf') if sent == 0 else dropped / sent
    return (throughput, delay, delivery_ratio, drop_ratio)


# node_flow graph
y1.clear()
y2.clear()
y3.clear()
y4.clear()
x = list(sizes)
xi = list(range(len(x)))

for size in sizes:
    command = 'ns offline.tcl ' + str(size) + ' ' + str(40) + ' ' + str(20)
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
plt.plot(x, y1, marker='o')
plt.xlabel('size(m)')
plt.ylabel('throughput(bits/sec)')
plt.xticks(x)
plt.title('Throughput vs area graph for node = ' + str(40) + ' flow = ' + str(20))
plt.show()

# average delay
plt.plot(x, y2, marker='o')
plt.xlabel('size(m)')
plt.ylabel('average delay(seconds)')
plt.xticks(x)
plt.title('Average delay vs area graph for node = ' + str(40) + ' flow = ' + str(20))
plt.show()

# delivery ration
plt.plot(x, y3, marker='o')
plt.xlabel('size(m)')
plt.ylabel('delivery ratio')
plt.xticks(x)
plt.title('Delivery ratio vs area graph for node = ' + str(40) + ' flow = ' + str(20))
plt.show()

# drop ratio
plt.plot(x, y4, marker='o')
plt.xlabel('size(m)')
plt.ylabel('drop ratio')
plt.xticks(x)
plt.title('Drop ratio vs area graph for node = ' + str(40) + ' flow = ' + str(20))
plt.show()

# area_flow graph
y1.clear()
y2.clear()
y3.clear()
y4.clear()
x = list(nodes)
xi = list(range(len(x)))

for n_node in nodes:
    command = 'ns offline.tcl ' + str(500) + ' ' + str(n_node) + ' ' + str(20)
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
plt.plot(x, y1, marker='o')
plt.xlabel('no of nodes')
plt.ylabel('throughput(bits/sec)')
plt.xticks(x)
plt.title('Throughput vs no of nodes graph for area = ' + str(500) + ' flow = ' + str(20))
plt.show()

# average delay
plt.plot(x, y2, marker='o')
plt.xlabel('no of nodes')
plt.ylabel('average delay(seconds)')
plt.xticks(x)
plt.title('Average delay vs no of nodes graph for area = ' + str(500) + ' flow = ' + str(20))
plt.show()

# delivery ration
plt.plot(x, y3, marker='o')
plt.xlabel('no of nodes')
plt.ylabel('delivery ratio')
plt.xticks(x)
plt.title('Delivery ratio vs no of nodes graph for area = ' + str(500) + ' flow = ' + str(20))
plt.show()

# drop ratio
plt.plot(x, y4, marker='o')
plt.xlabel('no of nodes')
plt.ylabel('drop ratio')
plt.xticks(x)
plt.title('Drop ratio vs no of nodes graph for area = ' + str(500) + ' flow = ' + str(20))
plt.show()

# node_area graph
y1.clear()
y2.clear()
y3.clear()
y4.clear()
x = list(flows)
xi = list(range(len(x)))

for flow in flows:
    command = 'ns offline.tcl ' + str(500) + ' ' + str(40) + ' ' + str(flow)
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
plt.plot(x, y1, marker='o')
plt.xlabel('flow')
plt.ylabel('throughput(bits/sec)')
plt.xticks(x)
plt.title('Throughput graph vs flow for node = ' + str(40) + ' area = ' + str(500))
plt.show()

# average delay
plt.plot(x, y2, marker='o')
plt.xlabel('flow')
plt.ylabel('average delay(seconds)')
plt.xticks(x)
plt.title('Average delay vs flow graph for node = ' + str(40) + ' area = ' + str(500))
plt.show()

# delivery ration
plt.plot(x, y3, marker='o')
plt.xlabel('flow')
plt.ylabel('delivery ratio')
plt.xticks(x)
plt.title('Delivery ratio vs flow graph for node = ' + str(40) + ' area = ' + str(500))
plt.show()

# drop ratio
plt.plot(x, y4, marker='o')
plt.xlabel('flow')
plt.ylabel('drop ratio')
plt.xticks(x)
plt.title('Drop ratio vs flow graph for node = ' + str(40) + ' area = ' + str(500))
plt.show()

f.close()
