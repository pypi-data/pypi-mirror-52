import requests
def balanse(wallet_id, token, result):
	url = "https://uc.simbrex.com/api/wallet/getBalance.php"
	payload = {
		
	"wallet_id": wallet_id,
	"token": token
}
	if result == True:
		headers = {}
		response = requests.request('POST', url, headers = headers, data = payload, allow_redirects=False)
		print(response.text)
	elif result == False:
		headers = {}
		response = requests.request('POST', url, headers = headers, data = payload, allow_redirects=False)

def transfer(wallet_id, token, to, sum, result):
	url = "https://uc.simbrex.com/api/wallet/transfer.php"
	payload = {
	"wallet_id": wallet_id,
	"token": token,
	"to": to,
	"sum": sum
	}
	if result == True:
		headers = {}
		response = requests.request('POST', url, headers = headers, data = payload, allow_redirects=False)
		print(response.text)
	elif result == False:
		headers = {}
		response = requests.request('POST', url, headers = headers, data = payload, allow_redirects=False)
		
def merchant_balanse(merchant_id, key, result):
	url = "https://uc.simbrex.com/api/merchant/getBalance.php"
	payload = {
	"merchant_id": merchant_id,
	"key": key
	}
	if result == True:
		headers = {}
		response = requests.request('POST', url, headers = headers, data = payload, allow_redirects=False)
		print(response.text)
	elif result == False:
		headers = {}
		response = requests.request('POST', url, headers = headers, data = payload, allow_redirects=False)

def merchant_transfer(merchant_id, key, to, sum, code, result):
	url = "https://uc.simbrex.com/api/merchant/transfer.php"
	payload = {
	"merchant_id": merchant_id,
	"key": key,
	"to": to,
	"sum": sum,
	"code": code
	}
	headers = {}
	if result == True:
		headers = {}
		response = requests.request('POST', url, headers = headers, data = payload, allow_redirects=False)
		print(response.text)
	elif result == False:
		headers = {}
		response = requests.request('POST', url, headers = headers, data = payload, allow_redirects=False)
		
def merchant_history(merchant_id, key, count, offset, result):
	url = "https://uc.simbrex.com/api/merchant/getHistory.php"
	payload = {
	"merchant_id": merchant_id,
	"key": key,
	"count": count,
	"offset": offset
	}
	if result == True:
		headers = {}
		response = requests.request('POST', url, headers = headers, data = payload, allow_redirects=False)
		print(response.text)
	elif result == False:
		headers = {}
		response = requests.request('POST', url, headers = headers, data = payload, allow_redirects=False)