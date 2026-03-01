import numpy as np #use for real number
import skfuzzy as fuzz #similar grading sa manu, has centroid function

studInfo = {} #creates an empty dictionary to store data
              # so when a certain method calls, certain info will be stored


studInfo["gwa"] = float(input("Enter your grade: "))
studInfo["income"] = float(input ("Enter annual income:"))
pwd = (input ("are you a pwd?(yes or no)")).lower()
studInfo["pwd"]=1 if pwd=="yes" else 0
#studInfo["awards"] =float(input("Number or awards: "))
indigent = (input("are you part of indigent people? ")).lower()
studInfo["indigent"] =1 if indigent=="yes" else 0
ip = (input("are you part of ip community? ")).lower()
studInfo["indigent2"] =1 if ip=="yes" else 0
#ip = (input("are you part of ip community? ")).lower()
#studInfo["ip"] =1 if ip=="yes" else 0

#print( studInfo)
#shows the fixed criteria in each scholarship type
scholarship = {
    "PFCIFIC": {
        "IP": 0.5,
        "PWD": 0.3,
        "INDIGENT": 0.2
    },
    "ASLAG":{
        "GWA": 0.6,
        "IP": 0.25,
        "Income": 0.15,
    },
      "DFPSEAP":{
        "GWA": 0.7,
        "Income": 0.3,
    }
}
def normGwa(gwa: float, min_gwa=1.0, max_gwa=5.0):
    return  (max_gwa - gwa)/(max_gwa - min_gwa)   
def normInc(income: float, max_income=100000):
    return 1 - (income/max_income)  
#def normAwa(awards: float, max_awards=10):
 #   return awards/max_awards
def normpwd(pwd):
    return pwd
def normind(indigent):
    return indigent
def normip(ip):
    return ip


#fuzzifiation #wrong logic huh
def tfnGwa (gwa_norm):
    if gwa_norm == 1:
        return (0.8,1.0,1.0) #excelent 1.0 
    elif gwa_norm >=0.8125 and gwa_norm<1:
        return (0.6,0.8,1.0) #very good  1.25 - 1.5
    elif gwa_norm>=0.625 and gwa_norm <0.8125:
        return (0.4,0.6,0.8) #good 1. 75-2.0
    else:
        return (0.2,0.4,0.6)#bad - 2.5 - 3.0
def tfnInc (inc_norm):
    if inc_norm >=0.95 and inc_norm<=1 :
        return (0.8,1.0,1.0) #5000 
    elif inc_norm >=0.85 and inc_norm<0.95:
        return (0.6,0.8,1.0) #10000
    elif inc_norm>=0.8 and inc_norm < 0.85:
        return (0.4,0.6,0.8)
    else:
        return (0.2,0.4,0.6)
#def tfnAwa (awa_norm):
#    if awa_norm >=0.75:
#        return (0.8,1.0,1.0)
 #   elif awa_norm >=0.5:
 #       return (0.6,0.8,1.0)
 #   elif awa_norm>=0.25:
 #       return (0.8,1.0,1.0)
 #   else:
 #       return (0.2,0.4,0.6)
def tfnPwd (pwd_norm):
    return (0.8,1.0,1.0) if pwd_norm == 1 else (0.0,0.0,0.0) #0000, or 1.0,1.0,1.0
def tfnInd (ind_norm):
    return (0.8,1.0,1.0) if ind_norm == 1 else (0.0,0.0,0.0)
def tfnIp (ip_norm):
    return (0.8,1.0,1.0) if ip_norm == 1 else (0.0,0.0,0.0)


def deffuzzy(tfn):
    l,m,u = tfn
    return (l + m + u)/3
print(deffuzzy)
gwa_norm = normGwa(studInfo["gwa"])
inc_norm = normInc(studInfo["income"])
#awa_norm = normAwa(studInfo["awards"])
pwd_norm = normpwd(studInfo["pwd"])
ind_norm = normind(studInfo["indigent"])
ip_norm = normip(studInfo["indigent2"])
print(gwa_norm,inc_norm,ind_norm,ip_norm,pwd_norm)

scores = {
    "GWA": deffuzzy(tfnGwa(gwa_norm) ),
    "Income": deffuzzy(tfnInc(inc_norm) ),
    #"Awards": deffuzzy(tfnAwa(awa_norm) ),
    "PWD": deffuzzy(tfnPwd(pwd_norm) ),
    "INDIGENT": deffuzzy(tfnInd(ind_norm)),
    "IP": deffuzzy(tfnIp(ip_norm) ),

}
print(scores)
total_score = {}
#for sch, weights in scholarship.items():
#    total_score[sch] = round(
#        scores["GWA"]*weights["GWA"] + 
#        scores["Income"]*weights["Income"] +
#        scores["Awards"]*weights["Awards"] +
#        scores["PWD"]*weights["PWD"], 4
#   ) 
#i think the logic here is incorrect
#for sch, weights in scholarship.items():
#    total = 0
#    for crit, weight in weights.items():
#        total +=total_score[crit]*weight 
#    scholarship_scores = round(total,4)
def computeSS(scores,scholarship_weights):
    total = 0
    weightS = 0
    steps=[]
    for criterion,weight in scholarship_weights.items():
        if criterion in scores:
            total +=scores[criterion]*weight
            weightS +=weight
        else:
            print("Warning: {criterion} not found in scores")

    if weightS >0:
        return round(total/weightS,4)
    else:
        return 0

for sch, weights in scholarship.items():
     total_score[sch]=computeSS(scores,weights)

#scholarship_score = {}
#scholarship_steps = {}
#for sch,weights in scholarship.items():
  #  score, steps = computeSS(score,weights)
  #  scholarship_score[sch]=score
  #  scholarship_steps[sch]=steps



ranking = sorted (total_score.items(), key=lambda x:x[1], 
                  reverse=True) 
print("\nRanking: ")
for i, (sch,score) in enumerate(ranking,1):
    print(f"{i},{sch}-{score *100}")

#for sch in scholarship_score:
#    print(f"\n==={sch.upper()} SCHOLARSHIP ===")
#    for crit,crisp,weight,contrib in scholarship_steps[sch]:
#        print(f"{crit}:{crisp:.3f} * {weight:.2f} = {contrib:.4f}")
#    total_weight = sum (w for _,_,w,_ in scholarship_steps[sch])
#    print(f"Total Weight: {total_weight:.2f}")
#    print(f"Final Computaility Sc0re: {scholarship_score[sch]:.4f}" )