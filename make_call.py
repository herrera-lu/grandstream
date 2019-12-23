import requests
from urllib3.exceptions import InsecureRequestWarning


class Grandstream:

    OUTGOING_DIGIT_DEFAULT = ""
    HS_DEFAULT = 0

    def __init__(self, ip, password):
        self.ip = ip
        self.password = password
        self.url = f"https://{self.ip}/cgi-bin"

    def call(self, phone_number, hs=HS_DEFAULT, outgoing_digit=OUTGOING_DIGIT_DEFAULT):
        call_params = {
            'passcode': self.password,
            'hs': hs,
            'phonenumber': f"{outgoing_digit}{phone_number}"
        }
        call_url = f"{self.url}/api-make_call"

        try:
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
            call_resp = requests.get(call_url, params=call_params, verify=False)
            call_resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(f"Call failed: {err}")
            return

        call_result = call_resp.json().get('response', 'ERROR: NO DATA')
        if call_result == "success":
            print("Calling!")
        else:
            print(f"Call failed: {call_result}")


if __name__ == "__main__":

    import ipaddress

    while True:
        try:
            ip = ipaddress.ip_address(input("IP: "))
            break
        except BaseException:
            print("Invalid IP...")

    password = input("Phone password: ")
    phone_number = input("Number to call: ")

    device = Grandstream(ip, password)
    device.call(phone_number)
