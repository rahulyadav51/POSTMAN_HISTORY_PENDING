import requests
import time
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def api_client(request):
    response_data = {
        'status_code': None,
        'response': None,
        'time_elapsed': None,
        'error': None
    }
    
    if request.method == 'POST':
        try:
            url = request.POST.get('url')
            method = request.POST.get('method', 'GET')
            headers = {}
            body = {}
            
            # Process headers
            headers_raw = request.POST.get('headers', '')
            if headers_raw:
                for line in headers_raw.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        headers[key.strip()] = value.strip()
            
            # Process body based on content type
            content_type = request.POST.get('content_type', 'json')
            body_raw = request.POST.get('body', '')
            
            if content_type == 'json' and body_raw:
                body = body_raw
            
            # Make the request
            start_time = time.time()
            
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, headers=headers, data=body)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, data=body)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)
            elif method == 'PATCH':
                response = requests.patch(url, headers=headers, data=body)
            else:
                response = requests.get(url, headers=headers)
            
            time_elapsed = time.time() - start_time
            
            response_data = {
                'status_code': response.status_code,
                'response': response.text,
                'time_elapsed': round(time_elapsed, 2),
                'error': None
            }
            
        except Exception as e:
            response_data['error'] = str(e)
    
    return render(request, 'api_client/client.html', response_data)