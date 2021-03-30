MalformedRequestError = 'malformed request'


def get_authorization_header(header):
    if 'Authorization' not in header:
        return MalformedRequestError
    if header['Authorization'].split()[0] != 'Bearer':
        return MalformedRequestError
    return header['Authorization'].split()[1]
