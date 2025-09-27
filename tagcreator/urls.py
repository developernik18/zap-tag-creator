from django.contrib import admin
from django.urls import path
from excel2pdf import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.upload_file, name='upload_file'),
    path('preview/', views.preview_file, name='preview_file'),
    path('download/', views.download_pdf, name='download_pdf'),
    path('view-pdf/', views.view_pdf, name='view_pdf'),
]
