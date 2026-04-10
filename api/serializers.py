from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Advertisement, Game, UserGameLibrary, GameAchievement, UserAchievement

# ---------- User Serializers ----------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'bio', 'avatar', 'join_date', 'total_playtime', 'xp_points')
        read_only_fields = ('id', 'join_date')

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    game_library = serializers.StringRelatedField(many=True, read_only=True)
    achievements = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'bio', 'avatar', 'join_date', 'total_playtime', 'xp_points', 'game_library', 'achievements')
        read_only_fields = ('id', 'join_date', 'username', 'email')

# ---------- Advertisement Serializer ----------
class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'
        read_only_fields = ('clicks', 'impressions', 'created_at')

# ---------- Game & Achievement Serializers ----------
class GameAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameAchievement
        fields = ('id', 'title', 'description', 'icon', 'xp_reward', 'is_hidden')

class GameSerializer(serializers.ModelSerializer):
    achievements = GameAchievementSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'rating', 'total_ratings')

# ---------- User Game Library Serializer ----------
class UserGameLibrarySerializer(serializers.ModelSerializer):
    game = GameSerializer(read_only=True)
    game_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserGameLibrary
        fields = ('id', 'game', 'game_id', 'status', 'playtime', 'last_played', 'added_date', 'user_rating', 'review')
        read_only_fields = ('added_date',)

# ---------- User Achievement Serializer ----------
class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = GameAchievementSerializer(read_only=True)

    class Meta:
        model = UserAchievement
        fields = ('id', 'achievement', 'unlocked_at')