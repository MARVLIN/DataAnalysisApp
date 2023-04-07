from django.contrib import admin
from django.urls import path
from chartjs import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view()),
    # path('test-api', views.get_data),
    path('api/', views.ChartData.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

