'''
pip install pyjwt  (2.8.0)
'''
import time

import jwt

JWT_TOKEN_EXPIRE_SECONDS = 3600 * 2  # token有效时间 2小时
JWT_TOKEN_SECRET_SALT = 'sdftest'
JWT_TOKEN_ALGORITHM = 'HS256'  # HASH算法


def generate_jwt_token(user):
    """根据用户id生成token"""
    data = {'user_id': user, 'exp': int(time.time()) + JWT_TOKEN_EXPIRE_SECONDS}
    print("generate data:", data)
    jwtToken = jwt.encode(data, JWT_TOKEN_SECRET_SALT, algorithm=JWT_TOKEN_ALGORITHM)
    return jwtToken


def verify_jwt_token(user, jwtToken):
    """验证用户token"""
    print(user)
    data = {'user_id': user}
    try:
        payload = jwt.decode(
            jwtToken, JWT_TOKEN_SECRET_SALT, algorithms=[JWT_TOKEN_ALGORITHM]
        )
        print("verify:", payload)
        exp = int(payload.pop('exp'))
        if time.time() > exp:
            print('已失效')
            return False
        return data == payload
    except jwt.exceptions.ExpiredSignatureError as ex:
        print('token签名过期:', ex)
    except jwt.PyJWTError as ex:
        print('token解析失败:', ex)
    return False


if __name__ == '__main__':
    '''

    https://www.jb51.net/python/2852675y0.htm

    AttributeError: module 'jwt' has no attribute 'encode'

    '''
    # generate_jwt_token('user')

    aa = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidXNlciIsImV4cCI6MTY4OTg0ODQyMH0.jx1qEhWA4dv_WK48jiSxBFIyWfAqhpEcLfXjPsUP3mw'
    verify_jwt_token('usseasdasdr', aa)
