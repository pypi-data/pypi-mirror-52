from hashlib import sha1
import hmac

def get_signed_url(skey, resource_path, query_params):
    request = resource_path + "?"
    c = 0
    for qp in query_params:
        if c > 0:
            request = request + "&"
        (key, value) = qp
        request = request + "{key}={value}".format(key=key, value=value)
        c+=1
    hashed = hmac.new(skey, request.encode('utf-8'), sha1)
    signature = hashed.hexdigest()
    return signature