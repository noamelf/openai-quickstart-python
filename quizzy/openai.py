import json
import openai

from quizzy.config import settings

openai.api_key = settings.OPENAI_API_KEY


def generate_animal_prompt(animal):
    return f"""Suggest three names for an animal that is a superhero.
            Animal: Cat
            Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
            Animal: Dog
            Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
            Animal: {animal}
            Names:"""


def get_pet_names(animal):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_animal_prompt(animal),
        temperature=0.6,
    )
    result = response.choices[0].text
    return result


def generate_quiz_prompt(topic, level, age):
    prompt = f"""Create a five question quiz about {topic}. The quiz have 5 difficulty levels from 1 to 5. 
                1 is the easiest and 5 is the hardest. For this quiz, the difficulty level is {level}.
                There are 3 different age levels: kids, teens, and adults. For this quiz, the age level is {age}.
                The result should be a json object. Don't surround it with any other text. 
                """
    example = """example:
                {
                    "quiz": [
                      {
                        "question": "What is the capital city of Australia?",
                        "options": ["Sydney", "Melbourne", "Canberra", "Perth"],
                        "answer": "Canberra"
                      },
                    ]
                }
    """
    return prompt + example


def get_quiz(topic, level, age):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": generate_quiz_prompt(topic, level, age)},
        ],
    )
    result = response.choices[0].message["content"]
    print(result)
    return json.loads(result)
