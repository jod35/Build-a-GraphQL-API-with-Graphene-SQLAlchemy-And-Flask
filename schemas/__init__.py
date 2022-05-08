import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from db import (
    User as UserDBModel,
    Post as PostDBModel,
    session
)


class UserSchema(SQLAlchemyObjectType):
    class Meta:
        model = UserDBModel
        interfaces = (relay.Node,)


class PostSchema(SQLAlchemyObjectType):
    class Meta:
        model = PostDBModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    all_users = SQLAlchemyConnectionField(UserSchema.connection)

    all_posts = SQLAlchemyConnectionField(PostSchema.connection)


class UserMutation(graphene.Mutation):

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)

    user = graphene.Field(lambda: UserSchema)

    def mutate(self, info, username, email):
        user = UserDBModel(
            username=username,
            email=email
        )

        session.add(user)
        session.commit()

        return UserMutation(user=user)


class PostMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    post = graphene.Field(lambda: PostSchema)

    def mutate(self, info, user_id, title, content):

        author = session.query(UserDBModel).filter_by(id=user_id).first()
        new_post = PostDBModel(
            title=title,
            content=content,
            author=author
        )

        session.add(new_post)
        session.commit()

        return PostMutation(post=new_post)


class Mutation(graphene.ObjectType):
    mutate_user = UserMutation.Field()
    mutate_post = PostMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
