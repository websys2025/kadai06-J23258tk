import requests
import pandas as pd

# -----------------------------------------------
# 参照するオープンデータの情報（e-Stat API）
#
# 名称：e-Stat（政府統計の総合窓口）統計データAPI
# 概要：日本政府が提供する各種統計情報にアクセス可能なオープンデータAPI。
#       このコードでは「人口総数（A1101）」のデータを取得している。
#
# エンドポイントと機能：
# URL: https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData
# 機能：統計表ID（statsDataId）を指定して、対応する統計データをJSON形式で取得できる。
#
# 使い方：
# - appId（APIキー）を取得して指定する（登録制）
# - statsDataId で対象の統計表を選ぶ（今回は「0000020201」＝国勢調査 人口等基本集計）
# - cdArea で地域コードを指定（ここでは千葉県の複数市）
# - cdCat01 で統計項目コードを指定（A1101＝人口総数）
# - その他、メタ情報や注釈、単位などの取得フラグも指定可能
# -----------------------------------------------

APP_ID = "d2c7e1e1bb598abd877b15f77f5029dbe95565b1"
API_URL = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

params = {
    "appId": APP_ID,
    "statsDataId": "0000020201",  # 統計表ID：国勢調査（人口等基本集計）
    "cdArea": "12101,12102,12103,12104,12105,12106",  # 地域コード（千葉県内の市）
    "cdCat01": "A1101",  # 統計項目：人口総数
    "metaGetFlg": "Y",  # メタ情報の取得
    "cntGetFlg": "N",   # 件数取得はしない
    "explanationGetFlg": "Y",  # 説明の取得
    "annotationGetFlg": "Y",   # 注釈の取得
    "sectionHeaderFlg": "1",   # セクションヘッダーの出力
    "replaceSpChars": "0",     # 特殊文字を置換しない
    "lang": "J"  # 日本語で取得
}

# APIへGETリクエストを送信
response = requests.get(API_URL, params=params)

# JSON形式でレスポンスを取得
data = response.json()

# 統計データ本体を取得（人口の数値など）
values = data['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE']

# pandasのDataFrameに変換
df = pd.DataFrame(values)

# メタ情報の取得（各コードの意味を名称に置換するため）
meta_info = data['GET_STATS_DATA']['STATISTICAL_DATA']['CLASS_INF']['CLASS_OBJ']

# 各カテゴリのIDを対応する名称に変換
for class_obj in meta_info:
    column_name = '@' + class_obj['@id']
    id_to_name_dict = {}
    
    # CLASSがリストか単体かで処理を分ける
    if isinstance(class_obj['CLASS'], list):
        for obj in class_obj['CLASS']:
            id_to_name_dict[obj['@code']] = obj['@name']
    else:
        id_to_name_dict[class_obj['CLASS']['@code']] = class_obj['CLASS']['@name']
    
    # IDを名称に変換
    df[column_name] = df[column_name].replace(id_to_name_dict)

# 列名の日本語化
col_replace_dict = {'@unit': '単位', '$': '値'}
for class_obj in meta_info:
    org_col = '@' + class_obj['@id']
    new_col = class_obj['@name']
    col_replace_dict[org_col] = new_col

# 列名の変換適用
new_columns = []
for col in df.columns:
    if col in col_replace_dict:
        new_columns.append(col_replace_dict[col])
    else:
        new_columns.append(col)

df.columns = new_columns

# 結果を出力
print(df)
                                                                                                    9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;///////////////////////////////////////////,