import requests
import json


class Ninebot():
    name = "九号出行"

    def __init__(self, deviceId, authorization):
        self.signUrl = "https://cn-cbu-gateway.ninebot.com/portal/api/user-sign/v1/sign"
        self.validUrl = "https://cn-cbu-gateway.ninebot.com/portal/api/user-sign/v1/status"
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": authorization,
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Host": "cn-cbu-gateway.ninebot.com",
            "Origin": "https://api5-h5-app-bj.ninebot.com",
            "from_platform_1": "1",
            "language": "zh",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Segway v6 C 606093338",
            "Referer": "https://api5-h5-app-bj.ninebot.com/"
        }
        self.deviceId = deviceId

    def sign(self, session, msg):
        try:
            response = session.post(
                url=self.signUrl, headers=self.headers, json={
                    "deviceId": self.deviceId
                })
            if response.status_code == 200:
                response_data = response.json()
                if (response_data.get("code") == 0):
                    checkin_num = response.json().get("data", {}).get('consecutiveDays')
                    msg.append({"name": "签到成功", "value": f"已连续签到{checkin_num}天"})
                else:
                    msg.append({"name": "签到失败", "value": f"{response_data.get('msg')}"})
        except Exception as e:
            msg.extend([
                {"name": "签到信息", "value": "签到失败"},
                {"name": "错误信息", "value": str(e)},
            ])

    def valid(self, session):
        try:
            content = session.get(url=self.validUrl, headers=self.headers)
        except Exception as e:
            return False, f"登录验证异常,错误信息: {e}"
        json_data = content.json()
        if content.status_code == 200:
            if json_data.get("code") == 0:
                return json_data.get("data", False), ""
            else:
                return False, json_data.get("msg")
        return False, "登录信息异常"

    def main(self):
        session = requests.session()
        valid_data, err_info = self.valid(session)
        if valid_data:
            completed = valid_data.get("currentSignStatus") == 1
            msg = [
                {"name": "连续签到天数", "value": f"{valid_data.get('consecutiveDays', '')}天"},
                {"name": "今日签到状态", "value": "已签到" if completed else "未签到"}
            ]
            if not completed:
                self.sign(session, msg)
        else:
            msg = [
                {"name": "相关信息", "value": f"{err_info}"},
            ]
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        return msg


# if __name__ == "__main__":
#     deviceId_value = "BC550B6A-3276-4775-90E6-3BF613AAEB35"  # 此处替换为真实的deviceId值
#     authorization_value = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjk4MDI2MjMzNzk5NTEyMDY0IiwiYXVkaWVuY2UiOiJtb2JpbGUiLCJ1c2VyX25hbWUiOiJrYWlwY2MiLCJjbGllbnRfaWQiOiJhcHBfY2xpZW50X2lkX3ZlaGljbGUiLCJyZWdfZGF0ZSI6MTcyOTUxNTE3MCwiYXVkIjpbImlvdC13ZWJhcHAiXSwiYXJlYUNvZGUiOiI4NiIsInBob25lIjoiMTgwNjYxMjg0NDgiLCJzY29wZSI6WyJyZWFkIl0sImV4cCI6MTczNzI3MDEzMSwicmVnaW9uIjoiYmoiLCJqdGkiOiJ5MUtPd0QtaXdqYWM5bjNhVWZyc0JjY1hScVEiLCJlbWFpbCI6bnVsbH0.v1MlCvcl_S6WNmEj0cOBJfHFepfd15BR2tixdqOZMQl2vH0do5mtFE098wGvXPDDP8VM0PHzbm9xtgI5pqUFLcqVX7zpAUyDlkcU-c_OlpzCFeQlHcLJZaa6lNYiuCYJiiA0CxdaKtb3JXSOd86SL_TFFDgIpr4-BFdvfIMCqig"  # 此处替换为真实的authorization值
#     res = Ninebot(deviceId_value, authorization_value).main()
#     print(res)
    
    