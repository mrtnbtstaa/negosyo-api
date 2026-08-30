from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class PublicBaseApiView(APIView):

    authentication_classes = ()
    permission_classes = ()

class ProtectedBaseAPiView(APIView):

    permission_classes = [IsAuthenticated]
