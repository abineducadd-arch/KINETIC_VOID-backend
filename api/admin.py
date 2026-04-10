from django.contrib import admin
from .models import User, Advertisement, Game, UserGameLibrary, GameAchievement, UserAchievement

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'xp_points', 'total_playtime')
    search_fields = ('username', 'email')

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'ad_type', 'is_active', 'clicks', 'impressions')
    list_filter = ('ad_type', 'is_active')

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'price', 'rating', 'is_featured')
    list_filter = ('genre', 'is_featured', 'is_new')
    search_fields = ('title', 'developer')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(UserGameLibrary)
class UserGameLibraryAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'status', 'playtime')
    list_filter = ('status',)

@admin.register(GameAchievement)
class GameAchievementAdmin(admin.ModelAdmin):
    list_display = ('game', 'title', 'xp_reward')

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'unlocked_at')