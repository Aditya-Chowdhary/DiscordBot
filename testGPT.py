'''
THIS IS NOT PART OF THE MAIN LOGIC/CODE. THIS IS MERELY A TESTING AREA TO TRY OUT SOME OF THE OTHER APIS
'''

import os
import openai
from dotenv import load_dotenv

# def get_api_response(prompt):
#     text = None

#     try: 
#         response = openai.Completion.create(
#             model='text-davinci-003',
#             prompt = prompt,
#             temperature=0.9,
#             max_tokens=150,
#             top_p=1,
#             frequency_penalty=0,
#             presence_penalty=0.6,
#             stop = [' Human:', ' AI:']
#         )

#         choices = response.get('choices')[0]
#         text = choices.get('text')

#     except Exception as e:
#         print('ERROR: ', e)

#     return text

# def update_list(message, pl):
#     pl.append(message)

# def create_prompt(message, pl):
#     p_msg = f"\nHuman: {message}"
#     update_list(p_msg, pl)
#     prompt = "".join(pl) 
#     return prompt

# def get_bot_response(message, pl):
#     prompt = create_prompt(message, pl)
#     bot_response = get_api_response(prompt)

#     if bot_response: 
#         update_list(bot_response, pl)
#         pos = bot_response.find('\nAI: ')
#         bot_response = bot_response[(pos + 5):]
#     else:
#         bot_response = 'Something went wrong....'

#     return bot_response

def get_api_response(prompt):
    text = None

    try: 
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt = prompt,
            temperature=0.9,
            max_tokens=50,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop = [' Human:', ' AI:']
        )

        choices = response.get('choices')[0]
        text = choices.get('text').strip()

    except Exception as e:
        print('ERROR: ', e)

    return text

def main():

    load_dotenv()
    openAI_api = os.getenv("env_OpenAI")
    openai.api_key = openAI_api


    prompt_list = ["You are a chatbot for a discord server. Respond to prompts in a helpful, yet minimal manner",
                    "\nHuman: Hello, who are you?",
                    "\nAI: Hi! I am a discord bot. How can I help you!"]
    prompt = ''.join(prompt_list)
    userinput = input("You: ")
    prompt += f'\nHuman: {userinput}'
    response = get_api_response(prompt)
    pos = response.find("\nAI: ")
    response = response[pos + 5:]
    print(f"Bot: {response}")

if __name__ == '__main__':
    main()



