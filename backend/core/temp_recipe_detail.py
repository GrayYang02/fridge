from demo.response import Response

temp_res =  {"recipes": [
            {
                "name": "Apple and Banana Smoothie",
                "ingredients": [
                    "2 medium-sized apples, peeled and chopped",
                    "1 large banana, peeled",
                    "1 cup of milk (dairy or non-dairy)",
                    "1 tablespoon honey (optional)"
                ],
                "steps": [
                    "Place the chopped apples and banana into a blender.",
                    "Add the milk and honey if using.",
                    "Blend all ingredients until smooth and creamy.",
                    "Pour the smoothie into glasses and serve immediately."
                ]
            } 
        ]
}
def recipe_detail(request):
    # Get the ingredient parameter from the request
    recipe_id = request.GET.get('recipe_id')
    user_id = request.GET.get('user_id')

    return Response.ok(data = temp_res, msg=f"recipe_id = {recipe_id}, user_id = {user_id}")