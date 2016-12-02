#! venv python

import requests
import urllib
import json


dataset_URI1_string='http://ogi.eu/#IrishNatoinalTideGaugeNetwork_ds'

def encode (URI):
    URI_encoded = urllib.quote_plus(URI)
    #   print URI_encoded
    return URI_encoded

encode (dataset_URI1_string)

#   requeststat= ['http://localhost:8080/dimensions?dataset='+ encode (dataset_URI1), 'http://localhost:8080/measures?dataset='+ encode (dataset_URI1), 'http://localhost:8080/attributes?dataset='+ encode (dataset_URI1)];


localserver_string='http://localhost:8000'
vmogiserver_string='http://vmogi01.deri.ie:8000'

request_for_dim_names_str=localserver_string+'/dimensions?dataset='+ encode (dataset_URI1_string)
print request_for_dim_names_str
response_dim_json = requests.get(request_for_dim_names_str)
data_dim_json = response_dim_json.json()
print data_dim_json

request_for_measure_names_str=localserver_string+'/measures?dataset='+ encode (dataset_URI1_string)
print request_for_measure_names_str
response_measure_json = requests.get(request_for_measure_names_str)
data_measure_json = response_measure_json.json()
print data_measure_json


# [{"hight":"55","wave":"5454"},{}]
visulization_list = []
visulization_dict = {}

print visulization_dict
print visulization_list



#   createing dim/meaures names/values dictionry
#   {"hight":["","","",""],"wave":["","","",""]}
""" creating values lists, and appeding it to the intermediate dictionary in tow steps on for dim and one for measures"""
intermediate_names_values_dict = {}
intermediate_values_list = []

print intermediate_names_values_dict
print intermediate_values_list


for dim_name in data_dim_json:
    #  clear intermediate_names_values_list
    intermediate_values_list = []
    dim_name_cleaned_str=dim_name['URI'].replace('http://ogi.eu/#','')
    intermediate_names_values_dict[dim_name_cleaned_str] = []
    request_for_values_str = localserver_string + '/dimension-values?dataset=' + encode(dataset_URI1_string) + '&dimension=' + encode(
        dim_name['URI'])
    print request_for_values_str
    response_dim_values_json = requests.get(request_for_values_str)
    #time.sleep(20)
    dim_values_json = response_dim_values_json.json()
    #print dim_values_json
#print intermediate_names_values_dict
    for dim_value in dim_values_json:
        dim_value_str=dim_value['URI']
        intermediate_values_list.append(dim_value_str)

    #print intermediate_values_list
    # append intermediate_names_values_list to the dictionary
    intermediate_names_values_dict[dim_name_cleaned_str] = intermediate_values_list
    #print intermediate_names_values_dict



for measure_name in data_measure_json:
    #  clear intermediate_names_values_list
    intermediate_values_list = []
    measure_name_cleaned_str = measure_name['URI'].replace('http://ogi.eu/#', '')
    intermediate_names_values_dict[measure_name_cleaned_str] = []

    request_for_values_str = localserver_string + '/dimension-values?dataset=' + encode(
        dataset_URI1_string) + '&dimension=' + encode(
        measure_name['URI'])
    print request_for_values_str
    response_measure_values_json = requests.get(request_for_values_str)

    measure_values_json = response_measure_values_json.json()
    #print measure_values_json
    for measure_value in measure_values_json:
        measure_value_str=measure_value['URI']
        intermediate_values_list.append(measure_value_str)
        #print measure_value_str
    #  append intermediate_names_values_list to the dictionary
    intermediate_names_values_dict[measure_name_cleaned_str] = intermediate_values_list

"""
x=json.dumps(intermediate_names_values_dict, ensure_ascii=False)

with open("jsFULL.json", "w") as text_file:
    text_file.write(x)


import csv
w = csv.writer(open("output.csv", "w"))
for key, val in intermediate_names_values_dict.items():
    w.writerow([key, val])

"""
""""creating visulization response as LIST OF DIC """
#for x in range (0,values_array_size):
limit=6
for x in range(0, limit+1):

    for dim_name in data_dim_json:
        dim_name_cleaned_str = dim_name['URI'].replace('http://ogi.eu/#', '')
        visulization_dict[dim_name_cleaned_str]=intermediate_names_values_dict[dim_name_cleaned_str][x]

    for measure_name in data_measure_json:
        measure_name_cleaned_str = measure_name['URI'].replace('http://ogi.eu/#', '')
        visulization_dict[measure_name_cleaned_str] = intermediate_names_values_dict[measure_name_cleaned_str][x]

    visulization_list.append(visulization_dict)




print len(visulization_list)
print visulization_list
PivotTabeljson = json.dumps(visulization_list)
print PivotTabeljson
