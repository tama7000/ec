from django.shortcuts import render 
from django.shortcuts import render, redirect  # 追加
from django.contrib.auth import authenticate, login  # 追加
from .forms import CustomUserCreationForm  # 追加 
# 追加
from django.shortcuts import get_object_or_404, render, redirect 
from .models import Product 
from django.contrib.auth.decorators import login_required 
from django.views.decorators.http import require_POST

@login_required
def fav_products(request): 
  user = request.user 
  products = user.fav_products.all() 
  return render(request, 'app/index.html', {'products': products}) 
@require_POST
def toggle_fav_product_status(request): 
  """お気に⼊り状態を切り替える関数""" 
 
  product = get_object_or_404(Product, pk=request.POST["product_id"]) 
  user = request.user 
 
  if product in user.fav_products.all(): 
    # productがユーザーのfav_productsに既に存在している場合(お気に⼊り済の場合) 
    # → productをfav_productsから除外する(お気に⼊りを外す) 
    user.fav_products.remove(product) 
  else: 
    # productがユーザーのfav_productsに存在しない場合(お気に⼊りしていない場合) 
    # → productをfav_productsに追加する(お気に⼊り登録する) 
    user.fav_products.add(product) 
  return redirect('app:detail', product_id=product.id) 


def index(request): 
  products = Product.objects.all().order_by('-id') 
  return render(request, 'app/index.html', {'products': products})

def signup(request): 
  if request.method == 'POST': 
    form = CustomUserCreationForm(request.POST) 
    if form.is_valid(): 
      form.save() 
      input_email = form.cleaned_data['email'] 
      input_password = form.cleaned_data['password1'] 
      new_user = authenticate( 
        email=input_email, 
        password=input_password, 
      ) 
      if new_user is not None: 
        login(request, new_user) 
        return redirect('app:index') 
  else: 
    form = CustomUserCreationForm() 
  return render(request, 'app/signup.html', {'form': form}) 

def detail(request, product_id): 
  product = get_object_or_404(Product, pk=product_id) 
  context = {'product': product} 
  return render(request, 'app/detail.html', context) 