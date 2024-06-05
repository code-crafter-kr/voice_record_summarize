import openai

# OpenAI API key setup
openai.api_key = 'sk-proj-UX4IIXjEyFDbzwZskH0sT3BlbkFJOVeVH4DfkQWjo7qgXsBW'

# Get a list of models
models = openai.Model.list()

# print the model list
for model in models['data']:
    print(model['id'])
