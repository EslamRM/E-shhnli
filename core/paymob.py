import requests
import json

api_key = "ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6VXhNaUo5LmV5SmpiR0Z6Y3lJNklrMWxjbU5vWVc1MElpd2libUZ0WlNJNklqRTJNRE16TlRneU9UUXVNekEzTVRnM0lpd2ljSEp2Wm1sc1pWOXdheUk2TXpNeE5UZDkuUnh4b1V1TEQwbHJhTHBxV1d2RlQ5TFhKS2tRMXEzNWFhVjFJQUhmMzdWTVBRSXlndkhRSE5yQzUzTW1iNVBpZ1JuZVpreHFVMEZIaHZLY3VZM1VWbFE="
def auth(api_key):
    url = "https://accept.paymobsolutions.com/api/auth/tokens"
    payload = {
        "api_key": api_key,
        }

    headers = {
        "content-type": "application/json"
        }
    modified_payload = json.dumps(payload)
    response = requests.request("POST", url, headers=headers, data = modified_payload)
    response = response.json()
    final_response = {
        "token": response['token'],
        "merchant_id": response['profile']['id'],
    }
    return final_response



def create_order(previous_response, amount, currency, items=False, merchant_order_id=False,
                 delivery_needed=False):
    url = "https://accept.paymobsolutions.com/api/ecommerce/orders"
    querystring = {"token": previous_response['token']}
    payload = {
        "delivery_needed": delivery_needed,
        "merchant_id": previous_response['merchant_id'],
        "amount_cents": amount,
        "currency": currency,
        "items": [],
    }
    if merchant_order_id:
        payload["merchant_order_id"] = merchant_order_id
    if items:
        payload["items"] = items
    headers = {
        "content-type": "application/json"
    }
    modified_payload = json.dumps(payload)
    response = requests.post(url, data=modified_payload, headers=headers, params=querystring)
    response = response.json()
    previous_response['order_id'] = response['id']
    previous_response['amount'] = amount
    previous_response['currency'] = currency
    return previous_response

def order(previous_response, amount, currency, items=False, merchant_order_id=False,
                 delivery_needed=False):
    
    url = "https://accept.paymobsolutions.com/api/ecommerce/orders"

    payload = {
        "auth_token":previous_response['token'],
        "delivery_needed":"false",
        "merchant_id":previous_response["merchant_id"],
        "amount_cents":amount,
        "currency":currency,
        "items":[],
        }
    headers = {
        "content-type": "application/json"
        }

    modified_payload = json.dumps(payload)
    response = requests.request("POST", url, headers=headers, data = modified_payload)
    response = response.json()
    previous_response['order_id'] = response['id']
    previous_response['amount'] = amount
    previous_response['currency'] = currency
    return previous_response

billing_info = {"apartment":"803","email":"claudette09@exa.com",
                "floor": "42","first_name": "Clifford","street":"Ethan Land",
                "building":"8028","phone_number": "+86(8)9135210487",
                "shipping_method":"PKG","postal_code":"01898",
                "city":"Jaskolskiburgh","country": "CR",
                "last_name": "Nicolas", "state": "Utah"}

def pay(previous_response, card_integration_id, billing_info):
    
    url = "https://accept.paymobsolutions.com/api/acceptance/payment_keys"
    payload = {
        "auth_token":previous_response['token'],
        "lock_order_when_paid":"false",
        "integration_id":card_integration_id,
        "amount_cents":previous_response['amount'],
        "currency":previous_response['currency'],
        "expiration":3600,
        "order_id":previous_response['order_id'],
        "billing_data":billing_info,
    }
    headers = {
        "content-type": "application/json"
        }

    modified_payload = json.dumps(payload)
    response = requests.request("POST", url, headers=headers, data = modified_payload)
    response = response.json()
    previous_response['payment_key'] = response['token']
    return previous_response



# url4 = "https://accept.paymobsolutions.com/api/acceptance/iframes/"+str(96321)+"?payment_token="+step3['payment_key']

# payload4 = {}
# headers4= {}
# response5 = requests.request("GET", url4, headers=headers4, data = payload4)


def transaction_res(previous):
    url = "https://accept.paymobsolutions.com/api/acceptance/payments/pay"

    payload = {
        "source": {
            "identifier": "wallet mobile number",
            "subtype": "WALLET"
        },
            "payment_token":previous['payment_key'],
        }
    headers = {
            "content-type": "application/json"
            }
    modified_payload = json.dumps(payload)
    response = requests.request("POST", url, headers=headers, data = modified_payload)
    response = response.json()
    return response

def transaction_response(params):
    query_params = {'id': str(params['id']), 'pending': str(params['pending']), 'amount_cents': str(params['amount_cents']),
                    'success': str(params['success']), 'is_auth': str(params['is_auth']), 'is_capture':
                        str(params['is_capture']), 'is_standalone_payment': str(params['is_standalone_payment']), 'is_voided':
                        str(params['is_voided']), 'is_refunded': str(params['is_refunded']), 'is_3d_secure':
                        str(params['is_3d_secure']), 'integration_id': str(params['integration_id']), 'profile_id':
                        str(params['profile_id']), 'has_parent_transaction': str(params['has_parent_transaction']), 'order':
                        str(params['order']), 'created_at': str(params['created_at']), 'currency':
                        str(params['currency']), 'error_occured': str(params['error_occured']), 'owner': str(params['owner']),
                    'parent_transaction': str(params['parent_transaction']), 'source_data.type':
                        str(params['source_data']['type']), 'source_data.pan': str(params['source_data']['pan']),
                    'source_data.sub_type': str(params['source_data']['sub_type'])}
    html = ""
    return query_params, html
