#!/usr/bin/python3

import json
import zipfile
import os.path
import collections
import operator
import jsonlines
from pprint import pprint
from tabulate import tabulate

def main():
    #opendata is uncompressed too large for github,so it is just uncompressed locally
    extracted_name = "opendata-2022-01-17-072501+0100.jsonl"
    if not os.path.exists(extracted_name):
        with zipfile.ZipFile("opendata-latest.zip", 'r') as zip_ref:
            zip_ref.extractall(".")
    print("Select CPU or GPU:")
    print("1. CPU")
    print("2. GPU")
    input_txt = input("Enter your choice: ")
    if input_txt == "1":
        renderdev = "CPU"
    elif input_txt == "2":
        renderdev = "GPU"

    print("   ")
    print("How many?")
    print("1. Top 10")
    print("2. Top 50")
    print("3. Top 100")
    print("4. Top 250")
    print("5. Top 500")
    input_txt = input("Enter your choice: ")
    if input_txt == "1":
        maxcount=10
    elif input_txt == "2":
        maxcount = 50
    elif input_txt == "3":
        maxcount = 100
    elif input_txt == "4":
        maxcount = 250
    elif input_txt == "5":
        maxcount = 500
    with jsonlines.open(extracted_name) as reader:
    #data = json.load(json_file)
        totallist=[]
        list_pre=[]
        sublist=[]
        error_count=0


        if renderdev == "CPU":
            # CPU
            for element in reader:
                #print(json.dumps(element["data"], indent=4, sort_keys=True))
                #print(json.dumps(element, indent=4, sort_keys=True))
                # print(element["data"][0]["scene"]["label"])
                try:
                    if element["data"][0]["scene"]["label"] == "pavillon_barcelona":
                        if element["data"][0]["device_info"]["device_type"] == "CPU":
                            # adding it to the list
                            sublist.append(element["data"][0]["device_info"]["compute_devices"][0]["name"])
                            sublist.append(element["data"][0]["device_info"]["device_type"])
                            sublist.append(element["data"][0]["stats"]["total_render_time"])
                            list_pre.append(sublist)
                            sublist = []

                except KeyError:
                    error_count += 1



        elif renderdev == "GPU":
            #GPU
            for element in reader:

                try:
                    if element["data"][0]["scene"]["label"] == "pavillon_barcelona":
                        if element["data"][0]["device_info"]["device_type"] == "CUDA" or element["data"][0]["device_info"]["device_type"] == "OPTIX" or element["data"][0]["device_info"]["device_type"] == "OPENCL" :
                            #adding it to the list
                            sublist.append(element["data"][0]["device_info"]["compute_devices"][0]["name"])
                            sublist.append(element["data"][0]["device_info"]["device_type"])
                            sublist.append(element["data"][0]["stats"]["total_render_time"])
                            list_pre.append(sublist)
                            sublist=[]

                except KeyError:
                    error_count += 1

    print(error_count)

    list_pre.sort()
    #form = json.dumps(list, indent=2)
    #print(form)

    #find double entries and calculate average of runtimes
    c = collections.defaultdict(list)

    for elm1,elm2,elm3 in list_pre:
        c[elm1].append(elm3)

    result = [(elm1,sum(v)//len(v)) for elm1,v in c.items()]

    result_sorted = sorted(result, key=operator.itemgetter(1), reverse=False)

    i=1
    list_ranked = []
    for element in result_sorted:
        list_ranked.append([i,element])
        #print(str(i), element)
        i=i+1
        if i > maxcount:
            break
    pprint(list_ranked)
    print("-------------------------------------------")
    print(" ")
    print("Please select baseline device for comparison of speed")
    input_txt = input("Enter comparison point (line number):")

    base_line = list_ranked[int(input_txt)-1]

    base_line_time = base_line[1][1]
    list_formated=[]
    for element in list_ranked:
        list_formated.append([element[0],element[1][0],int(element[1][1]),round(base_line_time/element[1][1], 2)])
    print (tabulate(list_formated, headers=["Rank", "Device", "Runtime in Seconds", "Times faster than baseline"]))

if __name__ == '__main__':
     main()

