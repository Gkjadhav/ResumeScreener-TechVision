from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import kaleido
import docx2txt
import plotly.express as px
import plotly.graph_objects as go
# import matplotlib.pyplot as plt
import pandas as pd
app = Flask(__name__)





@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')  
    else:
        resume = request.files['formFile']
        path="static/predictions_pic.svg"
        make_picture(resume,path)
        return render_template('Results.html',href=path)

@app.route("/Results") 
def Results():
    return render_template('Results.html')

@app.route("/about") 
def about():
    return render_template('about.html')

@app.route("/contact") 
def contact():
    return render_template('contact.html')

def make_picture(resume_file,output_file):
    resume = docx2txt.process(resume_file)
    # Create dictionary with Computer Engineering key terms by area

    job_description = {
    'Web Developement':['cookies','cache','html','css','javascript','wordpress','fullstack',
                        'git','github','devops','hypertext markup language','cascading style sheets','Bootstrap',
                        'backend','frontend''Responsive design', 'Semantic markup','SaaS','Server-side scripting',
                        'php','frameworks','Visual hierarchy','Infinite/parallax scrolling','API','deployment'],      
    'Machine learning':['python','pandas','keras','tensorflow','r programming','seaborn',
                        'opencv','matplotlib','visualization','graphs','bar chart','neural network',                             
                        'artificial intelligence','data science','supervised','unsupervised','semisupervised',
                        'safety','clustering','Association','numpy'],
    'Software Development':['java','c++','python','android development','web development','sql','dbms','nosql',
                            'api','application','browser','bug','cache','code','competative programming',
                            'deployment','debugging','oops','object','classes','datastructures','c',
                            ],
    'Data analytics':['analytics','api','aws','big data','busines intelligence','clustering','code',
                    'coding','data','database','data mining','data science','deep learning','hadoop',
                    'hypothesis test','iot','internet','machine learning','modeling','nosql','nlp',
                    'predictive','programming','python','r','sql','tableau','text mining',
                        'visualuzation']   }

    # Initializie score counters for each area
    web = 0
    machine = 0
    software = 0
    data = 0
    # Create an empty list where the scores will be stored
    scores = []
    # Obtain the scores for each area
    for area in job_description.keys():
            
        if area == 'Web Developement':
            for word in job_description[area]:
                if word in resume:
                    web +=1
            scores.append(web)
            
        elif area == 'Machine learning':
            for word in job_description[area]:
                if word in resume:
                    machine +=1
            scores.append(machine)
            
        elif area == 'Software Development':
            for word in job_description[area]:
                if word in resume:
                    software +=1
            scores.append(software)

            
        elif area == 'Data analytics':
            for word in job_description[area]:
                if word in resume:
                    data +=1
            scores.append(data)
            
    # Create a data frame with the scores summary
    summary = pd.DataFrame(scores,index=job_description.keys(),columns=['score']).sort_values(by='score',ascending=True)
    

    fig = px.pie(summary, values=summary.score ,names=summary.index)
    fig.update_traces(textposition='inside',textinfo='percent+label' )
    fig.write_image(output_file,engine='kaleido')
    # fig.show()

if __name__=="__main__":
    app.run(debug=True,port=8000)