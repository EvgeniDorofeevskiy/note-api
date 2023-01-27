from api import app, request, multi_auth
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema, UserSchema, UserRequestSchema
from utility.helpers import get_object_or_404
from flask_apispec import doc, marshal_with, use_kwargs


@app.route("/users/<int:user_id>")
@doc(description='Api for only user.', tags=['Users'], summary= "get user by id")
@marshal_with(UserSchema, code=200)
@doc(security= [{"basicAuth": []}])
def get_user_by_id(user_id):
    """
    Get User by id
    ---
    tags:
        - Users
    parameters:
         - in: path
           name: user_id
           type: integer
           required: true
           default: 1

    responses:
        200:
            description: A single user item
            schema:
                id: User
                properties:
                    id:
                        type: integer
                    username:
                        type: string
                    is_staff:
                        type: boolean
    """


    user = get_object_or_404(UserModel, user_id)
    if user is None:
        return {"error": "User not found"}, 404
    return user, 200


@app.route("/users")
@doc(description='Api for all users.', tags=['Users'], summary= "get users ")
@marshal_with(UserSchema(many=True), code=200)
def get_users():
    """
   Get all Users
   ---
   tags:
     - Users
   """

    users = UserModel.query.all()
    return users, 200


@app.route("/users", methods=["POST"])
@doc(description='Create user', tags=['Users'], summary= "get users ")
@marshal_with(UserSchema, code=201)
@use_kwargs(UserRequestSchema, location='json')
def create_user(**kwargs):
    
    user = UserModel(**kwargs)
    # TODO: добавить обработчик на создание пользователя с неуникальным username
    if UserModel.query.filter_by(username=user.username).one_or_none():
        return {"error": "User not exist"}, 409
    user.save()
    return user, 201


@app.route("/users/<int:user_id>", methods=["PUT"])
@doc(description='Edit user', tags=['Users'], summary= "edit user ")
@marshal_with(UserSchema, code=200)
@use_kwargs(UserRequestSchema, location='json')
@doc(security= [{"basicAuth": []}])
@doc(responses={"401": {"description": "Unauthorized"}})
@doc(responses={"404": {"description": "Not found"}})
@multi_auth.login_required(role="admin")
def edit_user(user_id, **kwargs):
    # user_data = request.json
    user = get_object_or_404(UserModel, user_id)
    user.username = kwargs["username"]
    user.save()
    return user, 200


@app.route("/users/<int:user_id>", methods=["DELETE"])
@doc(description='delete user', tags=['Users'], summary= "delete user ")
@multi_auth.login_required(role="admin")
def delete_user(user_id):
    """
    Пользователь должен удаляться только со своими заметками
    """
    user = get_object_or_404(UserModel, user_id)
    user = UserModel.query.get(user_id)
    user.delete()
    
# если есть цитаты у автора то автор будет удален а цитаты нет
# в место айди автора появится значение нулл в колонке автора
    
    return {"massege": f"user with id={user_id} deleted"}, 200
    # raise NotImplemented("Метод не реализован")