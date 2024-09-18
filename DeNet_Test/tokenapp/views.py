# tokenapp/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from .utils import get_balance, get_balances, get_token_info, get_transaction_history, get_top_addresses, \
    get_top_addresses_with_transactions


@csrf_exempt
@require_GET
def get_balance_view(request):
    address = request.GET.get('address')
    if not address:
        return JsonResponse({'error': 'Address is required'}, status=400)

    try:
        balance = get_balance(address)
        return JsonResponse({'balance': balance})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_POST
def get_balance_batch_view(request):
    addresses = request.POST.getlist('addresses[]')
    if not addresses:
        return JsonResponse({'error': 'Addresses are required'}, status=400)

    try:
        balances = get_balances(addresses)
        return JsonResponse({'balances': balances})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_GET
def get_token_info_view(request):
    try:
        token_info = get_token_info()
        return JsonResponse(token_info)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_GET
def get_transaction_history_view(request):
    address = request.GET.get('address')
    limit = int(request.GET.get('limit', 10))
    if not address:
        return JsonResponse({'error': 'Address is required'}, status=400)

    try:
        transactions = get_transaction_history(address, limit)
        return JsonResponse({'transactions': transactions})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_GET
def get_top_addresses_view(request):
    limit = int(request.GET.get('limit', 10))
    try:
        top_addresses = get_top_addresses(limit)
        return JsonResponse({'top_addresses': top_addresses})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_GET
def get_top_addresses_with_transactions_view(request):
    limit = int(request.GET.get('limit', 10))
    try:
        top_addresses_with_transactions = get_top_addresses_with_transactions(limit)
        return JsonResponse({'top_addresses_with_transactions': top_addresses_with_transactions})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
