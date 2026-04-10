from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    total_playtime = models.IntegerField(default=0)  # in hours
    xp_points = models.IntegerField(default=0)
    
    def __str__(self):
        return self.username

class Advertisement(models.Model):
    AD_TYPES = [
        ('banner', 'Banner'),
        ('sidebar', 'Sidebar'),
        ('popup', 'Popup'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='ads/')
    link_url = models.URLField(blank=True)
    ad_type = models.CharField(max_length=20, choices=AD_TYPES, default='banner')
    is_active = models.BooleanField(default=True)
    clicks = models.IntegerField(default=0)
    impressions = models.IntegerField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Game(models.Model):
    GENRE_CHOICES = [
        ('action', 'Action'),
        ('rpg', 'RPG'),
        ('strategy', 'Strategy'),
        ('simulation', 'Simulation'),
        ('horror', 'Horror'),
        ('cyberpunk', 'Cyberpunk'),
        ('sci-fi', 'Sci-Fi'),
        ('mmo', 'MMO'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    cover_image = models.ImageField(upload_to='games/covers/')
    banner_image = models.ImageField(upload_to='games/banners/', null=True, blank=True)
    gallery_images = models.JSONField(default=list)  # List of image URLs
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    developer = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    release_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    total_ratings = models.IntegerField(default=0)
    download_size = models.CharField(max_length=50)  # e.g., "45 GB"
    trailer_url = models.URLField(blank=True)
    system_requirements_min = models.JSONField(default=dict)
    system_requirements_rec = models.JSONField(default=dict)
    features = models.JSONField(default=list)  # List of feature strings
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    @property
    def final_price(self):
        return self.discount_price if self.discount_price else self.price

class UserGameLibrary(models.Model):
    STATUS_CHOICES = [
        ('owned', 'Owned'),
        ('wishlist', 'Wishlist'),
        ('playing', 'Currently Playing'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_library')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='owners')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='owned')
    playtime = models.IntegerField(default=0)  # in hours
    last_played = models.DateTimeField(null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True)
    user_rating = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['user', 'game']
    
    def __str__(self):
        return f"{self.user.username} - {self.game.title}"

class GameAchievement(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='achievements/', null=True, blank=True)
    xp_reward = models.IntegerField(default=100)
    is_hidden = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.game.title} - {self.title}"

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(GameAchievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'achievement']