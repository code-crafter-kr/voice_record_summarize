import speech_recognition as sr
# But don't recommand to use it - GPT model is better
# Recognizer 객체 생성
r = sr.Recognizer()

# 오디오 파일을 음성 입력 소스로 사용
audio_file = "01035789915-025401628 20240517153334-0.mp3"

with sr.AudioFile(audio_file) as source:
    audio = r.record(source)  # 오디오 파일 전체를 읽음

# Google Web Speech API를 사용하여 음성을 텍스트로 변환
try:
    # 음성을 텍스트로 변환
    text = r.recognize_google(audio, language="ko-KR")
    print("Google Web Speech thinks you said: " + text)
    
    # 텍스트 파일로 저장
    with open("transcribed_text.txt", "w", encoding="utf-8") as text_file:
        text_file.write(text)

    print("Transcription saved to transcribed_text.txt")

except sr.UnknownValueError:
    print("Google Web Speech could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Web Speech service; {0}".format(e))
