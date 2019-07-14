from flask import Flask, render_template, request
from decouple import config # send_message.py 에서 복사
import requests # send_message.py 에서 복사

app = Flask(__name__)

api_url = 'https://api.telegram.org' # send_message.py 에서 복사
token = config('TELEGRAM_BOT_TOKEN') # send_message.py 에서 복사
chat_id = config('CHAT_ID') # send_message.py 에서 복사
naver_client_id = config('NAVER_CLIENT_ID') 
naver_client_secret = config('NAVER_CLIENT_SECRET')

# https://api.telegram.org/bot643259608:AAH8e9jZ6419YJF_xEj5g1mkT036l3DEzUk/setWebhook?url=https://aee0d68d.ngrok.io

@app.route("/")
def hello():
    return "Hello World!"


@app.route('/write')
def write():
    return render_template('write.html')


@app.route('/send')
def send():
    token = config('TELEGRAM_BOT_TOKEN')
    chat_id = config('CHAT_ID')
    text = request.args.get('message')

    requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')

    return render_template('send.html')


@app.route(f'/{token}', methods=['POST']) # methods는 명시해줘야함
def telegram():
    # step 1. 구조 print 해보기 & 변수 저장
    print(request.get_json())
    from_telegram = request.get_json()

    # step 2. 그대로 돌려보내기
    if from_telegram.get('message') is not None: # NoneType일 경우 예외처리
        chat_id = from_telegram.get('message').get('from').get('id')
        text = from_telegram.get('message').get('text')

        # 2. keyword
        if text[0:4] == '/번역 ':
            headers = {'X-Naver-Client-Id': naver_client_id, 'X-Naver-Client-Secret': naver_client_secret}
            data = {'source': 'ko', 'target': 'en', 'text': text[4:]}
            papago_res = requests.post('https://openapi.naver.com/v1/papago/n2mt', headers=headers, data=data)
            text = papago_res.json().get('message').get('result').get('translatedText')

        res = requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')
    
    return '', 200



