from django.shortcuts import render

# Create your views here.


# //
def home_list_page(request):
    return render(request, 'df_goods/index.html')
