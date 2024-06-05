import openai
import pandas as pd

# <-----------------------------------------------------------------------> #
# OpenAI API key setup
# TODO:: Sehyoun: I recommand to use the system environment variable for the API key
openai.api_key = 'sk-proj-UX4IIXjEyFDbzwZskH0sT3BlbkFJOVeVH4DfkQWjo7qgXsBW'
# <-----------------------------------------------------------------------> #


# <-----------------------------------------------------------------------> #
# Read text file
with open('test.txt', 'r', encoding='utf-8') as file:
    text_content = file.read()
    
# Text parsing and summarization
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
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
# 결과를 데이터프레임으로 변환


# <-----------------------------------------------------------------------> #
# Text to DataFrame processing
lines = parsed_response.split('\n')
data = {
    '시간(날짜)': [lines[0].replace('날짜: ', '').strip()],
    '번호': [lines[1].replace('전화번호: ', '').strip()],
    '내용': [lines[2].replace('내용: ', '').strip()],
    'Follow up task': [lines[3].replace('Follow up task: ', '').strip()]
}
df = pd.DataFrame(data)
# <-----------------------------------------------------------------------> #

# <-----------------------------------------------------------------------> #
# excel file update
output_file = 'summarize.xlsx'
df.to_excel(output_file, index=False)

print(f"요약 결과가 '{output_file}' 파일에 저장되었습니다.")
# <-----------------------------------------------------------------------> #
