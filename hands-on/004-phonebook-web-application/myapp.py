from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import os
app= Flask(__name__)

db_endpoint = open('/home/ec2-user/dbserver.endpoint', 'r', encoding='UTF-8')

# Configure mysql database
app.config['MYSQL_DATABASE_HOST'] = db_endpoint.readline().strip()
# app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_URL_2')
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = '12345678'
app.config['MYSQL_DATABASE_DB'] = 'phonebook'
app.config['MYSQL_DATABASE_PORT'] = 3306

db_endpoint.close()


mysql = MySQL()
mysql.init_app(app)
connection = mysql.connect()
connection.autocommit(True)
cursor = connection.cursor()

#this function will run it locally in init-pb-db.py
# def init_todo_db():
#     drop_table = 'DROP TABLE IF EXISTS phonebook.phonebook;'
#     phonebook_table = """
#     CREATE TABLE phonebook(
#     id INT NOT NULL AUTO_INCREMENT,
#     name VARCHAR(100) NOT NULL,
#     number VARCHAR(100) NOT NULL,
#     PRIMARY KEY (id)
#     ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
#     """
#     data = """
#     INSERT INTO phonebook.phonebook (name, number)
#     VALUES
#         ("Amy", "1234567890"),
#         ("Ozzy", "67854"),
#         ("Ayvi", "876543554");
#     """
#     cursor.execute(drop_table)
#     cursor.execute(phonebook_table)
#     cursor.execute(data)

def find_number(keyword):
    query = f"""
    SELECT * FROM persons WHERE name like '%{keyword}%';
    """
    cursor.execute(query)
    result = cursor.fetchall()
    persons= [{"name":row[1], "number":row[2]} for row in result]
   
    if not any(persons):
        persons = [{"name":'Not found.', "number":'Not Found.'}]
    return persons


def add_number(name, number):
    query = f"""
    SELECT * FROM persons WHERE name like '{name}';
    """
    cursor.execute(query)
    result = cursor.fetchall()
    response = 'Error occurred..'
    if name == " " or number == " ":
        response = 'person or number can not be emtpy!!'
    elif not any(result):
        insert = f"""
        INSERT INTO persons(name,number) 
        VALUES ('{name}', '{number}');
        """
        cursor.execute(insert)
        connection.commit()
        response = f'{name} successfully added to phonebook'
    else:
        response = f'{name} already exits.'
    return response


def update_person(name, number):
    query = f"""
    SELECT * FROM phonebook WHERE name like '{name.strip().lower()}';
    """

    cursor.execute(query)
    row = cursor.fetchone()

    if row is None:
        return f'Person with name {name.strip().title()} does not exits.'
    
    update = f"""
    UPDATE phonebook
    SET name='{row[1]}', number = '{number}'
    WHERE id= {row[0]};
    """

    cursor.execute(update)

    return f'Phone record of {name.strip().title()} is updated successfully '


def delete_person(name):
    query = f"""
    SELECT * FROM phonebook WHERE name like '{name.strip().lower()}';
    """

    cursor.execute(query)
    row = cursor.fetchone()

    if row is None:
        return f'Person with name {name.strip().title()} does not exist, no need to delete.'
    
    delete = f"""
    DELETE FROM phonebook
    WHERE id= {row[0]};
    """

    cursor.execute(delete)
    return f'Phone record of {name.strip().title()} is deleted from the phonebook successfully.'


@app.route('/', methods=["GET", "POST"])
def find_records():
    if request.method == 'POST':
         keyword = request.form['username']
         persons = find_number(keyword)
         return render_template('index.html', persons=persons, keyword=keyword, show_result=True, developer_name="Ummuhan")
    else:
         return render_template('index.html', show_result=False, developer_name='Ummuhan')

@app.route('/add', methods=['GET','POST'])
def add_record():
    if request.method == 'POST':
        name = request.form['username']
        if name is None or name.strip() == "":
            return render_template('add-update.html', not_valid=True, message='Invalid input: Name can not be empty', show_result=False, action_name='save', developer_name='Ummuhan')
        elif name.isdecimal():
            return render_template('add-update.html', not_valid=True, message='Invalid input: Name of person should be text', show_result=False, action_name='save', developer_name='Ummuhan')
        phone_number = request.form['phonenumber']
        if phone_number is None or phone_number.strip()== "":
            return render_template('add-update.html', not_valid=True, message='Invalid input: Phone number can not be empty', show_result=False, action_name='save', developer_name='Ummuhan')
        elif not phone_number.isdecimal():
            return render_template('add-update.html', not_valid=True, message='Invalid input: Phone number should be in numeric format', show_result=False, action_name='update', developer_name='Ummuhan')
        result = update_person(name, phone_number)
        return render_template('add-update.html', show_result=True, result=result, not_valid=False, action_name='save', developer_name='Ummuhan')
    else:
        return render_template('add-update.html', show_result=False, not_valid=False, action_name='save', developer_name='Ummuhan')

@app.route('/update', methods=['GET', 'POST'])
def update_record():
    if request.method == 'POST':
        name = request.form['username']  
        if name is None or name.strip()== "":
            return render_template('add-update.html', not_valid=True, message='Invalid input: Name can not be empty', show_result=False, action_name='update', developer_name='Ummuhan')      
        phone_number = request.form['phonenumber']
        if phone_number is None or phone_number.strip() == "":
            return render_template('add-update.html', not_valid=True, message='Invalid input: Phone number can not be empty', show_result=False, action_name='update', developer_name='Ummuhan')
        elif not phone_number.isdecimal():
            return render_template('add-update.html', not_valid=True, message='Invalid input: Phone number should be in numeric format', show_result=False, action_name='update', developer_name='Ummuhan')

        result = update_person(name, phone_number)
        return render_template('add-update.html', show_result=True, result=result, not_valid=False, action_name='update', developer_name='Ummuhan')
    else:
        return render_template('add-update.html', show_result=False, not_valid=False, action_name='update', developer_name='Ummuhan') 



@app.route('/delete', methods=['GET', 'POST'])
def delete_record():
    if request.method == 'POST':
        name = request.form['username']
        if name is None or name.strip() == "":
            return render_template('delete.html', not_valid=True, message='Invalid input: Name can not be empty', show_result=False, developer_name='Ummuhan')
        result = delete_person(name)
        return render_template('delete.html', show_result=True, result=result, not_valid=False, developer_name='Ummuhan')
    else:
        return render_template('delete.html', show_result=False, not_valid=False, developer_name='Ummuhan')        



if __name__=='__main__':
    #init_todo_db()
    #app.run(debug=True)       
    app.run(host='0.0.0.0', port=80)        
        
        





