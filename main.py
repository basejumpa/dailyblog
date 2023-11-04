import os
import sys
import openai
from pytrends.request import TrendReq
from datetime import datetime
import requests
import shutil

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

def create_image_from(description, file_name):
    response = openai.Image.create(
        prompt=description,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    try:
        res = requests.get(image_url, stream = True)
        if res.status_code == 200:
            with open(file_name,'wb') as f:
                shutil.copyfileobj(res.raw, f)
            print('Image sucessfully created: ', file_name)
            return True
        else:
            print('Error Image couldn\'t be retrieved!')
            return False
    except:
        return False

def get_trends(count):
    trends = []

    pytrend = TrendReq()
    df = pytrend.trending_searches(pn='germany')
    for value in df.head(count).values:
        trends.append(value[0])

    return trends


if __name__ == "__main__":

    for trend in get_trends(6):
        print(f"Trend  \"{trend}\": ", end='')

        directory = "content/posts"

        if not os.path.exists(directory):
            os.makedirs(directory)

        trend_wo_whitespaces = trend.replace(' ', '-')

        file = directory + "/" + trend_wo_whitespaces + ".md"

        image_filename = "static/images/" + trend_wo_whitespaces + ".jpg"

        user_prompt = "Schreibe einen 4 Absätze langen Blogeintrag über folgendes Thema: " + trend
        response = chat_with_gpt3(user_prompt)

        if not os.path.exists(file):
            print("Writing new blog entry.")

            now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")

            f = open(file, "w")

            f.write(f"---\n")
            f.write(f"title: \"{trend}\"\n")
            f.write(f"date:  {now}\n")
            f.write(f"draft: false\n")
            f.write(f"---\n\n")

            if create_image_from(response[:999], image_filename):
                f.write(f"\n![alt](..images/{image_filename})\n\n")

            f.write(response)
            f.close()
        
        else:
            print("Blog entry already exists.")

