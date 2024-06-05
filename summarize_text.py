# This file is for summarizing the text file and save the result to the excel file

import openai
import pandas as pd

# <-----------------------------------------------------------------------> #
# OpenAI API key setup
# TODO:: Sehyoun: I recommand to use the system environment variable for the API key
openai.api_key = 'sk-proj-CBplk47U0WaA6gHBSp1kT3BlbkFJZNzTrSBU0biUEusiHu05'
# <-----------------------------------------------------------------------> #


# <-----------------------------------------------------------------------> #
# Read text file
with open('test.txt', 'r', encoding='utf-8') as file:
    text_content = file.read()

# Text parsing and summarization
response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that extracts and summarizes information."},
        {"role": "user", "content": f"다음 텍스트에서 날짜, 전화번호, 내용을 추출하고 follow up task를 생성해 주세요:\n\n{text_content}\n\n포맷은 다음과 같습니다:\n\n날짜: [추출된 날짜]\n전화번호: [추출된 전화번호]\n내용: [추출된 내용]\nFollow up task: [생성된 follow up task]"}
    ]
)
parsed_response = response['choices'][0]['message']['content'].strip()
# <-----------------------------------------------------------------------> #


# <-----------------------------------------------------------------------> #
#TODO:: this print is for debugging, remove it later
# Print the parsed response
print(parsed_response)
# <-----------------------------------------------------------------------> #


# <-----------------------------------------------------------------------> #
# Text to DataFrame processing
lines = parsed_response.split('\n')
date = lines[0].replace('날짜: ', '').strip()
phone = lines[1].replace('전화번호: ', '').strip()
content = "\n".join(lines[2:2+lines[2:].index('Follow up task:')]).replace('내용: ', '').strip()
follow_up = "\n".join(lines[2+lines[2:].index('Follow up task:'):]).replace('Follow up task: ', '').strip()

data = {
    '시간(날짜)': [date],
    '번호': [phone],
    '내용': [content],
    'Follow up task': [follow_up]
}
df = pd.DataFrame(data)
print(df)
# <-----------------------------------------------------------------------> #

# <-----------------------------------------------------------------------> #
# excel file update
output_file = 'test.xlsx'
df.to_excel(output_file, index=False)

# save the file

print(f"'{output_file}' has been saved")
# <-----------------------------------------------------------------------> #
