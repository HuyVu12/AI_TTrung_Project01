from flask import Flask, render_template, request
from model.model01 import *
from Data import *
from sklearn.linear_model import LinearRegression

import pandas as pd
import numpy as np

app = Flask(__name__)

data = Data()   

def run_model(age, gender, education, jobTitle, experience):
    # Prepare data
    df = data.df.copy()
    
    df['Gender'] = df['Gender'].astype('category')
    df['Gender'] = df['Gender'].cat.codes

    df['Education Level'] = df['Education Level'].astype('category')
    df['Education Level'] = df['Education Level'].cat.codes

    df['Job Title'] = df['Job Title'].astype('category')
    df['Job Title'] = df['Job Title'].cat.codes
    x = df.drop(columns=['Salary'])

    if(age == None): x = x.drop(columns=['Age'])
    if(gender == None): x = x.drop(columns=['Gender']).astype('category')
    if(education == None): x = x.drop(columns=['Education Level']).astype('category')
    if(jobTitle == None): x = x.drop(columns=['Job Title']).astype('category')
    if(experience == None): x = x.drop(columns=['Years of Experience'])
    y = data.df['Salary']
    x = np.array(x)
    y = np.array(y)

    val = []
    for i in [age, gender, education, jobTitle, experience]:
        if i != None:
            val.append(i)
    # Model 01 Calculate
    model01 = calc_model(x, y)
    predict_01 = model01[-1]

    for i in range(len(model01)-1):
        predict_01 += model01[i] * val[i]
    
    # Model 02 Calculate
    model02 = LinearRegression()
    model02.fit(x, y)
    print("Model01:", model01)
    print("Model02:", model02.coef_)

    predict_02 = model02.predict(np.array(val).reshape(1, len(val)))

    predict_01 = int(predict_01)
    predict_02 = int(predict_02[0])

    if predict_01 < 0: predict_01 = 0
    if predict_02 < 0: predict_02 = 0
    
    return [predict_01, predict_02]

def create_message(icon = "success", title = "Thông báo", text = "Thông báo"):
    return {
        'icon': icon,
        'title': title,
        'text': text
    }

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template(
            'index.html',
            job_titles = sorted(list(set(data.df['Job Title']))), 
            edus = set(data.df['Education Level']),
            gender = set(data.df['Gender'])
        )
    elif request.method == 'POST':
        age = request.form.get('age')
        gender = request.form.get('gender')
        education = request.form.get('education')
        jobTitle = request.form.get('jobTitle')
        experience = request.form.get('experience')
        age, gender, education, jobTitle, experience = data.convert_data(age, gender, education, jobTitle, experience)
        print(age, gender, education, jobTitle, experience)
        message = {}
        try:
            if age is None and gender is None and education is None and jobTitle is None and experience is None:
                message = create_message('information', text="Bạn phải nhập ít nhất một thông tin!")
                return render_template(
                    'index.html',
                    job_titles = sorted(list(set(data.df['Job Title']))), 
                    edus = set(data.df['Education Level']),
                    gender = set(data.df['Gender']),
                    message = message
                )
            if age is not None and age < 0:
                message = create_message('error', text='Bạn không phải người âm hãy nhập lại tuổi')
                return render_template(
                    'index.html',
                    job_titles = sorted(list(set(data.df['Job Title']))), 
                    edus = set(data.df['Education Level']),
                    gender = set(data.df['Gender']),
                    message = message
                )
            if experience is not None and experience < 0:
                message = create_message('error', text='Số năm trải đời không thể âm. Hãy nhập lại!')
                return render_template(
                    'index.html',
                    job_titles = sorted(list(set(data.df['Job Title']))), 
                    edus = set(data.df['Education Level']),
                    gender = set(data.df['Gender']),
                    message = message
                )
            if experience is not None and age is not None and experience > age:
                message = create_message('error', text='Số kinh nghiệm không thể nhỏ hơn số tuổi!')
                return render_template(
                    'index.html',
                    job_titles = sorted(list(set(data.df['Job Title']))), 
                    edus = set(data.df['Education Level']),
                    gender = set(data.df['Gender']),
                    message = message
                )
            py = run_model(age, gender, education, jobTitle, experience)
            message = create_message(text="Xử lí thành công.")
            return render_template(
                    'result.html',
                    message = message,
                    p01 = py[0], 
                    p02 = py[1]
                )
        except:
            message = create_message("error", "Thông báo", text="Lỗi khi dự đoán hãy thử lại sau.")
@app.route('/result')
def result():
    message = {}
    return render_template('result.html', message)


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
    # print('Testing')
 