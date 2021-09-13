import json
import re

#
# with open("json_file.json", "r") as json_file:
#     bus_line = json.load(json_file)
bus_line = json.loads(input())

# bugs_dict = {"bus_id": 0, "stop_id": 0, "stop_name": 0, "next_stop": 0, "stop_type": 0, "a_time": 0}
# total = 0
# template_time = r'[0-2][\d]:[0-5][\d]$'
# template_street = r'[A-Z]?\w*\s?[A-Z]\w*\s(Road|Avenue|Boulevard|Street)$'
# template_stop_type = r'^$|[FOS]{1}$'
# for element in bus_line:
#     if type(element['bus_id']) != int:
#         bugs_dict['bus_id'] += 1
#     if type(element['stop_id']) != int:
#         bugs_dict['stop_id'] += 1
#     if type(element['next_stop']) != int:
#         bugs_dict['next_stop'] += 1
#     if type(element['stop_type']) != str:
#         bugs_dict['stop_type'] += 1
#     if re.match(template_stop_type, element['stop_type']) is None:
#         bugs_dict['stop_type'] += 1
#     if type(element['stop_name']) != str:
#         bugs_dict['stop_name'] += 1
#     if re.match(template_street, element['stop_name']) is None:
#         bugs_dict['stop_name'] += 1
#     if type(element['a_time']) != str:
#         bugs_dict['a_time'] += 1
#     if re.match(template_time, element['a_time']) is None:
#         bugs_dict['a_time'] += 1
#
# for v in bugs_dict.values():
#     total += v

# print(f'''Type and required field validation: {total} errors\n'''
#       # f'''bus_id: {bugs_dict['bus_id']}\n'''
#       # f'''stop_id: {bugs_dict['stop_id']}\n'''
#       f'''stop_name: {bugs_dict['stop_name']}\n'''
#       # f'''next_stop: {bugs_dict['next_stop']}\n'''
#       f'''stop_type: {bugs_dict['stop_type']}\n'''
#       f'''a_time: {bugs_dict['a_time']}''')

# bus_line = [
#     {
#         "bus_id": 512,
#         "stop_id": 4,
#         "stop_name": "Bourbon Street",
#         "next_stop": 6,
#         "stop_type": "S",
#         "a_time": "08:13"
#     },
#     {
#         "bus_id": 512,
#         "stop_id": 6,
#         "stop_name": "Sunset Boulevard",
#         "next_stop": 0,
#         "stop_type": "F",
#         "a_time": "08:16"
#     }
# ]

dict_bus_stops = {}
list_bus_id = [element['bus_id'] for element in bus_line]
i = 0
j = 0
while i < len(list_bus_id):
    increment = list_bus_id.count(list_bus_id[i])
    dict_bus_stops[f'bus_id{[j]}'] = list_bus_id[i]
    dict_bus_stops[f'stops{[j]}'] = increment
    i += increment
    j += 1
# print("Line names and number of stops:")
# for y in range(j):
#     print('bus_id:',dict_bus_stops[f'bus_id{[y]}'], 'stops:', dict_bus_stops[f'stops{[y]}'])

# print(dict_bus_stops)

list_buses = []
start_stops = []
transfer_stops = set()
finish_stops = []
list_bus_id = [element['bus_id'] for element in bus_line]
list_stop_type = [element['stop_type'] for element in bus_line]
list_stop_name = [element['stop_name'] for element in bus_line]
all_stops = []

list_times = [element['a_time'] for element in bus_line]

for i in range(j):
    list_buses.append(dict_bus_stops[f'bus_id{[i]}'])

# count = 0
# print("Arrival time test:")
# for bus_line_id in list_buses:
#     time_list = []
#     i = 0
#     for bus_id, stop_name, time in zip(list_bus_id, list_stop_name, list_times):
#         if bus_id == bus_line_id:
#             count += 1
#             time_splitted = (time.split(":"))
#             casted_to_int = [int(y) for y in time_splitted]
#             time_to_int = casted_to_int[0] * 60 + casted_to_int[1]
#             time_list.append(time_to_int)
#             if len(time_list) >= 2:
#                 if time_list[i] < time_list[i + 1]:
#                     i += 1
#                 else:
#                     print(f'bus_id line {bus_id}: wrong time on station {stop_name}')
#                     break
#         if count == len(list_bus_id):
#             print('OK')

for bus_line_id in list_buses:
    x = []
    cnt = 0
    for bus_id, stop_type, stop_name in zip(list_bus_id, list_stop_type, list_stop_name):
        if bus_id == bus_line_id:
            x.append(stop_name)
            cnt += 1
            if cnt == 1 and stop_type != 'S':
                print(f'There is no start or end stop for the line: {bus_id}.')
                quit()
            if cnt == list_bus_id.count(bus_id) and stop_type != 'F':
                print(f'There is no start or end stop for the line: {bus_id}.')
                quit()
            elif stop_type == 'S':
                start_stops.append(stop_name)
            elif stop_type == 'F':
                finish_stops.append(stop_name)
    all_stops.append(set(x))


for i in range(len(all_stops)):
    for j in range(len(all_stops)):
        if i == j or i < j:
            continue
        else:
            intersect = all_stops[i].intersection(all_stops[j])
            if intersect:
                transfer_stops.update(intersect)
6
start_stops_set = set(start_stops)
finish_stops_set = set(finish_stops)

stops_start_finish_transfer = (list(start_stops_set)) + (list(transfer_stops)) + (list(finish_stops_set))

# print(f'Start stops: {len(list(start_stops_set))} {sorted(list(start_stops_set))}')
# print(f'Transfer stops: {len(list(transfer_stops))} {sorted(list(transfer_stops))}')
# print(f'Finish stops: {len(list(finish_stops_set))} {sorted(list(finish_stops_set))}')

wrong_stop_type_list = []

for el in bus_line:
    if el['stop_type'] == 'O':
        if el['stop_name'] in stops_start_finish_transfer:
            wrong_stop_type_list.append(el['stop_name'])

print('On demand stops test:')
if wrong_stop_type_list:
    print(f'Wrong stop type: {sorted(wrong_stop_type_list)}')
else:
    print("OK")
