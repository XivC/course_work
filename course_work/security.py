from rest_framework.permissions import IsAuthenticated, IsAdminUser


def make_readonly_permissions(action: str):
    if action == {'list', 'retrieve'}:
        permission_classes = [IsAuthenticated]
    else:
        permission_classes = [IsAdminUser]
    return [permission() for permission in permission_classes]