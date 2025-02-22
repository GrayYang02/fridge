import os
import openai
from fridgeserver.settings import API_URL,API_KEY,RECIPE_QUANTITY

# optional; defaults to `os.environ['OPENAI_API_KEY']`
openai.api_key = API_KEY
quantity = RECIPE_QUANTITY

# all client options can be configured just like the `OpenAI` instantiation counterpart
openai.base_url = API_URL
openai.default_headers = {"x-foo": "true"}

def get_recipe(foods ='' ):
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"Provide {RECIPE_QUANTITY} recipes using the following ingredients: {foods}. "
        f"Return the response in JSON format as shown below:\n\n"
        "{\n"
        '  "recipes": [\n'
        '    {"recipe 1": "[recipe details]"},\n'
        '    {"recipe 2": "[recipe details]"},\n'
        '    {"recipe 3": "[recipe details]"}\n'
        "  ]\n"
        "}"
            },
        ],
    )
    return completion.choices[0].message.content, quantity

