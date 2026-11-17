# script that annotates the 40 posts (20 from each school)
# one post at a time 
# writing the results to llm.csv
from google import genai
import time
import pandas as pd
client = genai.Client()
df1 = pd.read_csv("final_labeled_dataset_concordia.tsv", sep='\t')
df2 = pd.read_csv("final_labeled_dataset_mcgill.tsv", sep='\t')
categories = ["exams", "courses", "degree_planning", "grades", "other", "tech_support", "career", "housing", "fun", "study_or_survey"]

def call(df):
    for index, line in df.iterrows():
        title = line['title']
        
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=f"Here is a reddit post title: {title}. Provide a category on it out of {categories}"
        )
        print(response.text)
        time.sleep(2)
call(df1)
call(df2)