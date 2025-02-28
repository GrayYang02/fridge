import json
import os
from http import HTTPStatus
import re

import dashscope
from dashscope import Application

from demo.log import logger
from demo.response import Response
from fridgeserver.settings import API_KEY,APP_ID

dashscope.api_key = API_KEY

def get_recipe(request):
    if request.method == "GET":
        foods = request.GET.get('ingredient','user')
    else: Response.error('port method GET')
    response = Application.call(
        api_key=os.getenv(API_KEY),
        app_id=APP_ID,
        prompt=f'my food is {foods}')

    if response.status_code != HTTPStatus.OK:
        msg_info = (f'request_id={response.request_id},code={response.status_code}, message={response.message}.\n'
               f'See Doc：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
        return Response.error(msg = msg_info)
    else:
        res = response.output.text

        res_clean = extract_clean_data(res)
        if res_clean == '':
            return Response.error(msg=f'extract_clean_data failed, raw message is :{res}')

        return Response.ok(res_clean,msg='successful gain recipes')

# x = get_recipe('pasta,Tomato,Garlic')
# print(x)
# x = '''
# ```json
# {
#   "recipes": [
#     {
#       "name": "Tomato Garlic Pasta",
#       "ingredients": [
#         "1 pound spaghetti or any other pasta of your choice",
#         "2 tablespoons olive oil",
#         "4 cloves garlic, minced",
#         "1 can (28 ounces) crushed tomatoes",
#         "Salt and pepper to taste",
#         "Fresh basil leaves, chopped (optional)"
#       ],
#       "steps": [
#         "Bring a large pot of salted water to a boil. Add the pasta and cook according to package instructions until al dente.",
#         "While the pasta is cooking, heat the olive oil in a large skillet over medium heat. Add the minced garlic and sauté for about 1 minute until fragrant but not browned.",
#         "Drain the pasta and add it to the skillet with the garlic. Toss well to coat the pasta with the garlic and olive oil.",
#         "Add the crushed tomatoes to the skillet and stir to combine. Season with salt and pepper to taste.",
#         "Serve hot, garnished with fresh basil leaves if desired."
#       ]
#     },
#     {
#       "name": "Pesto Pasta with Tomato",
#       "ingredients": [
#         "1 pound spaghetti or any other pasta of your choice",
#         "1 cup fresh basil leaves",
#         "1/2 cup grated Parmesan cheese",
#         "1/2 cup pine nuts",
#         "1/2 cup extra virgin olive oil",
#         "Juice of 1 lemon",
#         "Salt and pepper to taste",
#         "1 can (28 ounces) crushed tomatoes"
#       ],
#       "steps": [
#         "Cook the pasta according to the package instructions until al dente. Drain and set aside.",
#         "In a blender or food processor, combine the basil leaves, Parmesan cheese, pine nuts, and lemon juice. Blend until smooth.",
#         "Heat a large skillet over medium heat. Add a little bit of olive oil and sauté the cooked pasta for about 2 minutes.",
#         "Add the pesto mixture to the skillet with the pasta and toss well to combine. Cook for another 2-3 minutes until heated through.",
#         "Serve hot, topped with additional grated Parmesan cheese and a squeeze of lemon juice if desired.",
#         "Top with crushed tomatoes before serving if desired."
#       ]
#     },
#     {
#       "name": "Garlic Butter Shrimp Pasta",
#       "ingredients": [
#         "1 pound spaghetti or any other pasta of your choice",
#         "1 pound large shrimp, peeled and deveined",
#         "4 tablespoons unsalted butter",
#         "6 cloves garlic, minced",
#         "1/4 cup all-purpose flour",
#         "1 cup chicken broth",
#         "Salt and pepper to taste",
#         "Fresh parsley, chopped (optional)"
#       ],
#       "steps": [
#         "Cook the pasta according to the package instructions until al dente. Drain and set aside.",
#         "In a large skillet, melt the butter over medium heat. Add the minced garlic and sauté for about 1 minute until fragrant.",
#         "Stir in the flour and cook for 1 minute, stirring constantly to prevent burning.",
#         "Gradually whisk in the chicken broth, stirring continuously to avoid lumps. Bring the mixture to a simmer and cook for 2-3 minutes until thickened.",
#         "Add the cooked pasta to the skillet and toss to coat with the sauce. Season with salt and pepper to taste.",
#         "Garnish with chopped fresh parsley before serving if desired.",
#         "Top with grilled or sautéed shrimp before serving if desired."
#       ]
#     }
#   ]
# }
# ```
# '''

def extract_clean_data(long_string):
    try:
        # first {
        first_brace_index = long_string.find('{')

        # last }
        last_brace_index = long_string.rfind('}')

        #
        if first_brace_index != -1 and last_brace_index != -1:
            ans = long_string[first_brace_index:last_brace_index+1]
            ans = eval(ans)
            return ans
        else:
            logger.error("No related sign")

    except Exception as e:
        logger.error('No return recipe been found')

    return ''

