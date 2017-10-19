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
sample = 5000
df = pd.read_csv('./data/NIS_2014_converted2.csv', nrows = sample)
df = df.sample(frac=1)
del df["RACE"]
df.drop(df.columns[[0]], axis=1)
#df = df[df['SEX']!=' ']
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

    RF_loop_results.append(clf.predict(testing[features]))
    print(clf.feature_importances_)

#Finding the majority voting
results = []

for i in range(len(RF_loop_results[0])):
    num = 0

    for j in range(len(RF_loop_results)):
        num = num + RF_loop_results[j][i]

    results.append(int(round(num/len(RF_loop_results))))

#The result of our multiple RFs
print("What our method predeicts is true:")
print(results)

print("-----------------------------------------------------------------------------")
#The actual answers
print("What is actually true:")
print(testing["Complications"].values)

print("-----------------------------------------------------------------------------")

number_complications_correctly_predicted = 0
for i in range(number_complications_testing):
    if results[i] == 1.0:
        number_complications_correctly_predicted = number_complications_correctly_predicted + 1

print("Percent of correct complication predictions:")
print(number_complications_correctly_predicted/number_complications_testing)

number_no_complications_correctly_predicted = 0
for i in range(number_complications_testing, len(testing)):
    if results[i] == 0.0:
        number_no_complications_correctly_predicted = number_no_complications_correctly_predicted + 1

print("Percent of correct no complication predictions:")
print(number_no_complications_correctly_predicted/(len(testing)-number_complications_testing))