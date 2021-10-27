import jsonlines
#import json 
import zipfile 
import os.path 
import collections 
import operator

def main():
    extracted_name = "opendata-2021-10-14-062531+0000.jsonl"
    
    if not os.path.exists(extracted_name):
        with zipfile.ZipFile("opendata-latest.zip", 'r') as zip_ref:
            zip_ref.extractall(".")

    with jsonlines.open(extracted_name) as reader:
    #data = json.load(json_file)
        totallist=[]
        list_pre=[]
        sublist=[]
        error_count=0
        for element in reader:
            #print(json.dumps(element["data"], indent=4, sort_keys=True))
            #print(json.dumps(element, indent=4, sort_keys=True))
            #print(element["data"][0]["scene"]["label"])
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


    c = collections.defaultdict(list)

    for elm1,elm2,elm3 in list_pre:
        c[elm1].append(elm3)

    # at this point c contains: {('a', 'b'): [1, 5], ('b', 'c'): [2]}
    #print(c)
    result = [(elm1,sum(v)//len(v)) for elm1,v in c.items()]

    result_sorted = sorted(result, key=operator.itemgetter(1), reverse=False)
    #print(result)
    i=1
    for element in result_sorted:
        print(str(i), element)
        i=i+1
        
if __name__ == '__main__':
    main()

