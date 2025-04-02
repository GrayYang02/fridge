from http import HTTPStatus
from core.log import logger
from core.response import Response


def get_suggest(request):
    from dashscope import Application
    from core.settings import SUGGEST_APP_ID, API_KEY


    # Ensure only GET requests are processed
    # if request.method != "GET":
    #     return Response.error(msg="Invalid request method, only GET allowed")
    #
    # # Get the ingredient parameter from the request
    # foods = request.GET.get('ingredient')
    #
    # user_id = request.user.id

    # if user_id is None:
    #     return Response.error(msg="cannot search with invalid user")

    # user_id = int(user_id)

    allergies = ["peanuts", "dairy"]
    preference = ["spicy", "savory", "Korean"]
    bmi = 23.4
    # Call the external API
    response = Application.call(

        api_key=API_KEY,
        app_id=SUGGEST_APP_ID,
        prompt=f'Hi! I need a 1-day meal plan.Here’s my profile:Allergies:{allergies} '
               f'Taste Preferences:{preference}'
               f'BMI: {bmi}'
    )

    # Check response status
    if response.status_code != HTTPStatus.OK:
        msg_info = (
            f"request_id={response.request_id}, code={response.status_code}, message={response.message}.\n"
            f"See Docs: https://help.aliyun.com/zh/model-studio/developer-reference/error-code"
        )
        logger.error(msg_info)
        return Response.error(msg=msg_info)

    res = response.output.text
    print(res)
    #     res_clean = extract_clean_data(res)
    #
    #     if res_clean == '':
    #         return Response.error(msg=f"extract_clean_data failed, raw message: {res}")
    #
    #     recipes_with_ids = []
    #     try:
    #         for d in res_clean['recipes']:
    #             recipe = Recipe.objects.create(
    #                 recipe_name=d['name'],
    #                 food=d['ingredients'],
    #                 calories=d['calories'],  # new attribute
    #                 flavor_tag=d['flavor_tag'],
    #                 recipe=d['steps'],
    #                 uid=user_id,
    #                 create_time=datetime.now()
    #             )
    #             d['id'] = recipe.id  # 直接在菜谱结构中添加 ID
    #             recipes_with_ids.append(d)
    #     except Exception as e:
    #         logger.error(f'failed to store info to Recipe, err_msg:{e}')
    #     # recipes_with_ids = 127
    #     return Response.ok(data={'recipes': recipes_with_ids}, msg="Successfully retrieved recipes")
    # except Exception as e:
    #     return Response.error(msg=f"Internal Server Error: {str(e)}")

get_suggest('afsd')