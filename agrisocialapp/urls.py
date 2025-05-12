from django.urls import path
from . import views
from .views import faq, about_us, contacts, notifications_view, exclusive_page, membership_page, claim_membership, edit_profile, create_post, like_post, comment_view, reshare_post, delete_product, edit_product, chat_list, chat_detail, send_message, fetch_messages

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about_us, name="about_us"),
    path("contacts/", views.contacts, name="contacts"),
    path("faq/", views.faq, name="faq"),
    

    # AUTHENTICATION URLS
    path("postsfeed/", views.postsfeed, name="postsfeed"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.register, name="register"),
    path('profile/<int:pk>/', views.profile_view, name='profile'),  
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('setup-profile/', views.setup_profile, name='setup_profile'),


    # POSTS FEATURE URLS
    path('create/', views.create_post, name='create_post'),
    path('posts/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:pk>/', views.delete_post, name='delete_post'),
    path('posts/<int:pk>/like/', like_post, name='like_post'),
    path('posts/<int:post_id>/reshare/', reshare_post, name='reshare_post'),

    # COMMENTS
    path('comments/<int:pk>/', views.comment_view, name='comment_view'),
    path('comments/<int:pk>/edit/', views.edit_comment, name='edit_comment'),
    path('post/<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    path('post/<int:pk>/delete_comment/', views.delete_comment, name='delete_comment'),

    # MARKETPLACE
    path("marketplace/", views.marketplace, name="marketplace"),
    path("marketplace/product/<int:pk>/", views.product_view, name="product_view"),
    path("marketplace/shop/<int:pk>/", views.user_shop_view, name="user_shop_view"),
    path("marketplace/add_product/", views.add_product, name="add_product"),
    path("marketplace/delete_product/<int:pk>/", views.delete_product, name="delete_product"),
    path("marketplace/edit_product/<int:pk>/", views.edit_product, name="edit_product"),

    # MESSAGING 
      # Chat list (mutual followers)
    path('messages/', views.chat_list, name='chat_list'),

    # Chat detail (conversation with specific user)
    path('messages/<int:id>/', views.chat_detail, name='chat_detail'),

    # Send message (AJAX/POST request)
    path('messages/send/<str:username>/', views.send_message, name='send_message'),

    # Notifications (check unread messages)
    path('notifications/unread/', views.unread_notifications, name='unread_notifications'),

    path('meesages/fetch/<str:username>/', views.fetch_messages, name='fetch_messages'),

    # Membership urls
    path('membership/', views.membership_page, name='membership_page'),
    path('claim-membership/', views.claim_membership, name='claim_membership'),
    path('exclusive/', views.exclusive_page, name='exclusive'),
    
    # Notifications urls
    path('notifications/', views.notifications_view, name='notifications_view'),
]
