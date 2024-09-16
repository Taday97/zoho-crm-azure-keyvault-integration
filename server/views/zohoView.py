# views.py
import requests
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.conf import settings
from server.models import ZohoToken , Lead
from django.utils import timezone
from rest_framework.views import APIView
from django.utils.http import urlencode
from django.shortcuts import  redirect
from ..utils import encrypt_data, decrypt_data


client_id = '1000.0PQJ90V3YHV7GBSWRJID2V6DM9UXYC'
client_secret = '6329266d5dbd906011e64ef1772b2fc58b58422ccc'
token_url = 'https://accounts.zoho.com/oauth/v2/token'
redirect_uri = 'http://localhost:4000'
redirectUrl= 'http://127.0.0.1:8000/zoho/callback/'
access_type = 'offline'   
response_type = 'code'
scope = 'ZohoCRM.modules.quotes.ALL,ZohoCRM.coql.READ,ZohoSubscriptions.subscriptions.READ,ZohoSubscriptions.plans.READ,ZohoCRM.modules.ALL,ZohoCRM.settings.modules.ALL,ZohoSubscriptions.products.READ,ZohoInventory.settings.READ,ZohoInventory.items.READ'
clientUrlIndex= 'http://localhost:4000/index/'
organizationid= '20100298866'
KV_URI = 'https://accounts.zoho.eu/oauth/v2/token'



# Rest of the Zoho token authentication and management code
def zoho_auth(request):
    auth_url = f'{settings.ZOHO_AUTHORIZATION_URL}?scope={scope}&client_id={client_id}&response_type={response_type}&access_type={access_type}&redirect_uri={redirectUrl}'
    return redirect(auth_url)

def zoho_callback(request):
    code = request.GET.get('code')
    if code:
        token_data = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirectUrl,
            'code': code
        }
        response = requests.post(KV_URI, data=token_data)
        if response.status_code == 200:
            token_data = response.json()
            if 'access_token' in token_data:
                print("Token "+ token_data['access_token'])
                access_token=encrypt_data(token_data['access_token'])
                refresh_token=encrypt_data(token_data['refresh_token'])
                ZohoToken.objects.create(
                    access_token=access_token,
                    refresh_token=refresh_token,
                    scope=token_data['scope'],
                    api_domain=token_data['api_domain'],
                    token_type=token_data['token_type'],
                    expires_in=token_data['expires_in'],
                )
                return redirect(clientUrlIndex)
            else:
                return JsonResponse({'status': 'error', 'message': 'No access token'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': response.json().get('error', 'Unknown error')}, status=response.status_code)
    else:
        return JsonResponse({'status': 'error', 'message': 'No code provided'}, status=400)

def get_latest_token():
    try:
        return ZohoToken.objects.latest('created_at')
    except ZohoToken.DoesNotExist:
        return None

def refresh_access_token():
    token = get_latest_token()
    if token is None:
        return None
    refresh_token=decrypt_data(token.refresh_token)
    data = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token':refresh_token
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        token_data = response.json()
        access_token=encrypt_data(token_data['access_token'])
        token.access_token =access_token 
        token.expires_in = token_data['expires_in']
        token.save()
        return token.access_token
    else:
        raise Exception('Failed to refresh access token')

def make_zoho_request(endpoint, method='GET', data=None, organizationid=None):
    token = get_latest_token()
    if token is None:
        return redirect('zoho/auth')
    access_token=decrypt_data(token.access_token)
    headers = {
        'Authorization': f'Zoho-oauthtoken {access_token}',
        'Content-Type': 'application/json',
        'X-com-zoho-inventory-organizationid': organizationid
    }
    url = f'{token.api_domain}{endpoint}'
    if method == 'GET':
        response = requests.get(url, headers=headers, params=data)
    else:
        response = requests.post(url, headers=headers, json=data)
    if response.status_code == 401:  # Token expired
        new_access_token = refresh_access_token()
        headers['Authorization'] = f'Zoho-oauthtoken {new_access_token}'
        if method == 'GET':
            response = requests.get(url, headers=headers, params=data)
        else:
            response = requests.post(url, headers=headers, json=data)
    return response.json()

def some_view(request):
    data = {"select_query": "select Full_Name, Lead_Status from Leads where (Full_Name is not null)"}
    response_data = make_zoho_request('/crm/v2/coql', method='POST', data=data)
    return JsonResponse(response_data)

def saveLeads(request):
    body = {"select_query": "select Full_Name, Lead_Status from Leads where (Full_Name is not null)"}
    data = make_zoho_request('/crm/v2/coql', method='POST', data=body)
    leads_data = data.get('data', [])
    for lead in leads_data:
        Lead.objects.update_or_create(
            zoho_id=lead['id'],
            defaults={
                'name': lead['Full_Name'],
                'status': lead['Lead_Status'],
            }
        )
    return JsonResponse({'message': 'Leads saved successfully'})

def get_products_group(request):
    response_data = make_zoho_request('/inventory/v1/itemgroups', method='GET', data=None, organizationid=organizationid)
    return JsonResponse(response_data)

def get_subscriptions(request):
    response_data = make_zoho_request('/billing/v1/subscriptions', method='GET', data=None, organizationid=organizationid)
    return JsonResponse(response_data)

def get_plans(request):
    response_data = make_zoho_request('/billing/v1/plans', method='GET', data=None, organizationid=organizationid)
    return JsonResponse(response_data)

def get_quotes(request):
     data = {"select_query": "select Subject, Quote_Stage, Grand_Total, Contact_Name.Full_Name, Account_Name.Account_Name, Deal_Name.Deal_Name, Owner from Quotes where (Subject is not null)"}
     response_data = make_zoho_request('/crm/v2/coql', method='POST', data=data)
     return JsonResponse(response_data)