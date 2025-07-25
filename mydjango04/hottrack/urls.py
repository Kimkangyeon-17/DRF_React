from django.urls import path, re_path
from . import views
from . import converters  # noqa

app_name = "hottrack"

urlpatterns = [
    path(route="", view=views.index, name="index"),
    path("<int:pk>/", view=views.song_detail, name="song_detail"),
    path(route="melon-<int:melon_uid>/", view=views.song_detail, name="song_detail"),
    # path(route="archives/<date:release_date>/", view=views.index),
    re_path(
        route=r"^export\.(?P<format>(csv|xlsx))$", view=views.export, name="export"
    ),
    path(route="<int:pk>/cover.png", view=views.cover_png, name="cover_png"),
    path(
        route="archives/<int:year>/",
        view=views.SongYearArchiveView.as_view(),
        name="song_archive_year",
    ),
    path(
        route="archives/<int:year>/<int:month>/",
        view=views.SongMonthArchiveView.as_view(),
        name="song_archive_month",
    ),
    path(
        route="archives/<int:year>/<int:month>/<int:day>/",
        view=views.SongDayArchiveView.as_view(),
        name="song_archive_day",
    ),
    path(
        route="archives/today/",
        view=views.SongTodayArchiveView.as_view(),
        name="song_archive_today",
    ),
    path(
        route="archives/<int:year>/week/<int:week>/",
        view=views.SongWeekArchiveView.as_view(),
        name="song_archive_week",
    ),
    re_path(
        route=r"^archives/(?P<date_list_period>year|month|day|week)?/?$",
        view=views.SongArchiveIndexView.as_view(),
        name="song_archive_index",
    ),
    # path(
    #     route="<int:year>/<int:month>/<int:day>/<int:pk>/",
    #     view=views.SongDateDetailView.as_view(),
    #     name="song_date_detail",
    # ),
    re_path(
        r"^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$",
        view=views.SongDateDetailView.as_view(),
        name="song_detail",
    ),
]
