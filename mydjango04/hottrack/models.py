from __future__ import annotations
from django.utils.html import format_html

# from dataclasses import dataclass
from datetime import date
from typing import Dict
from urllib.parse import quote

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Song(models.Model):
    melon_uid = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(allow_unicode=True, blank=True)
    rank = models.PositiveSmallIntegerField()
    album_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    artist_name = models.CharField(max_length=100)
    cover_url = models.URLField()
    lyrics = models.TextField()
    genre = models.CharField(max_length=100)
    release_date = models.DateField()
    like_count = models.PositiveIntegerField()

    class Meta:
        indexes = [
            # 조회를 위해 인덱스를 추가합니다.
            models.Index(fields=["slug"]),
        ]

    def save(self, *args, **kwargs):
        # slug 필드는 name 필드에 의존적입니다.
        # slug 필드 값이 없는 경우에만 name 필드로부터 slug 필드를 채웁니다.
        self.slugify()
        super().save(*args, **kwargs)

    def slugify(self, force=False):
        if force or not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)

    def get_absolute_url(self) -> str:
        self.slugify()
        """Song 모델의 detail url을 계산하여 반환"""
        # slug = slugify(self.name, allow_unicode=True)
        return reverse(
            "hottrack:song_detail",
            args=[
                self.release_date.year,
                self.release_date.month,
                self.release_date.day,
                self.slug,
            ],
        )

    @property
    def cover_image_tag(self) -> str:
        return format_html("<img src={} />", self.cover_url)

    @property
    def melon_detail_url(self) -> str:
        song_id = quote(self.melon_uid)
        return f"https://www.melon.com/song/detail.htm?songId={song_id}"

    @property
    def youtube_search_url(self) -> str:
        search_query = quote(f"{self.name}, {self.artist_name}")
        return f"https://www.youtube.com/results?search_query={search_query}"

    @classmethod
    def from_dict(cls, data: Dict) -> Song:
        return cls(
            melon_uid=data.get("곡일련번호"),
            rank=int(data.get("순위")),
            album_name=data.get("앨범"),
            name=data.get("곡명"),
            artist_name=data.get("가수"),
            cover_url=data.get("커버이미지_주소"),
            lyrics=data.get("가사"),
            genre=data.get("장르"),
            release_date=date.fromisoformat(data.get("발매일")),
            like_count=int(data.get("좋아요")),
        )
