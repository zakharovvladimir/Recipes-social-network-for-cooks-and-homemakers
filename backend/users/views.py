"""Users views.py."""
from django.shortcuts import get_object_or_404
from djoser import utils
from djoser.views import TokenDestroyView, UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.pagination import CustomPagination
from api.serializers import CustomUserSerializer, SubscribeSerializer

from .models import Follow, User


class CustomUserViewSet(UserViewSet):
    """Custom User viewset."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, **kwargs):
        """Subscribe func."""
        user = request.user
        author = get_object_or_404(User, id=self.kwargs.get('id'))
        if request.method == 'POST':
            subscription = SubscribeSerializer(author,
                                               data=request.data,
                                               context={"request": request})
            subscription.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            return Response(subscription.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            subscription = get_object_or_404(Follow,
                                             user=user,
                                             author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        """Subscriptions func."""
        user = request.user
        queryset = User.objects.filter(following__user=user).order_by('id')
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(pages,
                                         many=True,
                                         context={'request': request})
        return self.get_paginated_response(serializer.data)


class CustomTokenDestroyView(TokenDestroyView):
    """Logout."""

    def post(self, request):
        """Start logout."""
        utils.logout_user(request)
        return Response(status=status.HTTP_201_CREATED)


class ChangePasswordView(CustomTokenDestroyView):
    """Password change."""

    def patch(self, request, *args, **kwargs):
        """Start password change."""
        data = request.data
        new_password = data.get('new_password')
        current_password = data.get('current_password')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not self.user.check_password(current_password):
            return Response({'current_password': ['Wrong password.']},
                            status=status.HTTP_400_BAD_REQUEST)
        self.user.set_password(new_password)
        self.user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
