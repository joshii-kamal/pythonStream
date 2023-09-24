from  config.get_config import  get_config
import openai
class AskOpenAI:
    
    def ask(cls,prompt):
        config = get_config()
        ai_response = openai.ChatCompletion.create(
            model=config['model'],
            messages=[
                {"role": "system", "content": "You are a professor"},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
            api_key=config['apiKey'],
        )

        answer = ai_response.choices[0].message.content
        return answer