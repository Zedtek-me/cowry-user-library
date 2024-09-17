from graphene import Schema, ObjectType
from apps.users_api.schema.mutations import api_mutations
from apps.users_api.schema.queries import api_queries

class Query(api_mutations.Mutation, ObjectType):
    pass

class Mutation(api_queries.Query, ObjectType):
    pass

schema = Schema(query=Query, mutation=Mutation)
