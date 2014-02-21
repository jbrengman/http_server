import socket
import os
import mimetypes


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 50000))
    s.listen(5)
    while (True):
        try:
            connection, address = s.accept()
            receive(connection)
        finally:
            connection.close()


def receive(connection):
    message = connection.recv(1024)
    if (message):
        handle(message, connection)
    if (not message):
        return


def handle(message, connection):
    request = get_request(message)
    request_split = split_request(request)
    method = get_method(request_split)
    uri = get_uri(request_split)
    try:
        check_method(method)
    except ValueError:
        response = build_response(
            '405 Method not allowed', '', '405 Method not allowed')
        send_response(response, connection)
    else:
        try:
            content, mimetype = get_content(uri)
        except ValueError:
            response = build_response('404 Not found', '', '404 Not found')
            send_response(response, connection)
        else:
            response = build_response('200 OK', mimetype, content)
            send_response(response, connection)


def get_request(message):
    return message.split('\r\n')[0]


def split_request(r):
    return r.split(' ')


def get_method(r):
    return r[0]


def get_uri(r):
    return r[1]


def check_method(m):
    if (m == 'GET'):
        return True
    else:
        raise ValueError('Invalid method')


def get_content(uri):
    path = '/home/jordan/webroot' + uri
    if (os.path.isdir(path)):
        content = '\r\n'.join(os.listdir(path))
        mimetype = '\r\nContent-Type: text/plain'
    elif (os.path.isfile(path)):
        mimetype = '\r\nContent-Type: ' + mimetypes.guess_type(uri)[0]
        with open(path, 'rb') as infile:
            content = infile.read()
    else:
        raise ValueError('404 File not found')
    return content, mimetype


def build_response(message, mimetype, content):
    return ('HTTP/1.1 ' + message + mimetype + '\r\n\r\n' + content)


def send_response(response, connection):
    connection.sendall(response)

if __name__ == '__main__':
    main()
