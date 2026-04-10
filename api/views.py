from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Q
from .models import User, Advertisement, Game, UserGameLibrary
from .serializers import (
    UserSerializer, UserRegistrationSerializer, AdvertisementSerializer,
    GameSerializer, UserGameLibrarySerializer, UserProfileSerializer
)
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly

# ---------- Custom JWT View ----------
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(username=request.data.get('username'))
            user_serializer = UserSerializer(user)
            response.data['user'] = user_serializer.data
        return response

# ---------- User ViewSet ----------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'register']:
            return [AllowAny()]
        return super().get_permissions()
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def profile(self, request):
        user = request.user
        if request.method in ['PUT', 'PATCH']:
            serializer = UserProfileSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---------- Advertisement ViewSet ----------
class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.filter(is_active=True)
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=['post'])
    def track_click(self, request, pk=None):
        ad = self.get_object()
        ad.clicks += 1
        ad.save()
        return Response({'message': 'Click tracked'})

# ---------- Game ViewSet ----------
class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'   # <-- ADD THIS LINE
    lookup_value_regex = '[-\w]+'   # optional, allows hyphens and word chars
    
    def get_queryset(self):
        queryset = Game.objects.all()
        genre = self.request.query_params.get('genre')
        search = self.request.query_params.get('search')
        featured = self.request.query_params.get('featured')

        if genre:
            queryset = queryset.filter(genre=genre)
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(developer__icontains=search))
        if featured:
            queryset = queryset.filter(is_featured=True)

        return queryset

    @action(detail=True, methods=['get'])
    def similar_games(self, request, pk=None):
        game = self.get_object()
        similar = Game.objects.filter(genre=game.genre).exclude(id=game.id)[:5]
        serializer = self.get_serializer(similar, many=True)
        return Response(serializer.data)

# ---------- User Game Library ViewSet ----------
class UserGameLibraryViewSet(viewsets.ModelViewSet):
    serializer_class = UserGameLibrarySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return UserGameLibrary.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        library = request.user.game_library
        total_games = library.count()
        total_playtime = sum(item.playtime for item in library.all())
        completed = library.filter(status='completed').count()

        return Response({
            'total_games': total_games,
            'total_playtime': total_playtime,
            'completed_games': completed,
        })