import socket

from views import blog, index

URLS = {
    "/": index,
    "/blog": blog
}


def parse_request(request):
    parsed = request.split(" ")
    method = parsed[0]
    url = parsed[1]
    return (method, url)


def generate_heders(method, url):
    if not method == "GET":
        return ("HTTP/1.1 405 Method not allowed\n\n", 405)
    if url not in URLS:
        return ("HTTP/1.1 404 Not found\n\n", 404)
    return ("HTTP/1.1 200 OK\n\n", 200)


def generate_content(code, url):
    if code == 404:
        return "<H1>404</H1> <p>Not found</p>"
    if code == 405:
        return "<H1>405</H1> <p>Method not allowed</p>"
    return URLS[url]()


def generate_response(request):
    method, url = parse_request(request)
    headers, code = generate_heders(method, url)
    body = generate_content(code, url)
    return (headers + body).encode()


def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ip v4
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server_socket.bind(("localhost", 8000))
    server_socket.listen()

    while True:
        client_socket, addres = server_socket.accept()
        request = client_socket.recv(1024)
        response = generate_response(request.decode("utf-8"))
        client_socket.sendall(response)
        client_socket.close()


if __name__ == "__main__":
    run()
