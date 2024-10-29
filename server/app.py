from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

app = Flask(__name__)

app.config.from_object(__name__)

client = MongoClient('localhost', 27017)
db = client['local']
collection = db['users']

CORS(app, resources={r"/users/*": {"origins": "*"}})

@app.route('/users', methods=['GET', 'POST'])
def all_users():
    response_object= {'status':'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        new_user = {
            'username': post_data.get('username'),
            'password': post_data.get('password'),
            'roles': post_data.get('roles'),
            'preferences': {
                'timezone': post_data.get('timezone')
            },
            'active': post_data.get('active'),
            'created_ts': post_data.get('created_ts'),
            'updated_ts': post_data.get('updated_ts')
        }
        collection.insert_one(new_user)
        response_object['message'] = 'User Created!'
        return jsonify(response_object)
    else:
        page = int(request.args.get('page', 1))
        items_per_page = int(request.args.get('itemsPerPage', 10))
        sort_by = request.args.get('sortBy', 'username')
        sort_order = int(request.args.get('sortOrder', 1))
        start_index = (page - 1) * items_per_page
        user_cursor = collection.find().sort(sort_by, sort_order).skip(start_index).limit(items_per_page)
        users = list(user_cursor)
        for user in users:
            user['_id'] = str(user['_id'])
        total_users = collection.count_documents({})
        response_object['users'] = users
        response_object['total'] = total_users
    return jsonify(response_object)

@app.route('/users/<user_id>', methods =['GET', 'PUT', 'DELETE'])
def get_user_details(user_id):
    response_object = {'status':'success'}
    user = collection.find_one({'_id': ObjectId(user_id)})
    if request.method == 'GET':
        if user:
            user['_id'] = str(user['_id'])
            return jsonify(user), 200
        else:
            response_object['status'] = 'fail'
            response_object['message'] = 'User not found!'
            return jsonify(response_object), 404

    elif request.method == 'PUT':
        if user is None:
            response_object['status'] = 'fail'
            response_object['message'] = 'User not found!'
            return jsonify(response_object), 404
        
        post_data = request.get_json()
        update_data ={
            'username': post_data.get('username', user['username']),
            'password': post_data.get('password', user['password']),
            'roles': post_data.get('roles', user['roles']),
            'timezone': post_data.get('timezone', user.get('preferences', {}).get('timezone', 'default_timezone')),
            'active': post_data.get('active', user['active']),
            'updated_ts': datetime.now().isoformat()
        }
        collection.update_one({'_id': ObjectId(user_id)}, {'$set': update_data})
        response_object['message'] = 'User Updated!'
        return jsonify(response_object), 200
    
    elif request.method == 'DELETE':
        if user is None:
            response_object['status'] = 'fail'
            response_object['message'] = 'User not found!'
            return jsonify(response_object), 404
            
        collection.delete_one({'_id': ObjectId(user_id)})
        response_object['message'] = 'User Deleted!'
        return jsonify(response_object), 200

if __name__ == "__main__":
    app.run(debug=True)