"""
高山市暮らし応援商品券 加盟店一覧 データ更新スクリプト

使い方:
    python scripts/update_data.py

高山市公式サイトのCSV（Shift-JIS）を取得し、
data/stores.json として保存します。
"""

import csv
import io
import json
import os
import sys

import requests

# CSVファイルのURL（高山市公式サイト）
CSV_URL = "https://www.city.takayama.lg.jp/_res/projects/default_project/_page_/001/023/161/kameitenichiran.csv"

# 出力先（このスクリプトの親ディレクトリ/data/stores.json）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "data", "stores.json")


def fetch_stores():
    """CSVをShift-JISで取得し、辞書のリストを返す"""
    print(f"CSVを取得中: {CSV_URL}")
    response = requests.get(CSV_URL, timeout=30)
    response.raise_for_status()
    response.encoding = "cp932"

    reader = csv.DictReader(io.StringIO(response.text))
    stores = []
    for row in reader:
        stores.append({
            "name":            row.get("屋号・商号", "").strip(),
            "name_kana":       row.get("屋号・商号フリガナ", "").strip(),
            "category_large":  row.get("業種（大分類）", "").strip(),
            "category_medium": row.get("業種（中分類）", "").strip(),
            "items":           row.get("主な取扱品目", "").strip(),
            "area":            row.get("地域", "").strip(),
            "zip":             row.get("郵便番号", "").strip(),
            "address":         row.get("住所", "").strip(),
            "tel":             row.get("電話番号", "").strip(),
            "sarubobo":        row.get("さるぼぼコイン", "").strip(),
        })

    print(f"取得完了: {len(stores)}件")
    return stores


def save_json(stores, path):
    """リストをJSONファイルに保存する"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)
    print(f"保存完了: {os.path.abspath(path)}")


def main():
    try:
        stores = fetch_stores()
        save_json(stores, OUTPUT_PATH)
    except requests.RequestException as e:
        print(f"エラー: CSVの取得に失敗しました: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
