from flask import Flask, render_template, request, session,redirect
import pymongo
import datetime
import pywhatkit as pwk
import datetime

app = Flask(__name__)
app.secret_key = 'mysecretkey'
laptops = []
def database():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["sample"]
    col = db["laptop"]
    for doc in col.find():
        laptops.append(doc)

database()
# print(laptops)
# laptops = [
#     {'name': 'Laptop A', 'price': 700, 'os': 'Windows', 'primary_use': 'Work', 'description': 'This laptop is great for work and productivity.', 'image_url': 'https://via.placeholder.com/350x200','url':'https://www.amazon.in/Lenovo-E41-55-Windows-Graphics-Warranty/dp/B08KRZPGL3/ref=sr_1_3?keywords=laptop&sr=8-3'},
#     {'name': 'Laptop F', 'price': 800, 'os': 'Windows', 'primary_use': 'Work', 'description': 'This laptop is great for work .', 'image_url': 'https://via.placeholder.com/350x200','url':'https://www.amazon.in/Lenovo-E41-55-Windows-Graphics-Warranty/dp/B08KRZPGL3/ref=sr_1_3?keywords=laptop&sr=8-3'},
#     {'name': 'Laptop B', 'price': 1200, 'os': 'macOS', 'primary_use': 'Multimedia', 'description': 'This laptop is perfect for multimedia and creative work.', 'image_url': 'https://via.placeholder.com/350x200','url':'https://www.amazon.in/Lenovo-E41-55-Windows-Graphics-Warranty/dp/B08KRZPGL3/ref=sr_1_3?keywords=laptop&sr=8-3'},
#     {'name': 'Laptop C', 'price': 900, 'os': 'Linux', 'primary_use': 'Work', 'description': 'This laptop is ideal for work and development.', 'image_url': 'https://via.placeholder.com/350x200','url':'https://www.amazon.in/Lenovo-E41-55-Windows-Graphics-Warranty/dp/B08KRZPGL3/ref=sr_1_3?keywords=laptop&sr=8-3'},
#     {'name': 'Laptop D', 'price': 1500, 'os': 'Windows', 'primary_use': 'Gaming', 'description': 'This laptop is designed for gaming and entertainment.', 'image_url': 'https://via.placeholder.com/350x200','url':'https://www.amazon.in/Lenovo-E41-55-Windows-Graphics-Warranty/dp/B08KRZPGL3/ref=sr_1_3?keywords=laptop&sr=8-3'},
#     {'name': 'Laptop E', 'price': 600, 'os': 'Windows', 'primary_use': 'Browsing', 'description': 'This laptop is great for browsing the web and light use.', 'image_url': 'https://via.placeholder.com/350x200','url':'https://www.amazon.in/Lenovo-E41-55-Windows-Graphics-Warranty/dp/B08KRZPGL3/ref=sr_1_3?keywords=laptop&sr=8-3'}
# ]
@app.route('/')
def front():
    return render_template('front.html')


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/questions', methods=['GET', 'POST'])
def questions():
    if request.method == 'POST':
        session['budget'] = request.form['budget']
        session['os'] = request.form['os']
        session['primary_use'] = request.form['primary_use']
        session['battery'] = request.form['battery']
        session['ram'] = request.form['ram']
        session['storage'] = request.form['storage']
        session['displaysize'] = request.form['displaysize']
        session['weight'] = request.form['weight']
        session['displayres'] = request.form['displayres'] 
        return redirect('/results')

    return render_template('questions.html')
suglap = []
cityname = ""
suggested_laptops = []
@app.route('/results')

def results():
    
    budget = session.get('budget')
    os = session.get('os')
    primary_use = session.get('primary_use')
    battery = session.get('battery')
    ram = session.get('ram')
    storage = session.get('storage')
    displaysize = session.get('displaysize')
    weight  = session.get('weight')
    displayres = session.get('displayres')

 
    # suggested_laptops = []
    for laptop in laptops:
        # print(laptop)  and laptop['ram'] == ram and laptop['storage'] == storage and laptop['displaysize'] == displaysize and laptop['weight'] >= weight and laptop['displayres'] == displayres and
        condition  = laptop['os'] == os  and laptop['primary_use'] == primary_use and int(battery) <= laptop['battery']  and laptop not in suggested_laptops and laptop['ram'] == ram and laptop['storage'] == storage and laptop['displaysize'] == displaysize and laptop['displayres'] == displayres
        if budget == 'less-than-500' and laptop['budget'] <= 500:
            if condition:
                suggested_laptops.append(laptop)
        elif budget == '500-to-1000' and 500 < laptop['budget'] <= 1000:
            if condition:
                suggested_laptops.append(laptop)
        elif budget == 'more-than-1000' and laptop['budget'] > 1000:
            if condition:
                suggested_laptops.append(laptop)
        # else:
        #     if laptop['os'] == os and laptop not in suggested_laptops:
        #         suggested_laptops.append(laptop)

        # if primary_use == 'Any':
        #     if laptop not in suggested_laptops:
        #         suggested_laptops.append(laptop)
        # else:
        #     if laptop['primary_use'] == primary_use and laptop not in suggested_laptops:
        #         suggested_laptops.append(laptop)
    suglap = suggested_laptops
    return render_template('results.html', laptops=suggested_laptops)

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')

suggestedlaptopnames = []
for doc in suggested_laptops:
    suggestedlaptopnames.append(doc)


# @app.route('/whatsapp', methods=['POST'])
# def whatsapp():
#     selected = request.form.getlist('answers')
#     return render_template('whatsapp.html', selected=selected)

@app.route('/checkboxlaptop', methods=['GET', 'POST'])
def checkboxlaptop():
    return render_template('checkboxlaptop.html', questions=suggested_laptops)

selected=[]
city=""
laptopsname = ""
@app.route('/whatsapp',methods=['POST'])
def whatsapp():
    global laptopsname
    global city
    global cityname
    name = request.form['name']
    email = request.form['email']
    city = request.form['city']
    cityname = request.form['city']
    message = request.form['message']
    selected = request.form.getlist('answers')
    laptopsname = "name: "+name+"\n"+"email: "+email+'\n'+"city: "+city+'\n\n'+"meaasge:"+message+"\n\n"
    for i in selected: 
        laptopsname+= i+'\n'
    
    return render_template('whatsapp.html', selected=selected)


data = []
d = {}

def retrievephonenumber(city):
        global d
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db  = client['sample']
        doc = db['phone']
        for d in doc.find():
            data.append(d)
        for i in data:
            second_key = list(i.keys())[1]
            d[second_key] = i[second_key]
        print(d)
        return d[city.strip()]

# store the shops

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["sample"]
col = db["shops"]
shopdict = []
shop = {}
for i in col.find():
    shopdict.append(list(i)[1])
    shop[list(i)[1]] = i[list(i)[1]]









@app.route('/sendmsg')
def sendmsg():  
    now = datetime.datetime.now()
    # message = " ".join(selected)
    hour = now.hour
    minute = now.minute
    i = 0
    for num in retrievephonenumber(city):
        try:
            pwk.sendwhatmsg(num, laptopsname, hour, minute+i+1)
            print(f"Message sent to {num}!")
        except:
            print(f"Error sending message to {num}")
        i+=1
    # return redirect('/results')
    # print(shop[city])
    return render_template("shops.html", shop=shop[cityname.strip()])

 


# def sendmsg(selectedlaptops):
#     client = pymongo.MongoClient("mongodb://localhost:27017/")
#     db  = client['sample']
#     doc = db['phone']
#     ans = []
#     for d in doc.find():
#         ans.append(d)
#     numbers = dict()
#     for i in ans:
#         numbers['coimbatore'] = i['coimbatore']
#     print(numbers) 
#     phonenum = numbers[city]
#     print(phonenum)
#     now = datetime.datetime.now()
#     message = "Hi, how are you?"
#     hour = now.hour
#     minute = now.minute
#     i = 0
#     for num in phonenum:
#         try:
#             pwk.sendwhatmsg(num, message, hour, minute+i+1)
#             print(f"Message sent to {num}!")
#         except:
#             print(f"Error sending message to {num}")
#         i+=1

# code for searching laptops
@app.route("/",methods=["GET", "POST"])
def searchlap():
    return render_template("searchlap.html")


laptop_results = []
laptop_name=""

@app.route("/searchlap", methods=["GET", "POST"])
def search():
    laptop_results.clear()

    global laptop_name
    laptop_name = request.form.get("laptop")
    for i in laptops:
        if laptop_name.lower() in i['name'].lower():
            laptop_results.append(i)     
    return render_template("searchlap.html", laptops=laptop_results)

# shops retrival page

# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client["sample"]
# col = db["shops"]
# shopdict = []
# shop = {}
# for i in col.find():
#     shopdict.append(list(i)[1])
#     shop[list(i)[1]] = i[list(i)[1]]



# Define a route to display the shop details
@app.route("/show_shops")
def show_shops():
    return render_template("shops.html", shop=shop[city])

if __name__ == '__main__':
    app.run(debug=True)




