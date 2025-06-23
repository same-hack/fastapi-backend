from fastapi import APIRouter, UploadFile, File, Form
import os
from datetime import datetime
import shutil  # ✅ チャンクディレクトリ削除用
import boto3   # ✅ MinIO（S3互換）用ライブラリ

# =============================
# ✅ APIRouter の設定
# =============================
router = APIRouter(
    prefix="/upload",         # すべてのルートに /upload が付く
    tags=["Upload"],          # ドキュメント用タグ
)

# =============================
# ✅ 保存ディレクトリの設定
# =============================
UPLOAD_DIR = "./fastapi_data"  # FastAPI用
CHUNKS_DIR = os.path.join(UPLOAD_DIR, "chunks")
MERGED_DIR = UPLOAD_DIR

os.makedirs(UPLOAD_DIR, exist_ok=True)               # なければ作成
os.makedirs(CHUNKS_DIR, exist_ok=True)

# =============================
# ✅ MinIO (S3互換) クライアントの設定
# =============================
# MinIO用エンドポイントなどを環境変数や設定ファイルから読み込んでもOK
s3_client = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",  # MinIO のエンドポイント
    aws_access_key_id="minioadmin",        # アクセスキー（MinIOデフォルト）
    aws_secret_access_key="minioadmin",    # シークレットキー（MinIOデフォルト）
    region_name="us-east-1",               # ダミーでもOK（S3互換用）
)

# =============================
# ✅ 通常アップロード（1回で送信）
# =============================
@router.post("", summary="ファイルアップロード（末尾スラッシュなし）")
@router.post("/", summary="ファイルアップロード（末尾スラッシュあり）")
async def upload_file(file: UploadFile = File(...)):
    """
    単発ファイルアップロード。ファイル名に日付プレフィックスを付けて保存。
    """
    date_prefix = datetime.now().strftime("%Y%m%d")
    filename = f"{date_prefix}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "filename": filename,
        "message": "ファイルを保存しました"
    }

# =============================
# ✅ 分割アップロード用エンドポイント
# =============================
@router.post("/chunk", summary="分割アップロード（チャンク方式）")
async def upload_chunk(
    chunk: UploadFile = File(...),       # チャンクそのもの
    fileName: str = Form(...),           # 元のファイル名
    uploadId: str = Form(...),           # アップロードセッションID
    chunkIndex: int = Form(...),         # チャンク番号（0始まり）
    totalChunks: int = Form(...)         # チャンクの総数
):
    """
    分割アップロード用。チャンクを一時保存し、全チャンク受信後に結合し、MinIOにPOST。
    """

    # ==================================
    # ✅ チャンクを一時保存
    # ==================================
    chunk_dir = os.path.join(CHUNKS_DIR, uploadId)
    os.makedirs(chunk_dir, exist_ok=True)

    chunk_path = os.path.join(chunk_dir, f"{chunkIndex}.part")
    with open(chunk_path, "wb") as f:
        f.write(await chunk.read())

    # ==================================
    # ✅ 全チャンクが揃っていれば結合
    # ==================================
    all_received = all(os.path.exists(os.path.join(chunk_dir, f"{i}.part")) for i in range(totalChunks))
    if all_received:
        date_prefix = datetime.now().strftime("%Y%m%d")
        final_file_name = f"{date_prefix}_{fileName}"
        final_file_path = os.path.join(MERGED_DIR, final_file_name)

        # ✅ チャンク結合
        with open(final_file_path, "wb") as final_file:
            for i in range(totalChunks):
                part_path = os.path.join(chunk_dir, f"{i}.part")
                with open(part_path, "rb") as part:
                    final_file.write(part.read())

        # ==================================
        # ✅ MinIO へアップロード
        # ==================================
        bucket_name = "uploads"
        object_key = final_file_name

        # バケットが存在しなければ作成（既に存在していれば何もしない）
        try:
            s3_client.head_bucket(Bucket=bucket_name)
        except s3_client.exceptions.ClientError:
            s3_client.create_bucket(Bucket=bucket_name)

        # ファイルをMinIOへアップロード（ローカル→S3）
        s3_client.upload_file(final_file_path, bucket_name, object_key)

        # ==================================
        # ✅ ローカルファイル削除
        # ==================================
        os.remove(final_file_path)          # 結合後の一時ファイルを削除
        shutil.rmtree(chunk_dir)            # チャンクも削除（ディレクトリごと）

        # ==================================
        # ✅ レスポンス返却
        # ==================================
        return {
            "filename": final_file_name,
            "message": "すべてのチャンクを結合し、MinIO にアップロードしました",
            "minio_url": f"s3://{bucket_name}/{object_key}"
        }

    # チャンク受信中の応答（結合にはまだ到達していない）
    return {
        "chunkIndex": chunkIndex,
        "message": "チャンクを保存しました（まだ結合はしていません）"
    }
