import time
import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import APIRequestHistory

@csrf_exempt
def api_client(request):
    # Get recent history entries to display in the frontend
    recent_history = APIRequestHistory.objects.order_by('-timestamp')[:10]

    context = {
        'status_code': None,
        'response_body': None,
        'time_elapsed': None,
        'error': None,
        'history': recent_history  # This is OK for render() but NOT for JsonResponse!
    }

    if request.method == 'POST':
        print("Received POST request!")
        try:
            url = request.POST.get('url')
            method = request.POST.get('http_method', 'GET').upper()
            headers_raw = request.POST.get('headers', '')
            body_type = request.POST.get('body_type', 'none')
            raw_body = request.POST.get('raw_body', '')

            # Parse headers
            headers = {}
            for line in headers_raw.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip()] = value.strip()

            data = None
            formdata = {}
            urlencoded = {}

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

            # Send the actual request
            start_time = time.time()
            response = requests.request(method, url, headers=headers, data=data)
            elapsed = round(time.time() - start_time, 2)

            # Parse response body
            try:
                body = response.json()
                # body_str = json.dumps(body, indent=4)
                body_str = body
            except Exception:
                body_str = response.text

            # Save request to DB
            try:
                print("Saving API request to DB...")
                APIRequestHistory.objects.create(
                    url=url,
                    method=method,
                    headers=headers_raw,
                    body_type=body_type,
                    raw_body=raw_body if body_type == 'raw' else '',
                    formdata=formdata if body_type == 'formdata' else {},
                    urlencoded=urlencoded if body_type == 'x-www-form-urlencoded' else {},
                    response_body=body_str,
                    status_code=response.status_code,
                    time_elapsed=elapsed
                )
                print("Saved successfully!")

            except Exception as e:
                print(f"Error saving to DB: {e}")
                context['error'] = f"DB Save Error: {str(e)}"

            # Serialize updated history for JSON
            updated_history = list(
                APIRequestHistory.objects.order_by('-timestamp')[:10].values(
                    'id', 'url', 'method', 'status_code', 'timestamp'
                )
            )

            return JsonResponse({
                'status_code': response.status_code,
                'response_body': body_str,
                'time_elapsed': elapsed,
                # 'history': updated_history
            }, json_dumps_params={'indent': 4})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # GET request - render the client page
    return render(request, 'api_client/client.html', context)

def get_history_detail(request, history_id):
    return JsonResponse({'message': f'Placeholder for history ID {history_id}'})
