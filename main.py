from query_engine import query_engine

from flask import Flask, jsonify, request 
  
app = Flask(__name__) 
  
@app.route('/', methods = ['POST']) 
def home(): 
  
    if(request.method == 'POST'):
        query_str = request.form.get('query')
        if not query_str:
            raise Exception("Query str not sent")
        response = query_engine.query(query_str)
        print(str(response))
        return jsonify({'data': str(response)}) 

  
# driver function 
if __name__ == '__main__':

    print("Now starting server")
  
    app.run(port=8000, debug = True) 
