from django.urls import path,include
from medicines.views import *
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

urlpatterns = [

    path("categories/add/",CategoryCreateView.as_view(),name="add-category"),
    path("categories/<int:pk>/remove/",remove_category,name="remove-category"),

    path("addmedicines/",MedicineAddView.as_view(),name="add-medicines"),
    path('expired-medicines/', ExpiredMedicinesView.as_view(), name='expired_medicines'),
    path("all/",MedicineListView.as_view(),name="listmedicines"),

    path("<int:pk>/removemedicines/",remove_medicines,name="remove-medicines"),
    path("medicines/<int:pk>/",MedicineDetailView.as_view(),name="medicine-detail"),
    path("<int:pk>/change",MedicineUpdateView.as_view(),name="med-change"),
    path('autherization/', include('autherization.urls')),

    # path("shoppanel/",ShopPanelView.as_view(), name="shoppanel"),
    path("shoppanel/", shop_panel_view, name="shoppanel"),

    path('search/', search_medicines, name='search-medicine'),
    path('delete-medicine/<int:pk>/', delete_medicine, name='delete-medicine'),
    path('babycare/', BabyCareMedicinesView.as_view(), name='babycare'),
    path('babycare_detail/<int:pk>/',BabyCareDetailView.as_view(), name="babycare_detail"),

    path('beautycare/', BeautyCareMedicinesView.as_view(), name='beautycare'),
    path('beautycare_detail/<int:pk>/',BeautyCareDetailView.as_view(), name="beautycare_detail"),

    path('nutrition/',  NutritionView.as_view(), name='nutrition'),
    path('nutrition_detail/<int:pk>/',NutritionDetailView.as_view(), name="nutrition_detail"),

    path('diabetes/',  DiabetesView.as_view(), name='diabetes'),
    path('diabetes_detail/<int:pk>/',DiabetesDetailView.as_view(), name="diabetes_detail"),

    path('hairfall/',  HairfallView.as_view(), name='hairfall'),
    path('hairfall_detail/<int:pk>/',HairfallDetailView.as_view(), name="hairfall_detail"),

    path('medicines/shop_profile/', shop_profile, name="shop_profile"),
    path('medicines/update/<int:pk>',ShopProfileUpdateView.as_view() , name="updateshop"),
  

]



