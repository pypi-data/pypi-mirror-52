from flask import request
from base_aios.utils.md5 import encrypt_sha256
from base_aios.utils.exceptions import UnauthorizedException

def verify_mutex_login(aios_redis, user_id, **kwargs):
    '''互斥登录校验，以异常的形式抛出
    '''
    assert user_id is not None, 'user_id is not none!'

    kwargs = kwargs or {}
    ACTIVE_KEY = kwargs.get('ACTIVE_KEY', 'bam:active:{}')
    TOOL_ACTIVE_KEY = kwargs.get('TOOL_ACTIVE_KEY', 'bam:tool_active:{}')
    MUTEX_LOGIN = kwargs.get('MUTEX_LOGIN', '您的账号在另一地点登录, 您已被迫下线!')
    
    # 请求来源，默认是web页面
    source = request.headers.get('source', 'web')
    key = ACTIVE_KEY if source == 'web' else TOOL_ACTIVE_KEY

    current_access_token = request.headers.get('Authorization')
    # 本次请求的加密token
    actual_access_token = encrypt_sha256(current_access_token.replace('Bearer ', ''))
    # 缓存中期望的加密token
    except_access_token = aios_redis.get(key.format(user_id))
    if except_access_token is None:
        # 缓存失效时更新缓存
        aios_redis.set(key.format(user_id), actual_access_token)
        except_access_token = actual_access_token

    if isinstance(except_access_token, bytes):
        except_access_token = except_access_token.decode()
        
    if except_access_token != actual_access_token:
        raise UnauthorizedException(MUTEX_LOGIN)