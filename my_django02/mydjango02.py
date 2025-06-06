# import sqlite3
import sys
import django
from django.db import models
from django.db.models import Q

# from django.db import connection
import requests
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import path


settings.configure(
    ROOT_URLCONF=__name__,
    DEBUG=True,
    SECRET_KEY="secret",
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "melon-20230906.sqlite3",
        }
    },
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": ["templates"],
        }
    ],
)
django.setup()


class Song(models.Model):
    id = models.AutoField(primary_key=True)
    가수 = models.CharField(max_length=100)
    곡명 = models.CharField(max_length=200)
    곡일련번호 = models.IntegerField()
    순위 = models.IntegerField()
    앨범 = models.CharField(max_length=200)
    좋아요 = models.IntegerField()
    커버이미지_주소 = models.URLField()

    def __str__(self):
        return self.곡명

    class Meta:
        db_table = "songs"
        app_label = "melon"


def index(request):
    # query = request.GET.get("query", "").strip()

    # song_list = Song.objects.all()
    # if query:
    #     # QuerySet 객체를 통해 조회조건을 추가할 수 있습니다.
    #     song_list = song_list.filter(
    #         Q(곡명__icontains=query) | Q(가수__icontains=query)
    #     )
    # song_list = get_song_list(query)
    # json_url = "https://raw.githubusercontent.com/pyhub-kr/dump-data/main/melon/melon-20230906.json"

    # response = requests.get(json_url)
    # # response.raise_for_status()  # 비정상 응답을 받았다면, HTTPError를 발생시킵니다.
    # if response.ok:
    #     song_list = response.json()
    # else:
    #     song_list = []

    # if query:
    #     song_list = filter(
    #         lambda song: query in song["가수"],
    #         song_list,
    #     )

    # song_list = response.json()
    # query = "Love"  # 검색어

    # song_list = [
    #     {"곡명": "Seven (feat. Latto) - Clean Ver.", "가수": "정국"},
    #     {"곡명": "Love Lee", "가수": "AKMU (악뮤)"},
    #     {"곡명": "Super Shy", "가수": "NewJeans"},
    #     {"곡명": "후라이의 꿈", "가수": "AKMU (악뮤)"},
    #     {"곡명": "어떻게 이별까지 사랑하겠어, 널 사랑하는 거지", "가수": "AKMU (악뮤)"},
    # ]
    # # 파이썬 빌트인 함수 filter를 활용해서, 곡명에 검색어가 포함된 노래만 필터링
    # song_list = filter(
    #     lambda song: query in song["가수"] or query in song["곡명"], song_list
    # )

    # song_list_data = list(song_list.values())

    return render(request, "index.html")


def song_list_api(request):
    query = request.GET.get("query", "").strip()

    song_list = Song.objects.all()
    if query:
        # QuerySet 객체를 통해 조회조건을 추가할 수 있습니다.
        song_list = song_list.filter(
            Q(곡명__icontains=query) | Q(가수__icontains=query)
        )

    song_list_data = list(song_list.values())

    return JsonResponse(
        song_list_data,
        safe=False,
        json_dumps_params={"ensure_ascii": False},
        content_type="application/json; charset=utf-8",
    )


# def get_song_list(query):
#     # connection = sqlite3.connect("melon-20230906.sqlite3")
#     cursor = connection.cursor()
#     # connection.set_trace_callback(print)

#     if query:
#         param = "%" + query + "%"
#         sql = "SELECT * FROM songs WHERE 가수 LIKE %s OR 곡명 LIKE %s"
#         cursor.execute(sql, [param, param])
#     else:
#         cursor.execute("SELECT * FROM songs")

#     column_names = [desc[0] for desc in cursor.description]
#     song_list = [
#         dict(zip(column_names, song_tuple)) for song_tuple in cursor.fetchall()
#     ]
#     connection.close()

#     return song_list
# connection = sqlite3.connect("melon-20230906.sqlite3")
# cursor = connection.cursor()
# if not query:
#     cursor.execute("SELECT * FROM songs")
# else:
#     sql = "SELECT * FROM songs WHERE 가수 LIKE ? OR 곡명 LIKE ?"
#     param = "%" + query + "%"
#     cursor.execute(sql, [param, param])

# column_names = [desc[0] for desc in cursor.description]
# song_list = [dict(zip(column_names, song)) for song in cursor.fetchall()]
# connection.close()

# return song_list


urlpatterns = [
    path("", index),
    path("api/song-list.json/", song_list_api),
]


execute_from_command_line(sys.argv)
