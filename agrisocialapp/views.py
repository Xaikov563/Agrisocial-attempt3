from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import CustomUserCreationForm, UserProfileForm, CreatePostForm, EditPostForm, CommentForm, EditCommentForm, ProductForm, EditProductForm
from .models import Notification, UserProfile, Post, Like, Comment, ReShare, Product, Review, DirectMessage, ChatNotification
from django.db.models import Q
from .decorators import membership_required
from django.utils.timezone import localtime

# Create your views here.
def home(request):
    return render(request, "home.html")

def faq(request):
    return render(request, "FAQ.html")

def about_us(request):
    return render(request, "about_us.html")

def contacts(request):
    return render(request, "contacts.html")

def postsfeed(request):
    form = CreatePostForm()  # Default form for creating a post
    userprofiles = UserProfile.objects.exclude(user=request.user)  # Fetch user profiles
    posts = Post.objects.all().order_by("-created_at")  # Fetch all posts

    for post in posts:
        post.edit_form = EditPostForm(instance=post) # Add edit form to each post
        post.liked_by_user = Like.objects.filter(user=request.user, post=post).exists()

    return render(request, "postsfeed.html", {
        "posts": posts,
        "userprofiles": userprofiles,
        "form": form,  # Always pass form to template
    })


def loginPage(request):
    # If it's a POST request, handle authentication
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid():  # Check if the form is valid
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Try to authenticate the user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Log the user in
                login(request, user)
                print(f"User {username} logged in successfully.")  # Debug print
                return redirect('postsfeed')  # Redirect to the page after login, like postsfeed
            else:
                # Invalid credentials
                print(f"Failed login attempt for {username}.")  # Debug print
                form.add_error(None, "Invalid username or password.")
        else:
            # If the form is not valid, it will stay populated with errors
            print("Form is not valid.")  # Debug print

    else:
        form = AuthenticationForm()  # If not a POST request, create a new form

    return render(request, "home.html")  # Render the login page

def register(request):
    form = CustomUserCreationForm()  # Instantiate the form
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Prevent immediate save
            user.first_name = form.cleaned_data.get("first_name")
            user.last_name = form.cleaned_data.get("last_name")
            user.email = form.cleaned_data.get("email")
            user.save()
            login(request, user) #automatically login user
            return redirect("setup_profile")  # Redirect to home page

    return render(request, "register.html", {"form": form})  # Pass form to template

@login_required
def profile_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    posts = Post.objects.filter(author=user).all().order_by("-created_at")  # Fetch posts by the user
    
    userprofile = UserProfile.objects.get(user_id=pk) # Fetch all user profiles
    create_profile, created = UserProfile.objects.get_or_create(user=user)
        
    for post in posts:
        post.liked_by_user = Like.objects.filter(user=request.user, post=post).exists()

    if request.method == 'POST':
        #get currrent user
        current_user_profile = request.user.userprofile

        #get form data
        action = request.POST.get('follow')
        #decide to follow or unfollow
        if action == 'unfollow':
            current_user_profile.follows.remove(userprofile)
        elif action == 'follow':
            current_user_profile.follows.add(userprofile)

        #save the profile
        current_user_profile.save()
            
    return render(request, 'profile.html', {
        'create_profile': create_profile,  # creates profile automatically upon registration
        'userprofile': userprofile,  # Pass user profiles to the template
        'posts': posts,  # Pass posts to the template
        })

@login_required
def edit_profile(request):
    profile = request.user.userprofile  # Get the current user's profile
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile',pk=request.user.pk)  # Redirect to the profile page
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})

@login_required
def setup_profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = None  # No profile exists, create a new one if needed

    if request.method == 'POST':
        if profile:
            form = UserProfileForm(request.POST, request.FILES, instance=profile)
        else:
            form = UserProfileForm(request.POST, request.FILES)
            
        if form.is_valid():
            form.save()
            return redirect('profile', pk=request.user.pk)  # Redirect to the profile page after successful setup
    else:
        if profile:
            form = UserProfileForm(instance=profile)
        else:
            form = UserProfileForm()

    return render(request, 'setup_profile.html', {'form': form})

@login_required
def login_view(request):
    # After successful login
    if not request.user.userprofile:  # If no profile exists
        return redirect('setup_profile')
    return redirect('postsfeed')  # Redirect to home or dashboard if profile is complete

def logout_view(request):
    logout(request)
    return redirect('home')


#POSTS FEATURE VIEWS

@login_required
def create_post(request):
    form = CreatePostForm()  # Default form for creating a post

    if request.method == "POST":
        form_type = request.POST.get("form_type")  # Check which form was submitted

        if form_type == "create_post":  # Handle post creation
            form = CreatePostForm(request.POST, request.FILES)
            content = request.POST.get("content", "").strip()
            if form.is_valid():
                 if not content:
                    messages.error(request, "Post content cannot be empty.")
                    return redirect('postsfeed')  # or render the same page with error
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post Successfully Uploaded")
            return redirect("postsfeed")

        return render(request, 'postsfeed.html', {'form': form})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, id=pk)

    if post.author != request.user:
        messages.error(request, "You are not allowed to edit this post.")
        return redirect("profile", pk=request.user.pk)

    if request.method == "POST":
        form = EditPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            next_page = request.GET.get("next")
            if next_page == "profile":
                return redirect("profile", pk=request.user.pk)
            return redirect("postsfeed")
    else:
        form = EditPostForm(instance=post)

    return render(request, "edit_post.html", {"form": form, "post": post})



@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    posts = Post.objects.all().order_by("-created_at")

    if post.author != request.user:
        messages.error(request, "You are not allowed to delete this ost.")
        return redirect("profile", pk=request.user.pk)
        
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully!")
        
        next_page = request.GET.get("next")
        if next_page == "profile":
            return redirect("profile", pk=request.user.pk)
        
        return redirect("postsfeed")  # No pk needed
    
    return redirect("profile", pk=request.user.pk)

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    user = request.user

    # Get or create a like instance for the user and post
    like, created = Like.objects.get_or_create(user=user, post=post)

    if not created:
        like.delete()  # Unlike the post
        liked = False
    else:
        liked = True

    # Get the total number of likes for the post
    like_count = Like.objects.filter(post=post).count()
    
    # Return the updated like status and like count as a JSON response
    return JsonResponse({"liked": liked, "likes": like_count})

#COMMENT SECTION

@login_required
def comment_view(request, pk):
    userprofiles = UserProfile.objects.exclude(user=request.user)  # Fetch user profiles
    post = get_object_or_404(Post, id=pk)
    comments = post.comments.all().order_by("-created_at")
    
    next_page = request.GET.get("next")
    if next_page == "":
        if next_page == "profile":
            return redirect("profile", pk=request.user.pk) 
        return redirect('postsfeed')
    
    return render(request, 'comments.html', {'post': post, 'comments': comments, 'userprofiles': userprofiles, 'user': request.user})

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  # Set the user to the logged-in user
            comment.post = post  # Set the associated post
            comment.save()

        
            # Notify post owner if commenter is not the post owner
            if post.author != request.user:
                Notification.objects.create(
                    user=post.author,
                    sender=request.user,
                    verb="commented on your post.",
                    post=post
                )

            return redirect('comment_view', pk=post.id)  # Adjust to match your URL pattern
    else:
        form = CommentForm()

    return render(request, 'comments.html', {
        'form': form,
        'post': post,
        # Include other context if needed (e.g., comments)
    })

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    post = comment.post
    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted successfully!")
        return redirect('comment_view', pk=post.id)
    
@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    post = comment.post
    if request.method == "POST":
        form = EditCommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated successfully!")
            next_page = request.GET.get("next")
            if next_page == "profile":
                return redirect("profile", pk=request.user.pk)
            return redirect('comment_view', pk=post.id)
    else:
        form = EditCommentForm(instance=comment)
        return render(request, "edit_comment.html", {"form": form, "comment": comment, "post" : post})

@login_required
def reshare_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    reshare, created = ReShare.objects.get_or_create(user=request.user, post=post)
    if not created:
        reshare.delete()  # Toggle reshare off
    return JsonResponse({'reshares': post.reshares.count()})

#Marketplace Views =====

@login_required
def marketplace(request):
    products = Product.objects.all().select_related('seller').prefetch_related('reviews')



    return render(request, 'marketplace.html', {'products': products, 'range': range(1, 6)})

def product_view(request, pk):
    product = get_object_or_404(
        Product.objects.select_related('seller').prefetch_related('reviews'),
        pk=pk)

    user = product.seller
    userprofile = get_object_or_404(UserProfile, user=user)

    return render(request, 'product_view.html', {
        'product': product,
        'userprofile': userprofile,
        'user': user,
        'range': range(1, 6)  # for displaying rating stars
    })

def user_shop_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    products = Product.objects.filter(seller=user).select_related('seller').prefetch_related('reviews')
    userprofile = UserProfile.objects.get(user_id=pk) # Fetch all user profiles

    if request.method == 'POST':
        #get currrent user
        current_user_profile = request.user.userprofile

        #get form data
        action = request.POST.get('follow')
        #decide to follow or unfollow
        if action == 'unfollow':
            current_user_profile.follows.remove(userprofile)
        elif action == 'follow':
            current_user_profile.follows.add(userprofile)

        #save the profile
        current_user_profile.save()

    return render(request, 'user_shop.html', {
    'userprofile': userprofile,
    'products': products,
    'range': range(1, 6),
})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('user_shop_view', pk=request.user.id)
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.seller != request.user:
        messages.error(request, "You are not authorized to delete this product.")
        return redirect('user_shop_view', pk=request.user.id)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully.")

    return redirect('user_shop_view', pk=request.user.id)

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.seller != request.user:
        messages.error(request, "You are not authorized to edit this product.")
        return redirect('user_shop_view', pk=request.user.id)

    if request.method == "POST":
        form = EditProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('user_shop_view', pk=request.user.id)
    else:
        form = EditProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form})

#MESSAGING VIEWS
def chat_list(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    
    follows = profile.follows.all()  # Users you follow
    followed_by = profile.followed_by.all()  # Users who follow you

    users = (follows | followed_by).distinct()  # Union without duplicates

    return render(request, 'chat_list.html', {'users': users})

@login_required
def chat_detail(request, id):
    user_to_chat_with = get_object_or_404(UserProfile, user_id=id)
    messages = DirectMessage.objects.filter(
        sender=request.user, receiver=user_to_chat_with.user
    ) | DirectMessage.objects.filter(
        sender=user_to_chat_with.user, receiver=request.user
    )
    messages = messages.order_by('timestamp')

    if request.method == 'POST':
        message_content = request.POST.get('message')
        if message_content:
            DirectMessage.objects.create(
                sender=request.user,
                receiver=user_to_chat_with.user,
                message=message_content
            )
    
    return render(request, 'chat_detail.html', {'messages': messages, 'user_to_chat_with': user_to_chat_with})

@login_required
def send_message(request, username):
    if request.method == "POST":
        receiver = get_object_or_404(User, username=username)
        message_text = request.POST.get("message")

        if message_text:
            msg = DirectMessage.objects.create(sender=request.user, receiver=receiver, message=message_text)

            # Optionally, create a notification for the receiver
            ChatNotification.objects.create(
                sender=request.user,
                receiver=receiver,
                message=f"New message from {request.user.username}"
            )

            # Return message details including timestamp
            return JsonResponse({
                "status": "ok",
                "message": msg.message,
                "timestamp": localtime(msg.timestamp).strftime("%b %d, %Y %I:%M %p"),
                "sender_username": msg.sender.username
            })
    return JsonResponse({"status": "error"}, status=400)

@login_required
def fetch_messages(request, username):
    other_user = get_object_or_404(User, username=username)
    messages = DirectMessage.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    data = [{
        'id': msg.id,
        'sender': msg.sender.username,
        'receiver': msg.receiver.username,
        'message': msg.message,
        'timestamp': msg.timestamp.strftime("%b %d, %Y %I:%M %p")
    } for msg in messages]

    return JsonResponse(data, safe=False)

@login_required
def unread_notifications(request):
    count = ChatNotification.objects.filter(receiver=request.user, is_seen=False).count()
    return JsonResponse({"unread_count": count})

#MEMBERSHIP VIEWS

@login_required
def membership_page(request):
    return render (request, 'memberships.html')
    
@login_required
def claim_membership(request):
    profile = request.user.userprofile

    if not profile.has_membership:
        profile.has_membership = True
        profile.save()
        messages.success(request, "Subscription successfully purchased!")
    else:
        messages.info(request, "You already have a membership.")

    return redirect('profile', pk=request.user.pk)


@membership_required
def exclusive_page(request):
    return render(request, 'exclusive.html')

#NOTIFICATIONS VIEWS

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'notifications.html', {
        'notifications': notifications,
        })