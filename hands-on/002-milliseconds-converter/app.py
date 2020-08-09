from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', developer_name="Ummuhan", not_valid=False)

@app.route('/', methods=['POST'])   
def converter():
    number=request.form['number']
    if number.isdigit():
       millis=int(number)
       if millis>0 and millis<1000:
          result= f"Millisecond/s:{millis}" 
          return render_template('result.html', developer_name="Ummuhan", not_valid=True, milliseconds=millis, result=result)
       elif millis>1000:   
          seconds=(millis/1000)%60
          seconds = round(int(seconds), 3)
          minutes=(millis/(1000*60))%60
          minutes = round(int(minutes), 0)
          hours= round(( (millis/(1000*60*60))%24 ), 0)
          result= f"Hours:{hours}, Minutes:{minutes}, Seconds:{seconds}"
          return render_template('result.html', developer_name="Ummuhan", not_valid=True, milliseconds=millis, result=result)
       else:
          return render_template('index.html', developer_name="Ummuhan", not_valid=True)

    else:
        return render_template('index.html', developer_name="Ummuhan", not_valid=True)



if __name__=='__main__':
    app.run(debug=True)
    # app.run('localhost', port=5000, debug=True)
    #app.run('0.0.0.0', port=80)   
     