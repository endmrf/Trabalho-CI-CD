# routes.py
from flask import Blueprint, request, jsonify, Response
from prometheus_client import Counter, generate_latest
from src.data.user.list_users import (
    ListUsersUseCase,
    ListUsersParameter
)
from src.data.user.create_user import CreateUserUseCase, CreateUserParameter
from src.data.user.get_user import GetUserUseCase, GetUserParameter
from src.data.user.delete_user import DeleteUserUseCase, DeleteUserParameter
from src.data.user.update_user import UpdateUserUseCase, UpdateUserParameter

http_requests_total = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'code'])
bp = Blueprint('main', __name__)

@bp.route('/users', methods=['GET'])
def get_users():
    use_case = ListUsersUseCase()
    parameter = ListUsersParameter(
        name=request.args.get('name', ''),
    )
    response = use_case.proceed(parameter)
    serialized = use_case.serialize(response)        

    return jsonify(serialized)

@bp.route('/users/<id>', methods=['GET'])
def get_user(id):
    print("ID -> ", id)
    use_case = GetUserUseCase()
    parameter = GetUserParameter(id=id)
    response = use_case.proceed(parameter)
    user = use_case.serialize(response)
    return jsonify(user)

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    print("DATA -> ", data)
    use_case = CreateUserUseCase()
    parameter = CreateUserParameter(
        name=data['name'],
        email=data['email'],
        last_name=data['last_name'],
        cpf=data['cpf'],
    )
    response = use_case.proceed(parameter)
    new_user = use_case.serialize(response)

    return jsonify(new_user), 201

@bp.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    use_case = UpdateUserUseCase()
    parameter = UpdateUserParameter(
        id=id,
        name=data['name'],
        email=data['email'],
        cpf=data['cpf'],
        last_name=data['last_name'],
    )
    response = use_case.proceed(parameter)
    user = use_case.serialize(response)
    return jsonify(user)

@bp.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    use_case = DeleteUserUseCase()
    parameter = DeleteUserParameter(id=id)
    response = use_case.proceed(parameter)
    serialized = use_case.serialize(response)
    return jsonify(serialized), 204

@bp.route('/metrics', methods=['GET'])
def get_metrics():
    http_requests_total.labels(method='get', code='200').inc()
    return Response(generate_latest(), mimetype='text/plain')