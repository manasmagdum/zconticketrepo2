from flask import Flask

app = Flask(__name__)

@app.route('/')
def source():
 html = 'Hello World!'
 return html
print("helloooo")
#from flask import Flask,request
#import json
#import requests
#import ast
#app = Flask(__name__)


#@app.route('/',methods=['POST'])
#def JsonHandler():
#    flag=0
#    RequestDict={}
#    ProfileDict={}
#    print('Is this JSON?',request.is_json)
#    #print(request.headers)
#    content=request.get_json()
#    print(content)
#    res = {"text":"Got it! From my estimation, your days to solve."}  
#    print('Done')
#    return json.dumps(res)

    


    
    
#if __name__ == '__main__':
#    app.run()
