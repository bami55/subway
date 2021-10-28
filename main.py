import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
headers = {
    'User-Agent': user_agent
}

url = f"https://www.jorudan.co.jp/time/{quote('eki_姪浜_福岡地下鉄空港線')}.html"

res = requests.get(url, headers=headers)
if res.ok:
    bs = BeautifulSoup(res.content, 'html.parser')
    train_services = bs.select('table.timetable2.tt_weekday tr td div a')
    for ts in train_services:
        href = ts.attrs['href']
        ym = re.findall(r'Dym=[0-9]+', href)[0].replace('Dym=', '').zfill(6)
        day = re.findall(r'Ddd=[0-9]+', href)[0].replace('Ddd=', '').zfill(2)
        hour = re.findall(r'Dhh=[0-9]+', href)[0].replace('Dhh=', '').zfill(2)
        minute = re.findall(r'Dmn=[0-9]+', href)[0].replace('Dmn=', '').zfill(2)
        time_info = f'{ym}{day} {hour}:{minute}'

        text_array = []
        for x in ts.span.children:
            text = x.text.strip()
            if text:
                text_array.append(text)
        for_info = ' - '.join(text_array)

        print(f'{time_info}: {for_info}')
else:
    print(res.status_code)
