from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


@api_view(["GET"])
@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
@renderer_classes((JSONRenderer,))
def asked_get_user_information(requset, userid):
    import requests

    url = f"https://asked.kr/query.php?query=4&id={userid}"
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        },
    )
    return Response(response.text, response.status_code)


@api_view(["GET"])
@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
@renderer_classes((JSONRenderer,))
def asked_get_posts(requset, page, userid):
    import requests

    url = f"https://asked.kr/query.php?query=1&page={str(page)}&id={userid}"
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        },
    )
    response.encoding = "utf-8"
    return Response(response.text, response.status_code)


@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
@renderer_classes((JSONRenderer,))
def asked_post_ask(requset):
    import requests

    url = f"https://asked.kr/query.php?query=0"
    response = requests.post(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        },
        data=requset.body.decode("utf-8").encode("utf-8"),
    )

    return Response(response.text, response.status_code)
