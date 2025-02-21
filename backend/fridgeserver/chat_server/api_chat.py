import os
import openai
from fridgeserver.settings import API_KEY

# optional; defaults to `os.environ['OPENAI_API_KEY']`
openai.api_key = API_KEY

# all client options can be configured just like the `OpenAI` instantiation counterpart
openai.base_url = "https://free.v36.cm/v1/"
openai.default_headers = {"x-foo": "true"}


food_ingrediant = ['tomato','pasta','basil']
foods = ' '.join(food_ingrediant)

completion = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": f"Privde 3 recipe, Using food with {foods}. ",
        },
    ],
)
# print(completion.choices[0].message.content)
'''
1. Tomato Basil Pasta with Fresh Mozzarella
Ingredients:
- 1 pound pasta (such as spaghetti or penne)
- 2 tablespoons olive oil
- 3 cloves garlic, minced
- 1 can (28 oz) crushed tomatoes
- 1/4 cup fresh basil, chopped
- 8 oz fresh mozzarella, diced
- Salt and pepper, to taste

Instructions:
1. Cook the pasta according to package instructions until al dente. Drain and set aside.
2. In a large skillet, heat the olive oil over medium heat. Add the garlic and cook for 1-2 minutes until fragrant.
3. Add the crushed tomatoes and simmer for 10-15 minutes, stirring occasionally.
4. Stir in the fresh basil and season with salt and pepper.
5. Add the cooked pasta to the skillet and toss to combine.
6. Remove from heat and stir in the fresh mozzarella.
7. Serve hot and garnish with additional basil, if desired.

2. Tomato Basil Bruschetta
Ingredients:
- 1 baguette, sliced
- 4 ripe tomatoes, diced
- 1/4 cup fresh basil, chopped
- 2 cloves garlic, minced
- 2 tablespoons balsamic vinegar
- 2 tablespoons olive oil
- Salt and pepper, to taste

Instructions:
1. Preheat the oven to 400°F.
2. Arrange the baguette slices on a baking sheet and toast in the oven for 5-7 minutes, or until lightly golden brown.
3. In a bowl, combine the diced tomatoes, basil, garlic, balsamic vinegar, olive oil, salt, and pepper.
4. Spoon the tomato mixture onto the toasted baguette slices.
5. Serve as an appetizer or a light meal.

3. Tomato Basil Pesto Pasta
Ingredients:
- 1 pound pasta (such as spaghetti or fettuccine)
- 2 cups fresh basil leaves
- 1/2 cup cherry tomatoes, halved
- 1/4 cup pine nuts
- 2 cloves garlic
- 1/2 cup grated Parmesan cheese
- 1/4 cup olive oil
- Salt and pepper, to taste

Instructions:
1. Cook the pasta according to package instructions until al dente. Drain and set aside.
2. In a food processor, combine the basil, cherry tomatoes, pine nuts, garlic, Parmesan cheese, olive oil, salt, and pepper. Blend until smooth.
3. Toss the pesto with the cooked pasta until well combined.
4. Serve hot and garnish with additional basil and Parmesan cheese, if desired.

'''