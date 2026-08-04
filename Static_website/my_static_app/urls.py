from django.urls import path
from . import views

app_name = 'my_static_app'

urlpatterns = [
    path('', views, name="index")
    path('admin/', admin.site.urls),
]