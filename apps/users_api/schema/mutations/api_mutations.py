import graphene
from apps.users_api.models import AdminBooksRepresentation
from apps.users_api.schema.types.user_api_model_types import AdminBookRepresentationType
from django.db.transaction import atomic
from datetime import datetime, timedelta
from django.utils import timezone


class EnrollUsers(graphene.Mutation):
    '''
    enrolls users into the library, 
    sending their info to the admin service, since it manages the user data
    '''
    message = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
    
    def mutate(self, info, **kwargs):
        # sends user details here
        pass



class BorrowBook(graphene.Mutation):
    '''users borrow books through this api'''
    message = graphene.String()
    book = graphene.Field(AdminBookRepresentationType)

    class Arguments:
        book_id = graphene.Int(required=True)
        return_after = graphene.Int(required=True)

    @atomic
    def mutate(self, info, **kwargs):
        book = AdminBooksRepresentation.objects.filter(_id=kwargs.get("book_id")).first()
        book.status = "BORROWED"
        book.meta["return_date"] = datetime.strftime(
            (timezone.now() + timedelta(days=kwargs.get("return_after"))),
            "%Y-%m-%d %H:%M:%S"
        )
        book.save()
        return BorrowBook(
            message="book successfully borrowed!",
            book=book
        )

class Mutation(graphene.ObjectType):
    borrow_book = BorrowBook.Field(description="borrow book")
    enroll_users = EnrollUsers.Field(description="enroll user into the library")
    