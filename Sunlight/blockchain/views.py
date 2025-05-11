from django.shortcuts import render
from django.http import JsonResponse
from .utils import get_contract, get_web3
from accounts.models import UserProfile, Wallet
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from decouple import config

# Create your views here.

@login_required
def get_available_sellers(request):
    contract = get_contract()
    sellers = []
    try:
        # Assuming AvailableSellers is a public array
        i = 0
        while True:
            seller = contract.functions.AvailableSellers(i).call()
            sellers.append(seller)
            i += 1
    except Exception:
        pass  # End of array
    return JsonResponse({'sellers': sellers})

@login_required
def get_my_buying_history(request):
    contract = get_contract()
    selected_wallet = request.session.get('selected_wallet')
    if not selected_wallet:
        return JsonResponse({'buying_history': [], 'error': 'No wallet selected.'})
    try:
        history = contract.functions.myBuyingHistory().call({'from': selected_wallet})
    except Exception as e:
        history = []
    return JsonResponse({'buying_history': history})

@login_required
def get_my_selling_history(request):
    contract = get_contract()
    selected_wallet = request.session.get('selected_wallet')
    if not selected_wallet:
        return JsonResponse({'selling_history': [], 'error': 'No wallet selected.'})
    try:
        history = contract.functions.mySellingHistory().call({'from': selected_wallet})
    except Exception as e:
        history = []
    return JsonResponse({'selling_history': history})

@csrf_exempt
@require_POST
@login_required
def register_buyer_onchain(request):
    contract = get_contract()
    selected_wallet = request.session.get('selected_wallet')
    private_key = config('BLOCKCHAIN_PRIVATE_KEY')
    account = selected_wallet
    if not account:
        return JsonResponse({'status': 'error', 'message': 'No wallet selected.'})
    try:
        nonce = get_web3().eth.get_transaction_count(account)
        txn = contract.functions.registerBuyer().build_transaction({
            'from': account,
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': get_web3().to_wei('10', 'gwei'),
        })
        signed_txn = get_web3().eth.account.sign_transaction(txn, private_key=private_key)
        tx_hash = get_web3().eth.send_raw_transaction(signed_txn.rawTransaction)
        return JsonResponse({'status': 'success', 'tx_hash': tx_hash.hex()})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
@require_POST
@login_required
def register_seller_onchain(request):
    contract = get_contract()
    selected_wallet = request.session.get('selected_wallet')
    private_key = config('BLOCKCHAIN_PRIVATE_KEY')
    account = selected_wallet
    if not account:
        return JsonResponse({'status': 'error', 'message': 'No wallet selected.'})
    try:
        totalenergyAvaialble = int(request.POST.get('totalenergyAvaialble'))
        pricePerUnit = int(request.POST.get('pricePerUnit'))
        nonce = get_web3().eth.get_transaction_count(account)
        txn = contract.functions.registerSeller(totalenergyAvaialble, pricePerUnit).build_transaction({
            'from': account,
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': get_web3().to_wei('10', 'gwei'),
        })
        signed_txn = get_web3().eth.account.sign_transaction(txn, private_key=private_key)
        tx_hash = get_web3().eth.send_raw_transaction(signed_txn.rawTransaction)
        return JsonResponse({'status': 'success', 'tx_hash': tx_hash.hex()})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
@require_POST
@login_required
def buy_energy(request):
    contract = get_contract()
    selected_wallet = request.session.get('selected_wallet')
    private_key = config('BLOCKCHAIN_PRIVATE_KEY')
    account = selected_wallet
    if not account:
        return JsonResponse({'status': 'error', 'message': 'No wallet selected.'})
    try:
        seller_address = request.POST.get('sellerAddress')
        energy_amount = int(request.POST.get('energyAmount'))
        price_per_unit = contract.functions.sellerpage(seller_address).call()[2]
        total_cost = price_per_unit * energy_amount
        nonce = get_web3().eth.get_transaction_count(account)
        txn = contract.functions.buyEnergy(seller_address, energy_amount).build_transaction({
            'from': account,
            'nonce': nonce,
            'value': total_cost,
            'gas': 300000,
            'gasPrice': get_web3().to_wei('10', 'gwei'),
        })
        signed_txn = get_web3().eth.account.sign_transaction(txn, private_key=private_key)
        tx_hash = get_web3().eth.send_raw_transaction(signed_txn.rawTransaction)
        return JsonResponse({'status': 'success', 'tx_hash': tx_hash.hex()})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
@require_POST
@login_required
def update_price(request):
    contract = get_contract()
    selected_wallet = request.session.get('selected_wallet')
    private_key = config('BLOCKCHAIN_PRIVATE_KEY')
    account = selected_wallet
    if not account:
        return JsonResponse({'status': 'error', 'message': 'No wallet selected.'})
    try:
        new_price = int(request.POST.get('newPrice'))
        nonce = get_web3().eth.get_transaction_count(account)
        txn = contract.functions.UpdatePriceperUnit(new_price).build_transaction({
            'from': account,
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': get_web3().to_wei('10', 'gwei'),
        })
        signed_txn = get_web3().eth.account.sign_transaction(txn, private_key=private_key)
        tx_hash = get_web3().eth.send_raw_transaction(signed_txn.rawTransaction)
        return JsonResponse({'status': 'success', 'tx_hash': tx_hash.hex()})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
@require_POST
@login_required
def update_energy(request):
    contract = get_contract()
    selected_wallet = request.session.get('selected_wallet')
    private_key = config('BLOCKCHAIN_PRIVATE_KEY')
    account = selected_wallet
    if not account:
        return JsonResponse({'status': 'error', 'message': 'No wallet selected.'})
    try:
        new_energy = int(request.POST.get('newEnergy'))
        nonce = get_web3().eth.get_transaction_count(account)
        txn = contract.functions.UpdateTotalEnergyAvailablility(new_energy).build_transaction({
            'from': account,
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': get_web3().to_wei('10', 'gwei'),
        })
        signed_txn = get_web3().eth.account.sign_transaction(txn, private_key=private_key)
        tx_hash = get_web3().eth.send_raw_transaction(signed_txn.rawTransaction)
        return JsonResponse({'status': 'success', 'tx_hash': tx_hash.hex()})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
