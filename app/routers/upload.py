from fastapi import APIRouter, UploadFile, File
import os
from datetime import datetime

# =============================
# ✅ APIRouter の設定
# =============================
# このルーターは /upload 以下のルートを担当
router = APIRouter(
    prefix="/upload",         # すべてのルートの前に /upload が付く
    tags=["Upload"],          # ドキュメント上のグルーピング用タグ
)

# =============================
# ✅ 保存ディレクトリの設定
# =============================
# アップロードされたファイルを保存するディレクトリ
UPLOAD_DIR = "./data"

# ディレクトリが存在しない場合は自動で作成（なければ例外になるため）
os.makedirs(UPLOAD_DIR, exist_ok=True)

# =============================
# ✅ ファイルアップロードエンドポイント
# =============================
# トレイリングスラッシュの有無に対応（どちらでも動作するように2つ定義）
@router.post("", summary="ファイルアップロード（末尾スラッシュなし）")
@router.post("/", summary="ファイルアップロード（末尾スラッシュあり）")
async def upload_file(file: UploadFile = File(...)):
    """
    クライアントから送信されたファイルを受け取り、`./data` フォルダに保存する。
    ファイル名の先頭には現在日付（YYYYMMDD）をプレフィックスとして付与する。
    """

    # 現在の日付を YYYYMMDD 形式で取得
    date_prefix = datetime.now().strftime("%Y%m%d")

    # オリジナルファイル名の前に日付を付与（例: 20250617_myfile.csv）
    filename = f"{date_prefix}_{file.filename}"

    # 保存先パスを生成
    file_path = os.path.join(UPLOAD_DIR, filename)

    # ファイルの内容をバイナリ書き込みモードで保存
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # 保存完了のレスポンスを返却
    return {
        "filename": filename,
        "message": "ファイルを保存しました"
    }
