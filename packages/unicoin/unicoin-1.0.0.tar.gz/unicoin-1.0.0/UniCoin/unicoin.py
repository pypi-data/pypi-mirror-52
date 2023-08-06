import requests
def balanse(wallet_id, token):
	url = "https://uc.simbrex.com/api/wallet/getBalance.php"
	payload = {
		
	"wallet_id": wallet_id,
	"token": token
}
	headers = {}
	response = requests.request('POST', url, headers = headers, data = payload, allow_redirects=False)
	print(response.text)

def transfer(wallet_id, token, to, sum):
	url = "https://uc.simbrex.com/api/wallet/transfer.php"
	payload = {
	"wallet_id": wallet_id,
	"token": token,
	"to": to,
	"sum": sum
	}
	headers = {}
	response = requests.request('POST', url, headers = headers, data = payload, allow_redirects=False)
	print(response.text)
def merchant_balanse(merchant_id, key):
	url = "https://uc.simbrex.com/api/merchant/getBalance.php"
	payload = {
	"merchant_id": merchant_id,
	"key": key
	}
	headers = {}
	response = requests.request('POST', url, headers = headers, data = payload, allow_redirects=False)
	print(response.text)

def merchant_transfer(merchant_id, key, to, code):
	url = "https://uc.simbrex.com/api/merchant/transfer.php"
	payload = {
	"merchant_id": merchant_id,
	"key": key,
	"to": to,
	"code": code
	}
	headers = {}
	response = requests.request('POST', url, headers = headers, data = payload, allow_redirects=False)
	print(response.text)
def merchant_history(merchant_id, key, count, offset):
	url = "https://uc.simbrex.com/api/merchant/getHistory.php"
	payload = {
	"merchant_id": merchant_id,
	"key": key,
	"count": count,
	"offset": offset
	}
	headers = {}
	response = requests.request('POST', url, headers = headers, data = payload, allow_redirects=False)