from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib import messages

import json
import requests


def add_object_count(data):
    if isinstance(data, (dict, list)):
        object_count = len(data)
        if isinstance(data, dict):
            data["object_count"] = object_count
        for item in data.values() if isinstance(data, dict) else data:
            add_object_count(item)
            
                     
def sort_keys_values(data):
    if isinstance(data, dict):
        new_data = {}
        for key, value in sorted(data.items(), key=lambda x: str(x[0])):
            if isinstance(value, dict) or isinstance(value, list):
                new_value = sort_keys_values(value)
            elif isinstance(value, str):
                new_value = ''.join(sorted(value, reverse=True))
            else:
                new_value = value
            new_key = ''.join(sorted(str(key), reverse=True))
            new_data[new_key] = new_value
        return new_data
    elif isinstance(data, list):
        return [sort_keys_values(item) for item in data]
    else:
        return data
               
      
def jsonresp(request):
    try:
        if request.method == "POST":
            input_url = request.POST.get('query_data')
            response = requests.get(input_url)
            response.raise_for_status()
            json_data = response.json()
            json_data_d = json.dumps(json_data, indent=2) 
        
            sorted_keys = sort_keys_values(json_data)
            add_object_count(sorted_keys)
        
            data = json.dumps(sorted_keys, indent=2)
            context = {'data': data,
                       'json_data_d': json_data_d,
                       }
            return render(request, 'App/json-resp.html', context=context)
    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching JSON data: {e}"
        return render(request, 'App/json-resp.html', {'error_message': error_message})
    
    return render(request, 'App/json-resp.html', {})


