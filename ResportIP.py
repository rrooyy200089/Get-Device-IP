import requests
from time import sleep

def get_external_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()  # 如果回應狀態碼不是200，將拋出一個HTTPError異常
        ip_info = response.json()
        return ip_info['ip']
    except requests.RequestException as e:
        return f"Error occurred: {e}"
    
def lineNotifyMessage(msg):
      token = "" # 請輸入你的LINE Notify Token
      headers = {
          "Authorization": "Bearer " + token, 
          "Content-Type" : "application/x-www-form-urlencoded"
      }
	
      payload = {'message': msg}
      r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
      return r.status_code

if __name__ == "__main__":
    while True:
        external_ip = get_external_ip()
        if "Error" not in external_ip: break
        sleep(3.0)
    file = open("ip.txt", 'r')
    old_ip = file.readline()
    file.close()
    if external_ip != old_ip:
        with open("ip.txt", 'w', newline="", encoding='utf-8') as ip_file:
            ip_file.write(external_ip)
        lineNotifyMessage(f"RespberryPi new IP：{external_ip}")
    # print(f"External IP address: {external_ip}")