"""
高山市暮らし応援商品券 加盟店一覧 データ更新スクリプト

使い方:
    python scripts/update_data.py

高山市公式サイトのページからCSVのURLを自動検出し、
data/stores.json として保存します。
"""

import csv
import io
import json
import os
import re
import sys
from urllib.parse import urljoin

import requests

# 加盟店一覧ページのURL（CSVのリンクをここから自動検出する）
PAGE_URL = "https://www.city.takayama.lg.jp/shisei/1000067/1004674/1023161.html"

# 出力先（このスクリプトの親ディレクトリ/data/stores.json）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "data", "stores.json")


def find_csv_url():
    """ページのHTMLからCSVファイルのURLを探して返す"""
    print(f"ページを確認中: {PAGE_URL}")
    response = requests.get(PAGE_URL, timeout=30)
    response.raise_for_status()

    # href="...*.csv" のリンクをすべて探す
    matches = re.findall(r'href="([^"]+\.csv)"', response.text)
    if not matches:
        raise RuntimeError("ページ内にCSVファイルのリンクが見つかりませんでした")

    # 相対URLも絶対URLも正しく解決する
    csv_url = urljoin(PAGE_URL, matches[0])
    return csv_url


def fetch_stores():
    """CSVをShift-JISで取得し、辞書のリストを返す"""
    csv_url = find_csv_url()
    print(f"CSVを取得中: {csv_url}")
    response = requests.get(csv_url, timeout=30)
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
