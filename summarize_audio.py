import openai
import pandas as pd
import sys
import subprocess
import os

# <-----------------------------------------------------------------------> #
# Function to split the text into the required parts
def split_text(text):
    # Define the keywords to search for
    date_keyword = "시간: "
    phone_keyword = "전화번호: "
    content_keyword = "내용: "
    follow_up_keyword = "Follow up task:"

    # Find the positions of the keywords
    date_pos = text.find(date_keyword)
    phone_pos = text.find(phone_keyword)
    content_pos = text.find(content_keyword)
    follow_up_pos = text.find(follow_up_keyword)

    # Extract the parts of the text based on the positions of the keywords
    date = text[date_pos + len(date_keyword):phone_pos].strip()
    phone = text[phone_pos + len(phone_keyword):content_pos].strip()
    content = text[content_pos + len(content_keyword):follow_up_pos].strip()
    follow_up = text[follow_up_pos + len(follow_up_keyword):].strip()

    return date, phone, content, follow_up
# <-----------------------------------------------------------------------> #

# <-----------------------------------------------------------------------> #
# OpenAI API key setup
# TODO:: Sehyoun: I recommend using the system environment variable for the API key
openai.api_key = 'sk-proj-OuXA8njLyg4QHK9ew1eDT3BlbkFJUqXbcSFBnGUsB4XMKC74'
# <-----------------------------------------------------------------------> #

# <-----------------------------------------------------------------------> #
def process_audio_file(audio_file_path):
    # Read audio file and convert to text using OpenAI's Whisper
    with open(audio_file_path, 'rb') as audio_file:
        transcription = openai.Audio.transcribe("whisper-1", audio_file)
        text_content = transcription['text']

    text_content = audio_file_path.split('-')[0] + '\n' + text_content # 전화번호 정보
    text_content = audio_file_path.split(' ')[1] + '\n' + text_content # 시간정보

    # Print the transcribed text for debugging
    print("Transcribed Text:\n", text_content)
    # <-----------------------------------------------------------------------> #

    # <-----------------------------------------------------------------------> #
    # Text parsing and summarization (GPT model)
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts and summarizes information."},
            {"role": "user", "content": f"다음 텍스트에서 전화를 한 날짜와 시간, 전화번호, 내용을 추출하고 follow up task를 생성해 주세요:\n\n{text_content}\n\n포맷은 다음과 같습니다:\n\n시간: [ex) 6/5/2024 17:33]\n전화번호: [ex) 010-3578-9915]\n내용: [추출된 내용]\nFollow up task: [생성된 follow up task]"},
            {"role": "user", "content": "특히 일정에 관한 내용이라면 해당 날짜를 추출해 주세요."}
        ]
    )
    parsed_response = response['choices'][0]['message']['content'].strip()
    # <-----------------------------------------------------------------------> #

    # <-----------------------------------------------------------------------> #
    # result to DataFrame processing
    date, phone, content, follow_up = split_text(parsed_response)

    print(date + '\n' + phone + '\n' + content + '\n' + follow_up)
    data = {
        '시간(날짜)': [date],
        '번호': [phone],
        '내용': [content],
        'Follow up task': [follow_up]
    }
    df = pd.DataFrame(data)
    # <-----------------------------------------------------------------------> #

    # <-----------------------------------------------------------------------> #
    # Save DataFrame to a temporary file
    temp_file = 'temp.xlsx'
    df.to_excel(temp_file, index=False)

    # Execute file_save.py with the temporary file as argument
    try:
        subprocess.run(["python", "file_save.py", temp_file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during processing: {e.stderr}")

    # Remove the temporary file
    os.remove(temp_file)

    print(f"'{temp_file}' has been processed and deleted")
    # <-----------------------------------------------------------------------> #

# <-----------------------------------------------------------------------> #
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python summarize_audio.py <audio_file_path>")
        sys.exit(1)

    audio_file_path = sys.argv[1]
    process_audio_file(audio_file_path)
# <-----------------------------------------------------------------------> #
