import pandas as pd
import numpy as np
class Data():
    def get_code(self, column, key):
        re = self.df[column].astype('category')
        return re.cat.categories.get_loc(key)
    
    def convert_data(self, age, gender, education, jobTitle, experience):
        try:
            age = float(age)
        except:
            age = None
        try:
            gender = self.get_code('Gender', gender)
            gender = float(gender)
        except:
            gender = None
        try:
            education = self.get_code('Education Level', education)
            education = float(education)
        except:
            education = None
        try:
            jobTitle = self.get_code('Job Title', jobTitle)
            jobTitle = float(jobTitle)
        except:
            jobTitle = None
        try:
            experience = float(experience)
        except:
            experience = None
        return age, gender, education, jobTitle, experience

    def __init__(self):
        self.df = pd.read_csv('./data/Salary Data.csv')
        self.x = self.df.drop(columns=['Salary'])
        self.y = self.df['Salary']
        self.x['Gender'] = self.x['Gender'].astype('category')
        self.x['Gender'] = self.x['Gender'].cat.codes

        self.x['Education Level'] = self.x['Education Level'].astype('category')
        self.x['Education Level'] = self.x['Education Level'].cat.codes

        self.x['Job Title'] = self.x['Job Title'].astype('category')
        self.x['Job Title'] = self.x['Job Title'].cat.codes

        self.x = np.array(self.x)
        self.y = np.array(self.y)