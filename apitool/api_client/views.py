

# import json
# import time
# import requests
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def api_client(request):
#     context = {
#         'status_code': None,
#         'response_body': None,
#         'time_elapsed': None,
#         'error': None
#     }

#     if request.method == 'POST':
#         try:
#             url = request.POST.get('url')
#             method = request.POST.get('http_method', 'GET').upper()
#             headers_raw = request.POST.get('headers', '')
#             body_type = request.POST.get('body_type', 'none')

#             # Parse headers
#             headers = {}
#             for line in headers_raw.split('\n'):
#                 if ':' in line:
#                     key, value = line.split(':', 1)
#                     headers[key.strip()] = value.strip()

#             # Prepare request body
#             data = None
#             if body_type == 'raw':
#                 data = request.POST.get('raw_body', '')
#             elif body_type == 'formdata':
#                 data = {}
#                 keys = request.POST.getlist('formdata-key[]')
#                 values = request.POST.getlist('formdata-value[]')
#                 for k, v in zip(keys, values):
#                     if k.strip():
#                         data[k.strip()] = v.strip()
#             elif body_type == 'x-www-form-urlencoded':
#                 data = {}
#                 keys = request.POST.getlist('urlencoded-key[]')
#                 values = request.POST.getlist('urlencoded-value[]')
#                 for k, v in zip(keys, values):
#                     if k.strip():
#                         data[k.strip()] = v.strip()

#             # Make request
#             start_time = time.time()
#             response = requests.request(method, url, headers=headers, data=data)
#             elapsed = round(time.time() - start_time, 2)

#             # Parse response
#             try:
#                 body = response.json()
#                 body = json.dumps(body, indent=4)
#             except Exception:
#                 body = response.text

#             context.update({
#                 'status_code': response.status_code,
#                 'response_body': body,
#                 'time_elapsed': elapsed
#             })

#         except Exception as e:
#             context['error'] = str(e)

#     return render(request, 'api_client/client.html', context)


import time
import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import APIRequestHistory

@csrf_exempt
def api_client(request):
    context = {
        'status_code': None,
        'response_body': None,
        'time_elapsed': None,
        'error': None,
        'history': APIRequestHistory.objects.order_by('-timestamp')[:10]
    }

    if request.method == 'POST':
        try:
            url = request.POST.get('url')
            method = request.POST.get('http_method', 'GET').upper()
            headers_raw = request.POST.get('headers', '')
            body_type = request.POST.get('body_type', 'none')

            headers = {}
            for line in headers_raw.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip()] = value.strip()

            data = None
            formdata = {}
            urlencoded = {}
            raw_body = request.POST.get('raw_body', '')

            if body_type == 'formdata':
                keys = request.POST.getlist('formdata-key[]')
                values = request.POST.getlist('formdata-value[]')
                formdata = dict(zip(keys, values))
                data = formdata

            elif body_type == 'x-www-form-urlencoded':
                keys = request.POST.getlist('urlencoded-key[]')
                values = request.POST.getlist('urlencoded-value[]')
                urlencoded = dict(zip(keys, values))
                data = urlencoded

            elif body_type == 'raw':
                data = raw_body

            APIRequestHistory.objects.create(
                url=url,
                method=method,
                headers=headers_raw,
                body_type=body_type,
                raw_body=raw_body if body_type == 'raw' else '',
                formdata=formdata if body_type == 'formdata' else {},
                urlencoded=urlencoded if body_type == 'x-www-form-urlencoded' else {}
            )

            start_time = time.time()
            response = requests.request(method, url, headers=headers, data=data)
            elapsed = round(time.time() - start_time, 2)

            try:
                body = response.json()
                body = json.dumps(body, indent=4)
            except Exception:
                body = response.text

            context.update({
                'status_code': response.status_code,
                'response_body': body,
                'time_elapsed': elapsed,
            })

        except Exception as e:
            context['error'] = str(e)

    return render(request, 'api_client/client.html', context)

def get_history_detail(request, history_id):
    try:
        history = APIRequestHistory.objects.get(id=history_id)
        return JsonResponse({
            'url': history.url,
            'method': history.method,
            'headers': history.headers,
            'body_type': history.body_type,
            'raw_body': history.raw_body,
            'formdata': history.formdata,
            'urlencoded': history.urlencoded,
        })
    except APIRequestHistory.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
