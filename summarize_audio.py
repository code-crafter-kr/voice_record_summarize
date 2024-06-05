import openai
import pandas as pd

# <-----------------------------------------------------------------------> #
# OpenAI API key setup
# TODO:: Sehyoun: I recommand to use the system environment variable for the API key
openai.api_key = 'sk-proj-CBplk47U0WaA6gHBSp1kT3BlbkFJZNzTrSBU0biUEusiHu05'
# <-----------------------------------------------------------------------> #

# <-----------------------------------------------------------------------> #
# Read audio file and convert to text using OpenAI's Whisper
audio_file_path = '01035789915-025401628 20240517153334-0.mp3'

try:
    # Convert audio to text
    with open(audio_file_path, 'rb') as audio_file:
        transcription = openai.Audio.transcribe("whisper-1", audio_file)
        text_content = transcription['text']

    text_content = audio_file_path.split('-')[0] + '\n' + text_content
    text_content = audio_file_path.split(' ')[1] + '\n' + text_content

    # Print the transcribed text for debugging
    print("Transcribed Text:\n", text_content)
# <-----------------------------------------------------------------------> #

# <-----------------------------------------------------------------------> #
    # Text parsing and summarization (GPT model)
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts and summarizes information."},
            {"role": "user", "content": f"다음 텍스트에서 전화를 한 날짜, 전화번호, 내용을 추출하고 follow up task를 생성해 주세요:\n\n{text_content}\n\n포맷은 다음과 같습니다:\n\n날짜: [추출된 날짜]\n전화번호: [추출된 전화번호]\n내용: [추출된 내용]\nFollow up task: [생성된 follow up task]"}
        ]
    )
    print("debugging")
    parsed_response = response['choices'][0]['message']['content'].strip()

    # Print the parsed response for debugging
    print("Parsed Response:\n", parsed_response)
# <-----------------------------------------------------------------------> #


# <-----------------------------------------------------------------------> #
    # result to DataFrame processing
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
# <-----------------------------------------------------------------------> #

# <-----------------------------------------------------------------------> #
    # excel file update
    output_file = 'test.xlsx'
    df.to_excel(output_file, index=False)

    print(f"'{output_file}' has been saved")
# <-----------------------------------------------------------------------> #

except Exception as e:
    print(f"An error occurred: {e}")
