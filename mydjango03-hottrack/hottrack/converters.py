from datetime import date
from django.urls import register_converter


class DateConverter:
    regex = r"20\d{2}/([1-9]|0[1-9]|1[0-2]){1,2}/([1-9]|0[1-9]|[12][0-9]|3[01]){1,2}"

    # 뷰 함수에 넘기기 전에 date 객체로 변환
    #  - ex) "2023/12/25" -> date(2023, 12, 25)
    def to_python(self, value: str) -> date:
        year, month, day = map(int, value.split("/"))
        return date(year, month, day)

    def to_url(self, value: date) -> str:
        return f"{value.year}/{value.month:02d}/{value.day:02d}"


# DateConverter를 등록합니다.
register_converter(DateConverter, "date")
