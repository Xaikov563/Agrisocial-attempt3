from django.contrib import admin
from .models import Post, Like, Comment, ReShare, UserProfile, Product, Review, DirectMessage, ChatNotification

admin.site.register(UserProfile) 
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(ReShare)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(DirectMessage)
admin.site.register(ChatNotification)
# Register your models here.
