from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.db.models import Count
from .models import Recipe
from .models import Review
from .models import Favorite
from .forms import RecipeForm
from .forms import ReviewForm



def recipe_list(request):
    recipes = Recipe.objects.annotate(
        avg_rating=Avg('review__rating'),
        review_count=Count('review')
    )

    favorite_recipe_ids = []

    if request.user.is_authenticated:
        favorite_recipe_ids = Favorite.objects.filter(
            user=request.user
            ).values_list(
                'recipe_id',
                flat=True
            )
 
    title = request.GET.get('title')
 
    ingredient = request.GET.get('ingredient')

    sort = request.GET.get('sort')
 
 
    if title:
 
        recipes = recipes.filter(
            title__icontains=title
        )
 
 
    if ingredient:
 
        ingredient_list = ingredient.split()
 
        for word in ingredient_list:
 
            recipes = recipes.filter(
                ingredients__icontains=word
            )

    if sort == 'cost_high':
        recipes = recipes.order_by('-cost')

    elif sort == 'cost_low':
        recipes = recipes.order_by('cost')

    else:
        recipes = recipes.order_by('-avg_rating')

    context = {
        'recipes': recipes,
        'favorite_recipe_ids': favorite_recipe_ids
    }

    return render(
        request,
        'recipes/recipe_list.html',
        context
    )

@login_required
def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()

            return redirect('recipe_list')
    
    else:
        form = RecipeForm()

    context = {
        'form': form
    }

    return render(
        request,
        'recipes/recipe_create.html',
        context
    )

def recipe_detail(request, recipe_id):

    recipe = get_object_or_404(
        Recipe,
        id=recipe_id,
    )

    avg_rating = recipe.review_set.aggregate(Avg('rating'))

    is_favorite = False

    if request.user.is_authenticated:

        is_favorite = Favorite.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists()

    context = {
        'recipe': recipe,
        'avg_rating': avg_rating,
        'is_favorite': is_favorite
    }

    return render(
        request,
        'recipes/recipe_detail.html',
        context
    )

@login_required
def review_create(request, recipe_id):
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id
    )
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.recipe = recipe

            review.user = request.user
            review.save()
            return redirect(
                'recipe_detail',
                recipe_id=recipe.id
            )
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'recipe': recipe
    }

    return render(
        request,
        'recipes/review_create.html',
        context
    )

@login_required
def favorite_toggle(request, recipe_id):
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id
    )

    favorite = Favorite.objects.filter(
        user=request.user,
        recipe=recipe
    )

    if favorite.exists():
        favorite.delete()
    
    else:
        Favorite.objects.create(
            user=request.user,
            recipe=recipe
        )

    return redirect(
        request.META.get(
            'HTTP_REFERER',
            'recipe_list'
        )
    )

@login_required
def favorite_list(request):
 
    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related(
        'recipe'
    ).annotate(
        avg_rating=Avg('recipe__review__rating'),
        review_count=Count('recipe__review')
    )
 
    favorite_recipe_ids = Favorite.objects.filter(
        user=request.user
    ).values_list(
        'recipe_id',
        flat=True
    )
 
    context = {
        'favorites': favorites,
        'favorite_recipe_ids': favorite_recipe_ids
    }
 
    return render(
        request,
        'recipes/favorite_list.html',
        context
    )

@login_required
def mypage(request):
    recipes = Recipe.objects.filter(
        user=request.user
    )

    reviews = Review.objects.filter(
        user=request.user
    )

    context = {
        'recipes': recipes,
        'reviews': reviews
    }

    return render(
        request,
        'recipes/mypage.html',
        context
    )

@login_required
def recipe_update(request, recipe_id):
 
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id,
        user=request.user
    )
 
    if request.method == 'POST':
 
        form = RecipeForm(
            request.POST,
            instance=recipe
        )
 
        if form.is_valid():
 
            form.save()
 
            return redirect('mypage')
 
    else:
 
        form = RecipeForm(
            instance=recipe
        )
 
    context = {
        'form': form
    }
 
    return render(
        request,
        'recipes/recipe_update.html',
        context
    )

@login_required
def recipe_delete(request, recipe_id):
 
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id,
        user=request.user
    )
 
    if request.method == 'POST':
 
        recipe.delete()
 
        return redirect('mypage')
 
    context = {
        'recipe': recipe
    }
 
    return render(
        request,
        'recipes/recipe_delete.html',
        context
    )

@login_required
def review_update(request, review_id):
 
    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user
    )
 
    if request.method == 'POST':
 
        form = ReviewForm(
            request.POST,
            instance=review
        )
 
        if form.is_valid():
 
            form.save()
 
            return redirect('mypage')
 
    else:
 
        form = ReviewForm(
            instance=review
        )
 
    context = {
        'form': form
    }
 
    return render(
        request,
        'recipes/review_update.html',
        context
    )

@login_required
def review_delete(request, review_id):
 
    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user
    )
 
    if request.method == 'POST':
 
        review.delete()
 
        return redirect('mypage')
 
    context = {
        'review': review
    }
 
    return render(
        request,
        'recipes/review_delete.html',
        context
    )

def register(request):
    if request.method == 'POST':

        form =UserCreationForm(request.POST)
        
        if form.is_valid():

            form.save()

            return redirect('login')
    else:
        form = UserCreationForm()

    context = {
        'form': form
    }

    return render(
        request,
        'registration/register.html',
        context
    )