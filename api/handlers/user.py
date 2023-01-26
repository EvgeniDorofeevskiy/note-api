from api import app, request, multi_auth
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema
from utility.helpers import get_object_or_404


@app.route("/users/<int:user_id>")
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
    return user_schema.dump(user), 200


@app.route("/users")
def get_users():
    """
   Get all Users
   ---
   tags:
     - Users
   """

    users = UserModel.query.all()
    return users_schema.dump(users), 200


@app.route("/users", methods=["POST"])
def create_user():
    user_data = request.json
    user = UserModel(**user_data)
    # TODO: добавить обработчик на создание пользователя с неуникальным username
    if UserModel.query.filter_by(username=user.username).one_or_none():
        return {"error": "User not exist"}, 409
    user.save()
    return user_schema.dump(user), 201


@app.route("/users/<int:user_id>", methods=["PUT"])
@multi_auth.login_required(role="admin")
def edit_user(user_id):
    user_data = request.json
    user = get_object_or_404(UserModel, user_id)
    user.username = user_data["username"]
    user.save()
    return user_schema.dump(user), 200


@app.route("/users/<int:user_id>", methods=["DELETE"])
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