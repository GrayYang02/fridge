
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('core/',include('core.urls')),
    path('admin/', admin.site.urls),
    # path('quest_recipe/', admin.quest_recipe, name='create_item', methods=['POST']),

]
