import os
import sys
import openai
from pytrends.request import TrendReq
from datetime import datetime





openai.api_key = os.environ.get('API_KEY')

def chat_with_gpt3(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Du bist ein deutscher Blogger."},
            {"role": "user", "content": prompt}
        ]
    )

    assistant_reply = response['choices'][0]['message']['content']
    return assistant_reply

def get_trends(count):
    trends = []

    pytrend = TrendReq()
    df = pytrend.trending_searches(pn='germany')
    for value in df.head(count).values:
        trends.append(value[0])

    return trends


for trend in get_trends(5):
    print(f"Trend  \"{trend}\": ", end='')

    directory = "content/posts"

    if not os.path.exists(directory):
        os.makedirs(directory)

    trend_wo_whitespaces = trend.replace(' ', '-')

    file = directory + "/" + trend_wo_whitespaces + ".md"

    if not os.path.exists(file):

        print("Writing new blog entry.")

        user_prompt = "Schreibe einen Blog, 4 Absätze lang, über das Thema " + trend
        response = chat_with_gpt3(user_prompt)

        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")

        f = open(file, "w")

        f.write(f"---\n")
        f.write(f"title: {trend}\n")
        f.write(f"date:  {now}\n")
        f.write(f"draft: false\n")
        f.write(f"---\n\n")

        f.write(response)
        f.close()
    
    else:

        print("Blog entry already exists.")
