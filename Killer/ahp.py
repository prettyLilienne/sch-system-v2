import numpy as np #use for real number
import skfuzzy as fuzz #similar grading sa manu, has centroid function

from flask import Flask, render_template 
from flask import Flask, redirect, request
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/scholarship_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Scholarship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text) 
    amount = db.Column(db.Float, nullable=False) # Monetary val
    slots = db.Column(db.Integer, nullable=False) # Number of students it can accept
    deadline = db.Column(db.Date, nullable=False)
    status = db.Column (db.Text, nullable=False)

with app.app_context():
    db.create_all()
with app.app_context():
    if Scholarship.query.count()==0:
        s1 = Scholarship (
            name = "TSU Excellence Scholarship",
            description = "For student with outstandng Academic Performance",
            amount = "50000",
            slots="20",
            deadline = "2024-03-15",
            status = "active"
            )
        db.session.add(s1)
        db.session.commit()

class Applications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    date = db.Column(db.Date, nullable=False) 
    
    status = db.Column(db.Text, nullable=False, default="pending")
    recomended_scolarship= db.Column(db.Text, nullable=True)
    suitability_score = db.Column(db.Integer, nullable=True,)

with app.app_context():
    db.create_all()

@app.route('/fake_data')
def f_data():
    app1=Applications(
        name="Wanda Maximoff",
        date="2022-01-13",
        status="pending"
    )
    app2=Applications(
        name="Chris Evans",
        date="2023-03-17",
        status="pending"
    )
    app3=Applications(
        name="Tony Stark",
        date="2025-07-30",
        status="pending"
    )
    db.session.add_all([app1,app2,app3])
    db.session.commit()
    return redirect('/')

@app.route('/admin/applications')
def admin_app():
    pending_apps = Applications.query.filter_by(status='pending').all()
    eval_apps=Applications.query.filter_by(status='evaluated').all()    
    total_apps = Applications.query.count()
    pending_count= Applications.query.filter_by(status='pending').count()
    approved_count= Applications.query.filter_by(status='accepted').count()
    rejected_count=Applications.query.filter_by(status='rejected').count()
    evaluated_count=Applications.query.filter_by(status='evaluated').count()
    scholarships = Scholarship.query.all()
    total_scho = Scholarship.query.count()
    return render_template ('in.html', pending=pending_apps, evaluated=eval_apps,
    total_apps=total_apps, pending_count=pending_count, approved_count=approved_count,
    rejected_count=rejected_count, total_scho=total_scho, evaluated_count=evaluated_count)

@app.route('/admin/applications')
def apps ():
    pending_apps = Applications.query.filter_by(status='pending').all()
    eval_apps=Applications.query.filter_by(status='evaluated').all()
    return render_template('in.html', pending=pending_apps,evaluated=eval_apps)

@app.route('/evaluate/<int:id>', methods = ['POST'])
def evaluated(id):
    app=Applications.query.get_or_404(id)

    app.suitablity_score=request.form.get('score')
    app.recommended_scholarship=request.form.get('scholarship')
    app.status='evaluated'

    db.session.commit()

    return redirect('/')

@app.route('/decision/<int:id>/<action>')
def decision (id,action):
    app = Applications.query.get_or_404(id)

    if action == 'accept':
        app.status='accepted'
    elif action=='reject':
        app.status='rejected'

    db.session.commit()
    return redirect('/')


@app.route('/')
def index ():
    scholarships = Scholarship.query.all()
    print(type(scholarships))
    return render_template ('in.html', scholarships=scholarships)

@app.route('/add_scholarship', methods=['POST'])
def add_scholarship():
    name = request.form['name']
    description = request.form['description']
    amount =int(request.form['amount'])
    slots = int (request.form['slots'])
    deadlinestr = request.form['deadline']
    deadline = datetime.strptime(deadlinestr, '%Y-%m-%d').date()
    status = request.form['status']

    new_scholarship = Scholarship(
        name=name,
        description=description,
        amount=amount,
        slots=slots,
        deadline=deadline,
        status=status 
    )
    db.session.add(new_scholarship)  
    db.session.commit()

    return redirect('/') 

@app.route('/delete/<int:id>', methods=['POST'])
def delete_scholarship(id): 
    scholarships = Scholarship.query.get_or_404(id)
    db.session.delete(scholarships) 
    db.session.commit()
    return redirect ('/')  


#Pre-fills
@app.route('/update/<int:id>', methods=['POST'])
def update_scholarship(id):
    scholarships = Scholarship.query.get_or_404(id)

    scholarships.name = request.form["name"]
    scholarships.descriptionn = request.form["description"]
    scholarships.amount = request.form["amount"]
    scholarships.slots= request.form["slots"]
    scholarships.deadline=request.form["deadline"]
    scholarships.status=request.form["status"]

    db.session.commit()

    return redirect ('/')


if __name__=="__main__":
    app.run(debug=True)

#studInfo = {} #creates an empty dictionary to store data
              # so when a certain method calls, certain info will be stored

"""
studInfo["gwa"] = float(input("Enter your grade: "))
studInfo["income"] = float(input ("Enter annual income:"))
pwd = (input ("are you a pwd?(yes or no)")).lower()
studInfo["pwd"]=1 if pwd=="yes" else 0
studInfo["awards"] =float(input("Number or awards: "))

print( studInfo)
#shows the fixed criteria in each scholarship type
scholarship = {
    "Merit": {
        "GWA": 0.5,
        "Income": 0.2,
        "PWD": 0.1,
        "Awards": 0.2
    },
    "Financal Assisstance":{
        "GWA": 0.2,
        "Income": 0.5,
        "PWD": 0.2,
        "Awards": 0.1
    },
      "Athelic":{
        "GWA": 0.3,
        "Income": 0.1,
        "PWD": 0.1,
        "Awards": 0.5
    }
}
#normalize values - i ont get thi
def normGwa(gwa: float, min_gwa=1.0, max_gwa=5.0):
    return  (max_gwa - gwa)/(max_gwa-min_gwa)   
def normInc(income: float, max_income=100000):
    return 1 - (income/max_income)  
def normAwa(awards: float, max_awards=10):
    return awards/max_awards
def normpwd(pwd):
    return pwd


#how to grade the students, or we can add else if, TFN
x = np.arange(0,1.01,0.01) #minimun to maximum requirements

#low_gwa = fuzz.trimf(x,[ 0.2,0.4,0.6])
#ave_gwa = fuzz.trimf(x, [0.6,0.8,1.0])
#exe_gwa = fuzz.trimf(x, [0.8,1.0,1.0])

#low_inc = fuzz.trimf(x, [0.2,0.4,0.6])
#ave_inc = fuzz.trimf(x, [0.6,0.8,1.0])
#exe_inc = fuzz.trimf(x, [0.8,1.0,1.0])

#pwd_no = fuzz.trimf(x, [0,0,0])
#pwd_yes = fuzz.trimf(x, [0.8,1.0,1.0])

#x_awa = np.linspace(0,1,101)
#low_awa = fuzz.trimf(x_awa, [0.2,0.4,0.6])
#ave_awa = fuzz.trimf(x_awa, [0.6,0.8,1.0])
#exe_awa = fuzz.trimf(x_awa, [0.8,1.0,1.0])
#another  method, enumerating the TFN
tfn_gwa = { 
    "Low": (0.2,0.4,0.6),
    "Average": (0.6,0.8,1.0),
    "Execellent": (0.8, 1.0,1.0)
}
tfn_inc = {
    "Low": (0.2,0.4,0.6),
    "Average": (0.6,0.8,1.0),
    "Execellent": (0.8, 1.0,1.0)
}
tfn_awa = { #dk the explanation why awa has diff tfn
    "Low": (0.0,0.33, 0.66),
    "Average": (0.33,0.5,0.66),
    "Execellent": (0.66, 0.83,1.0)
}
tfn_pwd = {
    "No": (0.0,0.0,0.0),
    "Average": (0.8,1.0,1.0),
    
}

def fuzzification(value,tfn_dict): #calls the empty dictionary 
    #f = {} #create empty dictionary
    #g = studInfo["gwa"]
    # interp.membership find the degree of membership for a specific value 
    # in the fuzzy set
    memberships={} # empty dictionary
    for key, (l,m,u) in tfn_dict.items():
        mf = fuzz.trimf(x,[l,m,u]) #trimf is a triangular membership function generation
        memberships[key]=fuzz.interp_membership(x,mf,value)
    return memberships


#deffuzification
#def def_mem(memberships):#
 #   return max(memberships.values())
def def_tfn(memberships,tfn_dict):
    if not memberships:
        return 0
    best_cat = max (memberships, key=memberships.get)
    l,m,u = tfn_dict[best_cat]
    return (l + m + u)/3

#normalization
gwa_norm = normGwa(studInfo["gwa"])
inc_norm = normInc(studInfo["income"])
awa_norm = normAwa(studInfo["awards"])
pwd_norm = normpwd(studInfo["pwd"])
print( gwa_norm,inc_norm,awa_norm,pwd_norm)

#fuzzification
gwa_fuzzy = fuzzification(gwa_norm, tfn_gwa)
income_fuzzy = fuzzification(inc_norm, tfn_inc)
awa_fuzzy = fuzzification(awa_norm, tfn_awa)
pwd_fuzzy = fuzzification(pwd_norm, tfn_pwd)
print(gwa_fuzzy,income_fuzzy,awa_fuzzy,pwd_fuzzy)

#dufuzzy
gwa_score = def_tfn(gwa_fuzzy, tfn_gwa)
inc_score = def_tfn(income_fuzzy,tfn_inc)
awa_score = def_tfn(awa_fuzzy, tfn_awa)
pwd_score = def_tfn(pwd_fuzzy,tfn_pwd)
print(gwa_score,inc_score,awa_score,pwd_score)
#suitability score #let stop here
total_score = {}
for sch, weights in scholarship.items():
    total_score[sch] = round(
        gwa_score*weights["GWA"] + 
        inc_score*weights["Income"] +
        awa_score*weights["Awards"] +
        pwd_score*weights["PWD"], 4
   ) #make the scores in percentage
    
#ranking
ranking = sorted (total_score.items(), key=lambda x:x[1], 
                  reverse=True) 
#studInfo["total_score"]= total_score 
#studInfo["ranking"] = ranking
#print("\nScholarships Total Scores: ")
#for sch ,score in total_score.items():
#    print(f"{sch}: {score}")
print("\nranking:")
for i,(sch,score) in enumerate(ranking,1):
    print(f"{i}.{sch}(Score:{score})")
                  
"""



