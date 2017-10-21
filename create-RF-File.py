import pandas as pd 
import numpy as np
import csv
from sklearn.ensemble import RandomForestClassifier
import pickle
#complications_testing: Defined to be 30% of the complications data.
#no_complications_testing: The rest of the testing data - which is the other 70%.
#complications_training: The training data with complications.
#no_complications_training: The training data with no complications.
#I'm just grabbing the first 500 data points to make sure the program works as we want, we'll take this away when we want to try it out will the whole set.
sample = 500
df = pd.read_csv('./data/NIS_2008_2014_converted.csv', nrows = sample)
df = df.sample(frac=1)
del df["RACE"]
#df = df[df['SEX']!=' ']
#df = df[df['AGE']!=' ']
#df.drop(df.columns[[0]], axis=1)
#del df["PID"]
del df["LOS"]
del df["YEAR"]
del df["SEX"]
del df["AGE"]
# del df["46"]
# del df["47"]
del df["650"]
del df["651"]
del df["652"]
del df["653"]
del df["654"]
del df["655"]
del df["656"]
del df["657"]
del df["658"]
del df["659"]
del df["662"]
del df["670"]

print(df)
print(df.columns.values)

# for i in range(650,670):
#     del(df[str(i)])

for i in range(164,197):
   del(df[str(i)])

for i in range(213,224):
   del(df[str(i)])
df = df.reset_index(drop=True)

complications = pd.DataFrame(columns = list(df.columns.values))
no_complications = pd.DataFrame(columns = list(df.columns.values))
complications_testing = pd.DataFrame(columns = list(df.columns.values))
complications_training = pd.DataFrame(columns = list(df.columns.values))
no_complications_testing = pd.DataFrame(columns = list(df.columns.values))
no_complications_training = pd.DataFrame(columns = list(df.columns.values))

for i in range(len(df)):
    if df['Complications'][i] == 1:
        tempdf = pd.DataFrame(df.iloc[[i]], columns = list(df.columns.values))
        complications = complications.append(tempdf, ignore_index = True)
    elif df['Complications'][i] == 0:
        tempdf = pd.DataFrame(df.iloc[[i]], columns = list(df.columns.values))
        no_complications = no_complications.append(tempdf, ignore_index = True)

percent_testing = .3
number_complications_testing = round(percent_testing*len(complications))
number_no_complications_testing = round((1-percent_testing)*number_complications_testing/percent_testing)

x = 0
while (x<number_complications_testing):
    tempdf = pd.DataFrame(complications.iloc[[0]], columns = list(df.columns.values))
    complications_testing = complications_testing.append(tempdf, ignore_index = True)
    complications.drop(0, inplace=True)
    complications = complications.reset_index(drop=True)
    x = x + 1;

x = 0
while (x<number_no_complications_testing):
    tempdf = pd.DataFrame(no_complications.iloc[[0]], columns = list(df.columns.values))
    no_complications_testing = no_complications_testing.append(tempdf, ignore_index = True)
    no_complications.drop(0, inplace=True)
    no_complications = no_complications.reset_index(drop=True)
    x = x + 1;

complications_training = complications
no_complications_training = no_complications

testing = pd.DataFrame(columns = list(df.columns.values))
testing = testing.append(complications_testing, ignore_index = True)
testing = testing.append(no_complications_testing, ignore_index = True)

c = len(complications_training)
nc = len(no_complications_training)

number_of_trails = int(nc/c)

RF_loop_results = []
RFS = []
#This loops through all training data of all complcaitions and a fraction of no_complcations such that there is 50/50 in each RF.
#for i in range(number_of_trails):
for i in range(number_of_trails):
    currentTraining = pd.DataFrame(columns = list(df.columns.values))
    currentTraining = currentTraining.append(complications_training, ignore_index = True)
    currentTraining = currentTraining.append(no_complications_training[0:len(complications_training)], ignore_index = True)
    no_complications_training = no_complications_training.iloc[len(complications_training):]
    no_complications_training = no_complications_training.reset_index(drop=True)

    y = currentTraining["Complications"]
    y = y.values.astype(int)

    features = currentTraining.columns[1:262]
    X = currentTraining[features].as_matrix().astype(int)

    clf = RandomForestClassifier(n_jobs=2, oob_score = True, random_state = 42, n_estimators = 250)
    clf.fit(X, y)
    RFS.append(clf)

    RF_loop_results.append(clf.predict(testing[features]))

#Exporting Random Forest Array
pickle.dump(RFS, open('RF-array.sav', 'wb'))