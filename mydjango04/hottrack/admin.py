from django.utils.html import format_html
from django.contrib import admin
from .models import Song
from .utils.melon import get_likes_dict


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    search_fields = ["name", "artist_name", "album_name"]

    list_display = [
        "cover_image_tag",
        "name",
        "artist_name",
        "album_name",
        "genre",
        "like_count",
        "release_date",
    ]
    list_filter = ["genre", "release_date"]
    actions = ["update_like_count"]

    def update_like_count(self, request, queryset):
        melon_uid_list = queryset.values_list("melon_uid", flat=True)
        likes_dict = get_likes_dict(melon_uid_list)
        print("likes_dict", likes_dict)

        changed_count = 0
        for song in queryset:
            if song.like_count != likes_dict.get(song.melon_uid):
                song.like_count = likes_dict.get(song.melon_uid)
                # song.save() # 모델의 모든 필드에 대해서 업데이트를 수행
                song.save(update_fields=["like_count"])
                changed_count += 1
            # song.save()
        # Song.objects.bulk_update(queryset, fields=["like_count"])

        self.message_user(request, f"{changed_count} 곡의 좋아요 갱신 완료")

    # def cover_image(self, song):
    #     return format_html("<img src={} />", song.cover_url)


# admin.site.register(Song, SongAdmin)
