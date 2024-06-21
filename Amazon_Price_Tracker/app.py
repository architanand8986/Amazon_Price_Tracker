from flask import Flask,render_template,request,redirect,flash,session,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date,datetime
from scrapper import extract_Data
from plot import plot,check




app=Flask(__name__,template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Accounts.sqlite3'

# name of the table for db1 is accounts
app.secret_key="price"

db1=SQLAlchemy(app)


# creating a table in the database Accounts
# parent class
class Accounts(db1.Model):
    id=db1.Column(db1.Integer,primary_key=True)
    user=db1.Column(db1.String(50),nullable=False)
    password=db1.Column(db1.String(50),nullable=False)
    product=db1.relationship('Products',backref='track')
    
# creating one to many relationship
class Products(db1.Model):
    id=db1.Column(db1.Integer,primary_key=True)
    url=db1.Column(db1.String(100),nullable=False)
    name=db1.Column(db1.String(50),nullable=False)
    date=db1.Column(db1.Date,nullable=False)
    user_id=db1.Column(db1.Integer,db1.ForeignKey('accounts.id'))

# We would give user 7 slots for tracking data and after that user would be asked to clear
# all the trackers and start afresh
  
class Prices(db1.Model):
    id=db1.Column(db1.Integer,primary_key=True)
    price_id=db1.Column(db1.Integer,db1.ForeignKey('products.id'))
    p1 = db1.Column(db1.String(50))
    p2 = db1.Column(db1.String(50))
    p3 = db1.Column(db1.String(50))
    p4 = db1.Column(db1.String(50))
    p5 = db1.Column(db1.String(50))
    p6 = db1.Column(db1.String(50))
    p7 = db1.Column(db1.String(50))
    
class Date(db1.Model):
    id=db1.Column(db1.Integer,primary_key=True)
    date_id=db1.Column(db1.Integer,db1.ForeignKey('products.id'))
    d1=db1.Column(db1.String(10))
    d2=db1.Column(db1.String(10))
    d3=db1.Column(db1.String(10))
    d4=db1.Column(db1.String(10))
    d5=db1.Column(db1.String(10))
    d6=db1.Column(db1.String(10))
    d7=db1.Column(db1.String(10))
    
class LastTracked(db1.Model):
    id=db1.Column(db1.Integer,primary_key=True)
    track_id=db1.Column(db1.Integer,db1.ForeignKey('products.id'))
    date=db1.Column(db1.String(10))
    capacity=db1.Column(db1.Integer)     

# this table would store the official nane of the product on the amazon site
class OfficialName(db1.Model):
    id=db1.Column(db1.Integer,primary_key=True)
    name_id=db1.Column(db1.Integer,db1.ForeignKey('products.id'))
    name=db1.Column(db1.String(100))
    # currency=db1.Column(db1.String(5))    

# we can create a new column for storing currencies

# creating the database manually so it is working inside the context
with app.app_context():
    db1.create_all()    

@app.route("/")
def home():
    if "user" in session:
       
        return render_template("index.html",prop="nav-link")
    else:
        
        return render_template("index.html",prop="nav-link disabled")

# Use flash in flask with jinja templating to get over with a display bug in the program

# sign-in
@app.route("/account",methods=['GET','POST'])
def acc():
    if request.method=='GET':
        if "user" in session:
            return redirect("user")
        else:
            return render_template("signin.html")
    elif request.method=='POST':
        userid=request.form.get("email")
        password=request.form.get("password")
        
        check=Accounts.query.filter_by(user=userid).first()
        if check is not None:
            if check.password==password:
                session["user"]=userid
                return redirect("user")
            else:
                flash("Invalid Password")
                return redirect("account")
        else:
            flash("Invalid Username")
            return redirect("account")
                
        
        

# sign-up
@app.route("/create",methods=['GET','POST'])
def create():
    if request.method=='GET':
        return render_template("signup.html")
    elif request.method=='POST':
        userid=request.form.get("email")
        password=request.form.get("password")
        new_acc=Accounts(user=userid,password=password)
        username=Accounts.query.filter_by(user=userid).first()
        
        if username is not None:
            flash("User already exists")
            return redirect("create")
        else:
            
        
            try:
                db1.session.add(new_acc)
                db1.session.commit()
                session["user"]=userid
                flash("Successfully Signed-in")
                return redirect("user")
            except:
                flash("Account creation failed")
                return redirect("create")

          
@app.route("/user", methods=['GET','POST'])
def user():
    if request.method == "GET":
        try:
            userid=session["user"]
        except:
            flash("Sign-in to access Track items Page")
            return redirect("/")    
        flash("Successfully signed-in")
        return render_template("user.html",user=userid)
    
    elif request.method == "POST":
        user=session["user"]
        name=request.form.get("product")
        url=request.form.get("link")
        Add_date=date.today()
        own_id=Accounts.query.filter_by(user=user).first().id 
        
        # failsafe not implemented 
        nameCheck=Products.query.filter_by(name=name).all()
        if nameCheck is not None:
            for i in nameCheck:
                if i.user_id == own_id:
                 flash("Tracker with same name is active,pls change the name")
                 return redirect("user")
                
        urlCheck=Products.query.filter_by(url=url).all()
        if urlCheck is not None:
            for i in urlCheck:
                if i.user_id == own_id:
                 flash("Same product is already being tracked,Pls give a new product URL for tracking")
                 return redirect("user")
        
        
        
        new_product=Products(url=url,name=name,user_id=own_id,date=Add_date)
        
        try:
            db1.session.add(new_product)
            db1.session.commit()
            products=Products.query.filter_by(name=name).all()
            product_id=0
            for product in products:
                if product.user_id==own_id:
                    product_id=product.id
                     
            today=date.today().strftime("%d/%m/%Y")        
            new_track=LastTracked(track_id=product_id,capacity=0,date=today)
            new_price=Prices(price_id=product_id,p1="NOT_TRACKED",p2='NOT_TRACKED',p3='NOT_TRACKED',p4='NOT_TRACKED',p5='NOT_TRACKED',p6='NOT_TRACKED',p7='NOT_TRACKED')
            new_date=Date(date_id=product_id,d1='day-1',d2='day-2',d3='day-3',d4='day-4',d5='day-5',d6='day-6',d7='day-7')
            new_official=OfficialName(name_id=product_id,name="Product is not being tracked")
            db1.session.add(new_price)
            db1.session.add(new_track)
            db1.session.add(new_date)
            db1.session.add(new_official)
            db1.session.commit()
            return redirect("/user/item")
        
        except:
            return redirect("user")

@app.route("/user/item")
def items():
    user=session["user"]
    own_id=Accounts.query.filter_by(user=user).first().id
    products=Products.query.filter_by(user_id=own_id).all()
    return render_template("history.html",products=products)
                    

# destroy the session of the current user to sign-out
@app.route("/logout")
def logout():
    session.pop("user",None)
    flash("Successfully signed out")
    return redirect("/account")
        
@app.route("/item/update",methods=['GET','POST'])
def update():
    if request.method=="GET":
        id=request.args.get("id")
        product=Products.query.filter_by(id=id).first()
        flash("User not allowed to update the URL of the product")
        return render_template("update_item.html",product=product)
    
    elif request.method=='POST':
        name=request.form.get("product")
        id=request.form.get("id")
        
             
        product=Products.query.filter_by(id=id).first()
        try:
            product.name=name
            db1.session.commit()
            return redirect("/user/item")
        except:
            flash("Item Updation failed")
            redirect("/item/update")
        
        
        
     
@app.route("/item/delete",methods=['POST'])
def delete():
    if request.method=='POST':
        id=request.form.get("id")
        product=Products.query.filter_by(id=id).first()
        tracker=LastTracked.query.filter_by(track_id=id).first()
        official=OfficialName.query.filter_by(name_id=id).first()
        date=Date.query.filter_by(date_id=id).first()
        price=Prices.query.filter_by(price_id=id).first()
        
        try:
            db1.session.delete(product)
            db1.session.delete(tracker)
            db1.session.delete(official)
            db1.session.delete(date)
            db1.session.delete(price)
            db1.session.commit()
            return redirect("/user/item")
        except:
            return "ERROR"



@app.route("/item/activity",methods=['GET','POST'])
def activity():
    
        
    if request.method == 'POST':
        
        id=request.form.get("id")
    
        product=Products.query.filter_by(id=id).first()
        tracker=LastTracked.query.filter_by(track_id=id).first()
        official=OfficialName.query.filter_by(name_id=id).first()
        dates=Date.query.filter_by(date_id=id).first()
        prices=Prices.query.filter_by(price_id=id).first()
    
        d=[]
        p=[]
    
        d.append(dates.d1) 
        d.append(dates.d2) 
        d.append(dates.d3)
        d.append(dates.d4)
        d.append(dates.d5)
        d.append(dates.d6)
        d.append(dates.d7)
    
        p.append(prices.p1)
        p.append(prices.p2)
        p.append(prices.p3)
        p.append(prices.p4)
        p.append(prices.p5)
        p.append(prices.p6)
        p.append(prices.p7)
    
    # this method converts the arrays and converts it into dictionary
        my_dict=dict(zip(d,p))
   
         
        if official is None:
            name="Current object is not tracked"
        else:
            name=official.name
        
        return render_template("activity.html",product=product,track=tracker,name=name,dict=my_dict)


  
@app.route("/item/track",methods=['POST'])
def track():
    id=request.form.get("track")
    url=Products.query.filter_by(id=id).first().url
    tracker=LastTracked.query.filter_by(track_id=id).first()
    official=OfficialName.query.filter_by(name_id=id).first()
    dateobj=Date.query.filter_by(date_id=id).first()
    price=Prices.query.filter_by(price_id=id).first()
    
    today_date=date.today().strftime("%d/%m/%Y")
    days_tracked=tracker.capacity
    
    if days_tracked != 0:
        if today_date == tracker.date:
            return render_template("message.html",id=id,message="User allowed to track price only once a day",type="danger",head="OverRequest")
        
    my_dict=extract_Data(url)
    
    if my_dict is None:
        return render_template("message.html",id=id,message="No data is extracted from the given URL",type="danger",head="Failure")
    
    priceobj=my_dict["price"]
    
    if days_tracked == 0:
        dateobj.d1=today_date
        price.p1=priceobj
        official.name=my_dict["name"]
        # official.currency=my_dict["currency"]
        
        db1.session.commit()
    
    elif days_tracked == 1:
        dateobj.d2=today_date
        price.p2=priceobj
        db1.session.commit()
    
    elif days_tracked == 2:
        dateobj.d3=today_date
        price.p3=priceobj
        db1.session.commit()
    
    elif days_tracked == 3:
        dateobj.d4=today_date
        price.p4=priceobj
        db1.session.commit()
        
    elif days_tracked == 4:
        dateobj.d5=today_date
        price.p5=priceobj
        db1.session.commit()
        
    elif days_tracked == 5:
        dateobj.d6=today_date
        price.p6=priceobj
        db1.session.commit()
    
    elif days_tracked == 6:
        dateobj.d7=today_date
        price.p7=priceobj
        db1.session.commit()
        
    tracker.date=today_date
    tracker.capacity=(days_tracked+1)%7
    db1.session.commit()
    
    return render_template("message.html",id=id,message="Your Order is Successfully Tracked",type="success",head="Success")

 
@app.route("/item/advanced",methods=['POST'])
async def advanced():
    id=request.form.get("analysis")
    dates=Date.query.filter_by(date_id=id).first()
    prices=Prices.query.filter_by(price_id=id).first()
    official=OfficialName.query.filter_by(name_id=id).first()
    
    d=[]
    p=[]
    # making a array with correct sequence of dates and pushing it in plot remains....
    d.append(dates.d1) 
    d.append(dates.d2) 
    d.append(dates.d3)
    d.append(dates.d4)
    d.append(dates.d5)
    d.append(dates.d6)
    d.append(dates.d7)
    
    p.append(prices.p1)
    p.append(prices.p2)
    p.append(prices.p3)
    p.append(prices.p4)
    p.append(prices.p5)
    p.append(prices.p6)
    p.append(prices.p7)
    
    val=check(d)
    
    my_dict=[]
    # cur=official.currency
    
    val=check(d)
    
    # if cur is None:
    cur="₹"
    
    if(val<=2):
        return render_template("message.html",id=id,message=f"You need to track {3-val} times more to get Advanced Analysis",type="danger",head="LessTrack")
    else:
        my_dict=[]
        for i in range(0,val):
            dict={'date':d[i],'price':p[i]}
            my_dict.append(dict)
        my_dict.sort(key=lambda x:datetime.strptime(x['date'],"%d/%m/%Y"))
        await plot(my_dict,cur)
        return render_template("message.html",id=id,message="Return to the activity page",type="success",head="Success")
        
    
    
        
if __name__=="__main__":
    # this opens the server in debugging and self-restarting mode
    # here we set up the secret key for our server  
    

    app.run(debug=True)

