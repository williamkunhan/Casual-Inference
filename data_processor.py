import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
from scipy import stats
from matplotlib import style
import seaborn as sns
from matplotlib import pyplot as plt
import statsmodels.formula.api as smf
import graphviz as gr
from linearmodels.iv import IV2SLS

pd.set_option("display.max_columns", 5)
style.use("fivethirtyeight")

def get_dataset():
    data = pd.read_csv("../Casual-Inference/data/income_data/train.csv")
    data = data.dropna(axis=0)
    data.rename(columns={'educational-num': 'educational_num', "income_>50K": "income_bigger_than_50K",
                         'marital-status': 'marital_status', 'native-country': 'native_country'}, inplace=True)
    data["race"] = data["race"].replace(to_replace="Amer-Indian-Eskimo",
                                        value="Indian")
    data["race"] = data["race"].replace(to_replace="Asian-Pac-Islander",
                                        value="Asian")
    occupationDict = {
        "Exec-managerial": 0,
        "Other-service": 1,
        "Transport-moving": 2,
        "Adm-clerical": 2,
        "Machine-op-inspct": 2,
        "Sales": 2,
        "Handlers-cleaners": 2,
        "Farming-fishing": 2,
        "Protective-serv": 2,
        "Prof-specialty": 1,
        "Craft-repair": 0,
        "Tech-support": 2,
        "Priv-house-serv": 2,
        "Armed-Forces": 2
    }
    raceDict = {
        "White": 0,
        "Black": 1,
        "Asian": 2,
        "Indian": 2,
        "Other": 2
    }
    educationDict = {
        'Doctorate': 1,
        '12th': 0,
        'Bachelors': 1,
        '7th-8th': 0,
        'Some-college': 1,
        'HS-grad': 0,
        '9th': 0,
        '10th': 0,
        '11th': 0,
        'Masters': 1,
        'Preschool': 0,
        '5th-6th': 0,
        'Prof-school': 0,
        'Assoc-voc': 0,
        'Assoc-acdm': 0,
        '1st-4th': 0
    }
    genderDict = {
        "Male": 0,
        "Female": 1
    }
    maritalDict = {
        "Divorced": 2,
        "Never-married": 1,
        "Married-civ-spouse": 0,
        "Widowed": 2,
        "Separated": 2,
        "Married-spouse-absent": 2,
        "Married-AF-spouse": 2
    }
    workclassDict = {
        'Private': 0,
        'State-gov': 1,
        'Self-emp-not-inc': 2,
        'Federal-gov': 1,
        'Local-gov': 1,
        'Self-emp-inc': 1,
        'Without-pay': 1
    }

    def map_relationship(relationship):
        if relationship == "Husband":
            return 0
        if relationship == "Not-in-family":
            return 1
        else:
            return 2

    def map_country(native_country):
        if native_country == "United-States":
            return 0
        else:
            return 1

    data["occupation"] = data["occupation"].map(occupationDict)
    data["race"] = data["race"].map(raceDict)
    data["gender"] = data["gender"].map(genderDict)
    data["marital_status"] = data["marital_status"].map(maritalDict)
    data["native_country"] = data["native_country"].map(map_country)
    data["workclass"] = data["workclass"].map(workclassDict)
    data["education"] = data["education"].map(educationDict)
    data["relationship"] = data["relationship"].map(map_relationship)
    data.to_csv("modified_train.csv")
    return data

def get_dataset_by_age():
    data = pd.read_csv("../Casual-Inference/data/income_data/modified_train.csv")
    p = data["education"]
    x = data[[
        "workclass", "fnlwgt", "marital_status", "occupation", "relationship", "race", "gender", "capital-gain", "capital-loss", "hours-per-week", "native_country"]]
    z = data["age"]
    y = data["income_bigger_than_50K"]
    return z, x, p, y

def get_dataset_by_race():
    data = pd.read_csv("../Casual-Inference/data/income_data/modified_train.csv")
    p = data["education"]
    x = data[
        "workclass", "fnlwgt", "marital_status", "occupation", "relationship", "age", "gender", "capital-gain", "capital-loss", "hours-per-week", "native_country"]
    z = data["race"]
    y = data["income_bigger_than_50K"]
    return z, x, p, y

if __name__ == '__main__':
    z, x, p, y = get_dataset_by_age()
    print(z, x, p, y)