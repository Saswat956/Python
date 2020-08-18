import numpy as np
import pandas as pd
import pylab
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 8})
    
df = pd.read_csv("titanic_dataset.csv")
df = df.drop(["name","ticket","cabin","home.dest","body","boat"],axis=1)
#~ print df.head()
#~ print df.describe()
#~ print df.info()

classType = np.array(["C1","C2","C3"])
survive = np.array(["0-Survive","1-Survive"])
genderType = np.array(["Male","Female"])
parch = np.array([0,1,2,3,4,5,6,9])
embarked = np.array(["CB","SQ","SH"])

cnt_by_class = np.array(df.pclass.value_counts().sort_index()) # [Class1,Class2,Class3]
cnt_of_pass_by_survival = np.array(df.survived.value_counts().sort_index()) # [Notsurvived,Survived]
cnt_of_pass_by_gender = np.array(df.Gender.value_counts()) # [Male,Female]
age_list = np.array(df.age.replace(np.nan,np.mean(df.age)))
parch_list = np.array(df.parch.value_counts().sort_index()) # [0,1,2,3,4,5,6,9]
fare = np.array(df.fare.replace(np.nan,np.mean(df.fare)))
cnt_of_emb_by_city = np.array(df.embarked.value_counts().sort_index()) # [C = Cherbourg, Q = Queenstown, S = Southampton]

embarked_C_survive_data = np.array(df.groupby(["embarked"]).get_group("C").survived.value_counts().sort_index())
embarked_S_survive_data = np.array(df.groupby(["embarked"]).get_group("S").survived.value_counts().sort_index())
embarked_Q_survive_data = np.array(df.groupby(["embarked"]).get_group("Q").survived.value_counts().sort_index())
#~ print embarked_C_survive_data
#~ print embarked_S_survive_data
#~ print embarked_Q_survive_data

age_survive_data = df.groupby(["survived"]).get_group(1)
age_Notsurvive_data = df.groupby(["survived"]).get_group(0)
#~ print age_survive_data.survived

width = .5
color = ["y","m","b","g","r","c","k","w"]

plt.subplot(3,4,1)
plt.tight_layout()
plt.bar(classType,cnt_by_class,color=color,width=width)
for i in range(len(classType)):
    plt.text(classType[i],cnt_by_class[i]+.5,cnt_by_class[i])
plt.title("Count by classType")

plt.subplot(3,4,2)
plt.bar(survive,cnt_of_pass_by_survival,color=color,width=width)
for i in range(len(survive)):
    plt.text(survive[i],cnt_of_pass_by_survival[i]+.5,cnt_of_pass_by_survival[i])
plt.title("Count by Survival")

plt.subplot(3,4,3)
plt.bar(genderType,cnt_of_pass_by_gender,color=color,width=width)
for i in range(len(genderType)):
    plt.text(genderType[i],cnt_of_pass_by_gender[i]+.5,cnt_of_pass_by_gender[i])
plt.title("Count by Gender")

plt.subplot(3,4,4)
plt.bar(parch,parch_list,width=width,color=color)
for i in range(len(parch)):
    plt.text(parch[i],parch_list[i]+.5,parch_list[i])
plt.title("Count by Parch")

plt.subplot(3,4,5)
plt.bar(embarked,cnt_of_emb_by_city,color=color,width=width)
for i in range(len(embarked)):
    plt.text(parch[i],cnt_of_emb_by_city[i]+.5,cnt_of_emb_by_city[i])
plt.title("Count by Embarkation")

plt.subplot(3,4,6)
plt.hist(age_list,bins=np.linspace(10,80,50),align="mid",rwidth=.8)
plt.title("Age distribution")

plt.subplot(3,4,7)
plt.scatter(age_survive_data.survived,age_survive_data.age,alpha=.1,s=np.pi*2**2)
plt.scatter(age_Notsurvive_data.survived,age_Notsurvive_data.age,alpha=.1,s=np.pi*2**2) # ## here the plot has to be transparent so we need to pic low alpha value
plt.title("Count by Age+Survival")


plt.subplot(3,4,8)
for cnt in range(3):
    if embarked[cnt] == "CB":
        plt.bar(embarked[cnt],embarked_C_survive_data[0],color=color[0],width=width,label="Survived==0")
        plt.text(embarked[cnt],embarked_C_survive_data[0]-50,embarked_C_survive_data[0]) # adding text to some x,y position
        plt.bar(embarked[cnt],embarked_C_survive_data[1],bottom=embarked_C_survive_data[0],color=color[1],width=width,label="Survived==1")
        plt.text(embarked[cnt],embarked_C_survive_data[0]+embarked_C_survive_data[1]+5,embarked_C_survive_data[1]) # adding text to some x,y position
    if embarked[cnt] == "SQ":
        plt.bar(embarked[cnt],embarked_Q_survive_data[0],color=color[0],width=width)
        plt.text(embarked[cnt],embarked_Q_survive_data[0]-50,embarked_Q_survive_data[0]) # adding text to some x,y position
        plt.bar(embarked[cnt],embarked_Q_survive_data[1],bottom=embarked_Q_survive_data[0],color=color[1],width=width)
        plt.text(embarked[cnt],embarked_Q_survive_data[0]+embarked_Q_survive_data[1]+5,embarked_Q_survive_data[1]) # adding text to some x,y position
    if embarked[cnt] == "SH":
        plt.bar(embarked[cnt],embarked_S_survive_data[0],color=color[0],width=width)
        plt.text(embarked[cnt],embarked_S_survive_data[0]-50,embarked_S_survive_data[0]) # adding text to some x,y position
        plt.bar(embarked[cnt],embarked_S_survive_data[1],bottom=embarked_S_survive_data[0],color=color[1],width=width)
        plt.text(embarked[cnt],embarked_S_survive_data[0]+embarked_S_survive_data[1]+5,embarked_S_survive_data[1]) # adding text to some x,y position
plt.title("Count by Embarked+Survival")
plt.legend()

plt.subplot(3,4,9)
for x in ("C","Q","S"):
    a = df.pclass[df.embarked==x].value_counts().sort_index().iloc[0] # ix for integer and label and iloc are integer only
    #~ print a
    b = df.pclass[df.embarked==x].value_counts().sort_index().iloc[1]
    #~ print b
    c = df.pclass[df.embarked==x].value_counts().sort_index().iloc[2]
    #~ print c
    plt.bar(x,a,color=color[0])
    plt.bar(x,b,bottom=a,color=color[1])
    plt.bar(x,c,bottom=b,color=color[2])
plt.legend(("C1","C2","C3"))    
plt.title("pclass wrt Embarkation")

plt.subplot(3,4,10)
for x in range(2):
    df.age[df.survived==x].plot(kind="kde")
plt.legend(("0-NotSurvive","1-Survived"))
plt.title("Survive wrt Age")

plt.subplot(3,4,11)
for x in range(1,4):
    df.age[df.pclass==x].plot(kind="kde")
plt.legend(("1st","2nd","3rd"))
plt.title("Age wrt Pclass")

plt.subplot(3,4,12)
for x in ("C","Q","S"):
    df.fare[df.embarked==x].plot(kind="line")
plt.legend(("C","Q","S"))
plt.title("Fare wrt Embarked")

plt.show()