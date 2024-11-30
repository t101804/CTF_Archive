from flask import Flask, render_template, send_from_directory, request, send_file, jsonify, render_template_string
import os, jwt, json

app = Flask(__name__)

IMAGE_DIR = os.path.join(app.root_path, 'static/images')

SECRET_KEY = "SUPER_SECRET_KEYS"
with open('config.json') as config_file:
    config = json.load(config_file)
    SECRET_KEY = config['secret_key']


def anti(words):
    anti = ["join","0","+","-",":","=", "()", "import", "os","system", "globals","subclasses", "call","subprocesses", "eval","getitem","popen","read", "self"]
    for word in anti:
        if word in words:
            print(word, "Nakal")
            return "Nakal"
    return words


@app.route('/')
def home():
    images = os.listdir(IMAGE_DIR)
    return render_template('home.html', images=images)

@app.route('/admin')
def admin():
    jwt_token = request.cookies.get('jwt_token')
    if not jwt_token:
        return "Not Authorized", 401
    
    try:
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
        return render_template('admin.html', user=payload)
    except jwt.ExpiredSignatureError:
        return "Token is Expired", 401
    except jwt.InvalidTokenError:
        return "Token Invalid", 401

@app.route('/check', methods=['POST'])
def check():

    jwt_token = request.cookies.get('jwt_token')
    if not jwt_token:
        return "Not Authorized", 401
    
    try:
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
        try:
            filename = request.form.get('filename')
            if len(filename) < 90:
                if anti(filename) != "Nakal":
                    if filename:
                        checking = f"<h1>Checking for Files: {filename}</h1>"
                        return render_template_string(checking)
                    else:
                        return "<h1>No filename provided</h1>", 400 
                else:
                    return "Nakal", 500
            else:
                return "<h1>Filename too long", 400
        except Exception as e:
            return f"Error: {str(e)}", 500 

    except jwt.ExpiredSignatureError:
        return "Token is Expired", 401
    except jwt.InvalidTokenError:
        return "Token Invalid", 401
    

@app.route('/download')
def download_image():
    whiteList = ["jpg", "png", "jpeg"]
    try:
        safeRequest = False 
        
        query = request.args
        if len(query) > 3:
            return "Request Denied"

        for param in query:
            print('3 last is ' + query[param][-3:])
            if query[param][-3:] in whiteList:
                safeRequest = True
                break

        if not safeRequest:
            return "Unsafe Request"

        filename = request.args.get('filename')
        print(filename)
        file_path = os.path.join(IMAGE_DIR, filename)
        if os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return "File not found", 404
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
