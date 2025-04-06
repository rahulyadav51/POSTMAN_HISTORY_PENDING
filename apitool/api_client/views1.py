from django.shortcuts import render
# import requests
# import time
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse

# @csrf_exempt
# def api_client(request):
#     response_data = {
#         'status_code': None,
#         'response': None,
#         'time_elapsed': None,
#         'error': None
#     }
    
#     if request.method == 'POST':
#         try:
#             url = request.POST.get('url')
#             method = request.POST.get('method', 'GET')
#             headers = {}
#             body = {}
            
#             # Process headers
#             headers_raw = request.POST.get('headers', '')
#             if headers_raw:
#                 for line in headers_raw.split('\n'):
#                     if ':' in line:
#                         key, value = line.split(':', 1)
#                         headers[key.strip()] = value.strip()
            
#             # Process body based on content type
#             content_type = request.POST.get('content_type', 'json')
#             body_raw = request.POST.get('body', '')
            
#             if content_type == 'json' and body_raw:
#                 body = body_raw
            
#             # Make the request
#             start_time = time.time()
            
#             if method == 'GET':
                # response = requests.get(url, headers=headers)
#             elif method == 'POST':
#                 response = requests.post(url, headers=headers, data=body)
#             elif method == 'PUT':
#                 response = requests.put(url, headers=headers, data=body)
#             elif method == 'DELETE':
#                 response = requests.delete(url, headers=headers)
#             elif method == 'PATCH':
#                 response = requests.patch(url, headers=headers, data=body)
#             else:
#                 response = requests.get(url, headers=headers)
            
#             time_elapsed = time.time() - start_time
            
#             response_data = {
#                 'status_code': response.status_code,
#                 'response': response.text,
#                 'time_elapsed': round(time_elapsed, 2),
#                 'error': None
#             }
            
#         except Exception as e:
#             response_data['error'] = str(e)
    
#     return render(request, 'api_client/client.html', response_data)
import requests
import time
import logging
# from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# logger = logging.getLogger(__name__)

# @csrf_exempt
# def api_client(request):
#     logger.debug(f"Request method: {request.method}")
#     logger.debug(f"POST data: {request.POST}")
#     logger.debug(f"Headers: {request.headers}")
#     response_data = {
#         'status_code': None,
#         'response': None,
#         'time_elapsed': None,
#         'error': None
#     }

#     if request.method == 'POST':
#         try:
#             logger.debug("Processing POST request")
#             url = request.POST.get('url')
#             method = request.POST.get('http-method', 'GET').upper()
#             headers = {}
            
#             # Process headers: each line should be in the form "Key: Value"
#             headers_raw = request.POST.get('headers', '')
#             if headers_raw:
#                 for line in headers_raw.split('\n'):
#                     if ':' in line:
#                         key, value = line.split(':', 1)
#                         headers[key.strip()] = value.strip()
            
#             # Determine body option based on radio button selection
#             body_option = request.POST.get('body-type', 'none')
#             body = None
            
#             if body_option == 'raw':
#                 # For Raw, process the raw text body along with a content type
#                 content_type = request.POST.get('content_type', 'json')
#                 body_raw = request.POST.get('body-raw', '')
#                 body = body_raw  # You could parse JSON if needed
#             elif body_option == 'formdata':
#                 # For Form Data, collect keys and values into a dictionary
#                 keys = request.POST.getlist('formdata-key[]')
#                 values = request.POST.getlist('formdata-value[]')
#                 body = {}
#                 for key, value in zip(keys, values):
#                     if key.strip():
#                         body[key.strip()] = value.strip()
#             elif body_option == 'urlencoded':
#                 # For x-www-form-urlencoded, collect keys and values into a dictionary
#                 keys = request.POST.getlist('urlencoded-key[]')
#                 values = request.POST.getlist('urlencoded-value[]')
#                 body = {}
#                 for key, value in zip(keys, values):
#                     if key.strip():
#                         body[key.strip()] = value.strip()
#             else:
#                 body = None  # 'none' is selected
            
#             # Time the API call
#             start_time = time.time()
#             if method == 'GET':
#                 resp = requests.get(url, headers=headers)
#             elif method == 'POST':
#                 resp = requests.post(url, headers=headers, data=body)
#             elif method == 'PUT':
#                 resp = requests.put(url, headers=headers, data=body)
#             elif method == 'DELETE':
#                 resp = requests.delete(url, headers=headers)
#             elif method == 'PATCH':
#                 resp = requests.patch(url, headers=headers, data=body)
#             else:
#                 resp = requests.get(url, headers=headers)
#             time_elapsed = time.time() - start_time
            
#             response_data = {
#                 'status_code': resp.status_code,
#                 'response': resp.text,
#                 'time_elapsed': round(time_elapsed, 2),
#                 'error': None
#             }
            
#         except Exception as e:
#             response_data['error'] = str(e)
    
#     return render(request, 'api_client/client.html', response_data)
import json


# def send_api_request(request):
#     if request.method == 'POST':
#         # Get form data (URL, method, headers, body, etc.)
#         url = request.POST.get('url')
#         method = request.POST.get('method', 'GET')
#         headers = {}  # Parse from frontend
#         body_type = request.POST.get('body_type')
#         data = {}  # or raw_json_body

#         # Example: x-www-form-urlencoded handling
#         if body_type == 'x-www-form-urlencoded':
#             for key in request.POST:
#                 if key.startswith('form_data_key_'):
#                     index = key.split('_')[-1]
#                     data_key = request.POST.get(f'form_data_key_{index}')
#                     data_value = request.POST.get(f'form_data_value_{index}')
#                     if data_key:
#                         data[data_key] = data_value

#         try:
#             if body_type == 'raw':
#                 response = requests.request(method, url, headers=headers, data=request.POST.get('raw_body'))
#             elif body_type == 'x-www-form-urlencoded':
#                 response = requests.request(method, url, headers=headers, data=data)
#             else:
#                 response = requests.request(method, url, headers=headers)

#             # Try parsing JSON
#             try:
#                 response_body = response.json()
#                 response_body = json.dumps(response_body, indent=4)
#             except Exception:
#                 response_body = response.text

#             return render(request, 'api_client/client.html', {
#                 'response_body': response_body,
#                 'status_code': response.status_code
#             })

#         except Exception as e:
#             return render(request, 'api_client/client.html', {
#                 'response_body': f"Error: {str(e)}",
#                 'status_code': 'Request Failed'
#             })

#     return render(request, 'api_client/client.html')
