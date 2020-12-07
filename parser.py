import math

received = 0
sent  = 0 
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
                sent+=1
            
            elif event == 'r':
                delay = float(time_sec) - send_time_dict[packet_id]
                total_delay += delay
                bytes = int(packet_bytes) - int(header_bytes)
                received_bytes += bytes
                received += 1
        
        if packet_type == 'tcp' and event == 'D':
            dropped += 1



print(start_time)
print(end_time)
simulation_time = end_time - start_time
print('Sent packets ', sent)
print('Dropped packets',dropped)
print('received packets', received)
print("-------------------------------------------------------------")
print("Throughput: ", (received_bytes * 8) / simulation_time, "bits/sec")
print("Average Delay: ", (total_delay / received), "seconds")
print("Delivery ratio: ", (received / sent))
print("Drop ratio: ", (dropped / sent))