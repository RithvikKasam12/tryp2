from flask import Flask,render_template,url_for,request, redirect
import mysql.connector
import matplotlib as plt
import io
import base64

app = Flask(__name__)

db = mysql.connector.connect(host="localhost",
            database="flaskdata",
            user="root",
            password="root")   




@app.route('/')
def hello():
    return render_template('login page.html')

@app.route('/main')
def main():
    return render_template('mainmenu.html')

"""@app.route('/create')
def create():
    return render_template('create.html')"""

@app.route('/display')
def display():
    return render_template('display.html')


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method=='POST':
        table_name = request.form['table_name']
        x_label = request.form['XV']
        y_label = request.form['YV']
        db = mysql.connector.connect(host="localhost",
            database="flaskdata",
            user="root",
            password="root")   
        cursor= db.cursor()
        cursor.execute(f"Create table {table_name} ({x_label} int(10), {y_label} int(10))")
        db.commit()
        return redirect(f'/add_data?table_name={table_name}&x_label={x_label}&y_label={y_label}')
        
    return render_template('make.html')
    



@app.route('/add_data', methods=['GET','POST'])
def add_data():
    if request.method=='POST':
        table_name = request.args.get('table_name')
        x_value = request.form['xval']
        y_value = request.form['yval']
        x_label = request.args.get('x_label')
        y_label = request.args.get('y_label')

        db = mysql.connector.connect(host="localhost",
            database="flaskdata",
            user="root",
            password="root")   

        cursor = db.cursor()
        sql = f"INSERT INTO {table_name} ({x_label}, {y_label}) VALUES (%s, %s)"
        val = (x_value, y_value)

        cursor.execute(sql, val)
        db.commit()
        
        return redirect(f'/plot_graph?table_name={table_name}&x_label={x_label}&y_label={y_label}')
    table_name=request.args.get('table_name')
    x_label=request.args.get('x_label')
    y_label=request.args.get('y_label')
    
    
    return render_template('data-entry.html', table_name=table_name)

        

@app.route('/graphit/')
def graphit():
    table_name = request.args.get('table_name')
    x_label = request.args.get('x-axis')
    y_label = request.args.get('y-axis')
    
    db = mysql.connector.connect(host="localhost",
            database="flaskdata",
            user="root",
            password="root") 
    cursor = db.cursor()

    cursor.execute(f"Select {x_label}, {y_label} From {table_name}")
    rows = cursor.fetchall()

    x = []
    y = []

    for row in rows:
        x.append(row[0])
        y.append(row[1])
    
    cursor.close()
    db.commit()
    db.close()
    
    plt.plot(x,y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(table_name)

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)

    return render_template('graphdp.html', table_name=table_name, x_label=x_label, y_label=y_label, img_data=img_bytes.getvalue())
            
    

if __name__=="__main__":
    app.run(debug=True)