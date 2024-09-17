import graphene
from apps.users_api.schema.types.user_api_model_types import AdminBookRepresentationType
from apps.users_api.models import AdminBooksRepresentation

class Query(graphene.ObjectType):
    books = graphene.List(
        AdminBookRepresentationType,
        id=graphene.Int(),
        author=graphene.String(),
        category=graphene.String()
    )
    book = graphene.Field(
        AdminBookRepresentationType,
        id=graphene.Int()
    )

    def resolve_books(self, info, **kwargs):
        _filter = {}
        if kwargs.get("id"):
            _filter["_id"] = kwargs.get("id")
        if kwargs.get("author"):
            _filter["author"] = kwargs.get("author")
        if kwargs.get("category"):
            _filter["category"] = kwargs.get("category")
        
        books = AdminBooksRepresentation.objects.filter(**_filter)
        return books

    def resolve_book(self, id):
        return AdminBooksRepresentation.objects.filter(_id=id).first()
    
    