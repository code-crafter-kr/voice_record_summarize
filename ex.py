import openai

# OpenAI API 키 설정
openai.api_key = 'sk-proj-UX4IIXjEyFDbzwZskH0sT3BlbkFJOVeVH4DfkQWjo7qgXsBW'

# 사용 가능한 모델 목록 가져오기
models = openai.Model.list()

# 모델 목록 출력
for model in models['data']:
    print(model['id'])
