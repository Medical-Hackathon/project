## compute_input.py
import numpy as np
import sys, json, numpy as np
import pandas as pd 
import csv
from sklearn.ensemble import RandomForestClassifier
import pickle
from decimal import Decimal

#Read data from stdin
def read_in():
    lines = sys.stdin.readlines()
    #Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])

def predict(data):

    clf = pickle.load(open('RF-array (2).sav', 'rb'))

    columns = ['AGE','SEX','RACE','CM_AIDS','CM_ALCOHOL','CM_ARTH','CM_BLDLOSS','CM_CHF','CM_CHRNLUNG','CM_COAG','CM_DEPRESS','CM_DM','CM_DMCX','CM_DRUG','CM_HTN_C','CM_HYPOTHY','CM_LIVER','CM_LYMPH','CM_LYTES','CM_METS','CM_NEURO','CM_OBESE','CM_PARA','CM_PERIVASC','CM_PSYCH','CM_PULMCIRC','CM_RENLFAIL','CM_TUMOR','CM_ULCER','CM_VALVE','CM_WGHTLOSS','HCUP_ED','HOSP_BEDSIZE','HOSP_LOCTEACH','TOTAL_DISC','@1','@2','@3','@4','@5','@6','@7','@8','@9','@10','@11','@12','@13','@14','@15','@16','@17','@18','@19','@20','@21','@22','@23','@24','@25','@26','@27','@28','@29','@30','@31','@32','@33','@34','@35','@36','@37','@38','@39','@40','@41','@42','@43','@44','@45','@46','@47','@48','@49','@50','@51','@52','@53','@54','@55','@56','@57','@58','@59','@60','@61','@62','@63','@64','@76','@77','@78','@79','@80','@81','@82','@83','@84','@85','@86','@87','@88','@89','@90','@91','@92','@93','@94','@95','@96','@97','@98','@99','@100','@101','@102','@103','@104','@105','@106','@107','@108','@109','@110','@111','@112','@113','@114','@115','@116','@117','@118','@119','@120','@121','@122','@123','@124','@125','@126','@127','@128','@129','@130','@131','@132','@133','@134','@135','@136','@137','@138','@139','@140','@141','@142','@143','@144','@145','@146','@147','@148','@149','@151','@152','@153','@154','@155','@156','@157','@158','@159','@160','@161','@162','@163','@197','@198','@199','@200','@201','@202','@203','@204','@205','@206','@207','@208','@209','@210','@211','@212','@225','@226','@227','@228','@229','@230','@231','@232','@233','@234','@235','@236','@237','@239','@240','@241','@242','@243','@244','@245','@246','@247','@248','@249','@250','@251','@252','@253','@254','@255','@256','@257','@258','@259','@660','@661','@663']


    predictData = []

    for i in range(239):
        predictData.append(0)

    predictData[0] = data[0][0]
    predictData[1] = data[0][1]
    predictData[2] = data[0][2]
    predictData[31] = data[0][3]
    predictData[32] = data[0][4]
    predictData[33] = data[0][5]
    predictData[34] = data[0][6]

    for i in range(len(data[1])):
        for j in range(len(columns)):
            if (data[1][i]==columns[j]):
                predictData[j] = 1




    testing_point = pd.DataFrame(columns = columns)
    testing_point.loc[0] = predictData

    RF_loop_results = []
    probs = []
    probs_complications = []
    probs_no_complications = []

    for i in range(len(clf)):
        features = testing_point.columns

        RF_loop_results.append(clf[i].predict(testing_point[features]))
        probs.append(clf[i].predict_proba(testing_point[features]))

    results = []
    for i in range(len(RF_loop_results[0])):
        num = 0
        total_prob_complcaition = 0
        total_prob_no_complcaition = 0

        for j in range(len(RF_loop_results)):
            num = num + RF_loop_results[j][i]
            total_prob_complcaition = total_prob_complcaition + probs[j][0][1]
            total_prob_no_complcaition = total_prob_no_complcaition + probs[j][0][0]

        results.append(int(round(num/len(RF_loop_results))))
        results.append(float(round(Decimal(total_prob_no_complcaition/len(RF_loop_results)*100),2)))
        results.append(float(round(Decimal(total_prob_complcaition/len(RF_loop_results)*100),2)))


    return results

def main():
    #get our data as an array from read_in()
    data = read_in()

    result = predict(data)

    print(result)

#start process
if __name__ == '__main__':
    main()