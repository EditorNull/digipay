from os import system
import uuid
from base64 import b64encode

try:
    from requests import Session
except ModuleNotFoundError:
    system("pip install requests")
    from requests import Session

class digipay:
    def __init__(self , proxy=None):
        self.proxies = {"http" : proxy , "https" : proxy}
        self.session = Session()
        self.uuid = str(uuid.uuid4())
        self.auth = "Basic " + b64encode(f'webapp-client-id:webapp-client-secret-debee79d-b04d-47ef-8ed5-c32e24ec836e'.encode()).decode()
    def sendcode(self , phone):
        self.json = {
            "deviceAPI": "WEB_BROWSER",
            "deviceId": self.uuid,
            "deviceModel": "Windows/Chrome",
            "osName": "WEB",
            "cellNumber": phone
        }
        self.headers = {
            "Accept": "application/json",
            "Agent": "WEB",
            "Authorization": self.auth,
            "Client-Version": "1.0.0",
            "Content-Type": "application/json",
            "Digipay-Version": "2022-10-04",
            "Referer": "https://app.mydigipay.com/auth/login",
            "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        }
        self.resp = self.session.post(url="https://app.mydigipay.com/digipay/api/users/send-sms" , headers=self.headers , json=self.json , proxies=self.proxies).json()
        if self.resp["result"]["title"] == "SUCCESS":
            self.userId = self.resp["userId"]
            return self.resp
        else:
            return {"result" : "false" , "message" : "OTP_WAIT"}
    def verify(self , code):
        self.json = {
            "smsToken": code,
            "userId": self.userId
        }
        self.headers = {
            "Accept": "application/json",
            "Agent": "WEB",
            "Authorization": self.auth,
            "Client-Version": "1.0.0",
            "Content-Type": "application/json",
            "Digipay-Version": "2022-10-04",
            "Referer": "https://app.mydigipay.com/auth/login/otp",
            "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        }
        return self.session.post(url="https://app.mydigipay.com/digipay/api/users/activate" , headers=self.headers , json=self.json , proxies=self.proxies).json()["accessToken"]
    def account(self , accessToken):
        return self.session.get(url="https://app.mydigipay.com/digipay/api/users/profile" , headers={"Authorization" : f"Bearer {accessToken}"}).json()
    def balance(self , accessToken):
        return self.session.get(url="https://app.mydigipay.com/digipay/api/wallets/balance" , headers={"Authorization" : f"Bearer {accessToken}"}).json()["amount"]
    def transactions(self , accessToken):
        return self.session.post(url="https://app.mydigipay.com/digipay/api/activities/app/search" , headers={"Authorization" : f"Bearer {accessToken}"} , json={"restrictions":[],"orders":[{"field":"exerciseDate","order":"desc"}]}).json()
    def cashIn(self , amount , accessToken):
        self.headers = {
            "Accept": "application/json",
            "Agent": "WEB",
            "Authorization": f"Bearer {accessToken}",
            "Client-Version": "1.0.0",
            "Content-Type": "application/json",
            "Digipay-Version": "2022-10-04",
            "Referer": "https://app.mydigipay.com/service/cash-in",
            "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        }
        return self.session.post(url="https://app.mydigipay.com/digipay/api/wallets/cash-in" , headers=self.headers , json={"amount":amount,"redirectUrl":"https://app.mydigipay.com/payment/result/cash-in"}).json()["payUrl"]
    def buycharge(self , accessToken , oprator , phone , amount):
        if oprator == "mtn":
            opid = 2
        elif oprator == "mci":
            opid = 1
        elif oprator == "rightel":
            opid = 3
        else:
            return {"result" : "false" , "message" : "invalid oprator."}
        self.json = {
            "chargeType":opid,
            "targetedCellNumber":phone,
            "chargePackage":{"amount":amount},
            "operatorId":opid,
            "redirectUrl":"https://app.mydigipay.com/payment/result/top-up",
            "cellNumberType":opid
        }
        self.headers = {
            "Accept": "application/json",
            "Agent": "WEB",
            "Authorization": f"Bearer {accessToken}",
            "Client-Version": "1.0.0",
            "Content-Type": "application/json",
            "Digipay-Version": "2022-10-04",
            "Referer": "https://app.mydigipay.com/service/topup/confirm",
            "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        }
        self.resp = self.session.post(url="https://app.mydigipay.com/digipay/api/top-ups" , headers=self.headers , json=self.json).json()
        self.headers = {
            "Accept": "application/json",
            "Agent": "WEB",
            "Authorization": f"Bearer {accessToken}",
            "Client-Version": "1.0.0",
            "Content-Type": "application/json",
            "Digipay-Version": "2022-10-04",
            "Referer": "https://app.mydigipay.com/wallet/pay",
            "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        }
        return self.session.post(url="https://app.mydigipay.com/digipay/api/top-ups/pay/wallet" , headers=self.headers , json={"type":"wallet","ticket":self.resp["ticket"]}).json()