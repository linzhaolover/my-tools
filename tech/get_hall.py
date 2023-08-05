from datetime import datetime

import urllib3
import json
import requests

import os

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header




urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

token = "eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjE2NDExMGZmLWQ3M2QtNDhiZS05YmFmLWZmNzgwMTYxMjg2MiJ9.KpCU0IRqa91EOoZ07FXhoF1-v1hV8uZhv3RMBUexIazhpj-DlbzYEufiTdGQrJaj22yDIzkIgsbIe6wmppPGMQ"


class MyMail(object):

    def send_mail(self, content):
        # SMTP server settings
        smtp_server = 'smtp.qiye.aliyun.com'
        smtp_port = 465
        smtp_username = 'business@x-metaview.com'
        # smtp_password = 'Xys20228888'

        # Email content
        subject = f'send hall report {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        body =  content
        sender = 'business@x-metaview.com'

        # 多个recipient 
        recipient = ','.join(['linzhaolover@163.com'])


        # Create a MIME multipart message
        message = MIMEMultipart()
        message['Subject'] = Header(subject, 'utf-8')
        message['From'] = sender
        message['To'] = recipient

        # Add the body of the email
        body_part = MIMEText(body, 'plain', 'utf-8')
        message.attach(body_part)

        # Add the attachments
        # attachments = ['test_return.py', 'test_mail.py']
        attachments = []
        dir = "pystudy"
        for attachment in attachments:
            attachment_path = os.path.join(dir, attachment)
            with open(attachment_path, 'rb') as file:
                attachment_part = MIMEApplication(file.read(), Name=attachment)
                attachment_part['Content-Disposition'] = f'attachment; filename="{attachment}"'
                message.attach(attachment_part)

        # Create a SMTP connection
        smtp_conn = smtplib.SMTP_SSL(smtp_server, smtp_port)
        smtp_conn.login(smtp_username, smtp_password)

        # Send the email
        smtp_conn.sendmail(sender, recipient.split(","), message.as_string())

        # Close the SMTP connection
        smtp_conn.quit()




headers = {
   "Content-Type": "application/json;charset=UTF-8",
   "Authorization": "Bearer " + token,
}

def get_schedule_by_hallid(query_date="2023/08/11"):
    """
    https://pcticket.cstm.org.cn/prod-api/pool/getScheduleByHallId?hallId=2&openPerson=1&queryDate=2023/08/11&saleMode=1&single=true
    """
    url = "https://pcticket.cstm.org.cn/prod-api/pool/getScheduleByHallId"
    payload = {
        "hallId": 2,
        "openPerson": 1,
        "queryDate": query_date,
        "saleMode":1,
        "single": True,
    }
    try:
        response = requests.get(url, params=payload, headers=headers, verify=False)
        response.raise_for_status()
        # print(response.url)
        # print(response.json())
    except Exception as ex:
        print(ex)
        return {"code": -1, "data": []}
    ret_data = response.json()
    if ret_data.get("code") != 200:
        print(ret_data)
        return {"code": -1, "data": []}


    ret = {"code": -1, "data": []}
    data = response.json().get("data")
    for d in data:
        # print(d)
        ticket_pool = d.get("ticketPool")
        td = {"scheduleName": d.get("scheduleName"), "name": d.get("name"), "currentDate": d.get("currentDate"), "ticketPool": ticket_pool, }
        if ticket_pool >= 2:
            ret["code"] = 0
            ret["data"].append(td)
    return ret

def get_schedule_id():
    url = "https://pcticket.cstm.org.cn/prod-api/pool/getPriceByScheduleId"
    payload = {
        "hallId": 2,
        "openPerson": 1,
        "queryDate": "2023/08/11",
        "saleMode":1,
        "scheduleId": 23,
    }
    response = requests.get(url, params=payload, headers=headers, verify=False)
    print(response.url)
    data = response.json().get("data")
    for d in data:
        print({"priceName":d.get("priceName"), "ticketPool": d.get("ticketPool"), "price": d.get("price")})
    return response



def get_contract_list():
    url = "https://pcticket.cstm.org.cn/prod-api/system/individualContact/list"
    payload = {"userId":1579613}
    response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
    return response

# response = get_schedule_id()
# response = get_contract_list()
# print(json.dumps(response.json(), indent=4, ensure_ascii=False))

if __name__ == "__main__":
    query_dates = [
        "2023/08/06",
        "2023/08/08",
        "2023/08/09",
        "2023/08/10",
        "2023/08/11",
        "2023/08/12",
    ]

    data = []
    for date in query_dates:
        print(date)
        ret = get_schedule_by_hallid(date)
        if ret.get("code") == 0:
            data.extend(ret.get("data"))
            print("x" * 20)
            # print(ret)


    if len(data):
        content = json.dumps(data, indent=4, ensure_ascii=False)
        print(content)

        print("send mail -- >>")
        MyMail().send_mail(content)
