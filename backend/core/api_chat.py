from dashscope import Application 
from demo.log import logger
from demo.settings import APP_ID,API_KEY
from http import HTTPStatus
from demo.response import Response 

from core.log import logger
from core.response import Response
from core.settings import APP_ID,API_KEY 

def get_recipe(request):
    try:
        # Ensure only GET requests are processed
        if request.method != "GET":
            return Response.error(msg="Invalid request method, only GET allowed")

        # Get the ingredient parameter from the request
        foods = request.GET.get('ingredient')
        user_id = request.GET.get('user_id')

        # Call the external API
        response = Application.call(
            api_key= API_KEY,
            app_id= APP_ID,
            prompt=f'My food is {foods}'
        )

        # Check response status
        if response.status_code != HTTPStatus.OK:
            msg_info = (
                f"request_id={response.request_id}, code={response.status_code}, message={response.message}.\n"
                f"See Docs: https://help.aliyun.com/zh/model-studio/developer-reference/error-code"
            )
            logger.error(msg_info)
            return Response.error(msg=msg_info)

        # Process the response
        res = response.output.text
        res_clean = extract_clean_data(res)

        if not res_clean:
            return Response.error(msg=f"extract_clean_data failed, raw message: {res}")

        return Response.ok(data=res_clean, msg="Successfully retrieved recipes")

    except Exception as e:
        return Response.error(msg=f"Internal Server Error: {str(e)}")

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

    except Exception as err:
        logger.error(err)
        logger.error('No return recipe been found')

    return ''

