from flask import Flask, jsonify, request
import instaloader
from functools import wraps
import os
from werkzeug.middleware.proxy_fix import ProxyFix

if not os.getenv('API_TOKEN'):
    raise EnvironmentError("API_TOKEN não configurado no ambiente")

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def require_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.args.get('token')
        if not token or token != os.getenv('API_TOKEN'):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/profile', methods=['GET'])
@require_token
def get_profile():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Bad Request"}), 400
        
    try:
        loader = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(loader.context, username)
        
        return jsonify({
            "profile": {
                "username": profile.username,
                "full_name": profile.full_name,
                "profile_pic_url": profile.profile_pic_url,
                "followers": profile.followers,
                "followees": profile.followees,
            }
        })
    except:
        return jsonify({"error": "Not Found"}), 404

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=False
    )