from flask import Flask,render_template,request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', developer_name='Ummuhan', not_valid=False)

@app.route('/', methods=['POST'])
def coverter():
    number=request.form['number']
    roman_numbers=["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    digits=[1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    result=[]
    if number.isdigit():
        number_decimal=int(number)
        if number_decimal > 0 and number_decimal <4000:
           i=0
           while i < len(digits):
               if number_decimal>=digits[i]:
                 result.append(roman_numbers[i])
                 number_decimal -= digits[i]
               else:
                 i += 1
                 result="".join(result)
           return  render_template('result.html', not_valid=False, developer_name='Ummuhan', number_decimal=number, number_roman=result)
        else:
           return render_template('index.html', not_valid=True, developer_name='Ummuhan')
    else:
        return render_template('index.html', developer_name='Ummuhan', not_valid=True)
if __name__=='__main__':
    app.run(debug=True)
    app.run('localhost', port=5000, debug=True)
    #app.run('0.0.0.0', port=80)