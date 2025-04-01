import sqlite3

query = "1' OR 1==1 --"

print("검색어:", query)

connection = sqlite3.connect("melon-20230906.sqlite3")
cursor = connection.cursor()
connection.set_trace_callback(print)

param = "%" + query + "%"
# sql = f"SELECT * FROM songs WHERE 가수 LIKE '{param}' OR 곡명 LIKE '{param}'"
# cursor.execute(sql)

sql = "SELECT * FROM songs WHERE 가수 LIKE ? OR 곡명 LIKE ?"
param = "%" + query + "%"
cursor.execute(sql, [param, param])

column_names = [desc[0] for desc in cursor.description]

song_list = cursor.fetchall()
# 각 행은 tuple 타입으로 조회됩니다.

print("list size :", len(song_list))

for song_tuple in song_list:
    song_dict = dict(zip(column_names, song_tuple))
    # 사전
    print(song_dict["곡명"], song_dict["가수"])
connection.close()
