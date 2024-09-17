from graphene_django import DjangoObjectType
from apps.users_api.models import AdminBooksRepresentation




class AdminBookRepresentationType(DjangoObjectType):
    class Meta:
        model = AdminBooksRepresentation
        fields = "__all__"
