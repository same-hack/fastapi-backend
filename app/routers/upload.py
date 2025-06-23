from fastapi import APIRouter, UploadFile, File, Form
import os
from datetime import datetime

# =============================
# ✅ APIRouter の設定
# =============================
router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)

# =============================
# ✅ 保存ディレクトリの設定
# =============================
UPLOAD_DIR = "./data"
CHUNKS_DIR = os.path.join(UPLOAD_DIR, "chunks")
MERGED_DIR = UPLOAD_DIR  # 結合後のファイルも ./data に置く

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CHUNKS_DIR, exist_ok=True)

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
    chunk: UploadFile = File(...),
    fileName: str = Form(...),
    uploadId: str = Form(...),
    chunkIndex: int = Form(...),
    totalChunks: int = Form(...)
):
    """
    分割アップロード用。チャンクを一時保存し、全チャンク受信後に結合する。
    """
    chunk_dir = os.path.join(CHUNKS_DIR, uploadId)
    os.makedirs(chunk_dir, exist_ok=True)

    chunk_path = os.path.join(chunk_dir, f"{chunkIndex}.part")
    with open(chunk_path, "wb") as f:
        f.write(await chunk.read())

    # 全チャンクが揃ったらファイルを結合
    all_received = all(os.path.exists(os.path.join(chunk_dir, f"{i}.part")) for i in range(totalChunks))
    if all_received:
        date_prefix = datetime.now().strftime("%Y%m%d")
        final_file_name = f"{date_prefix}_{fileName}"
        final_file_path = os.path.join(MERGED_DIR, final_file_name)

        with open(final_file_path, "wb") as final_file:
            for i in range(totalChunks):
                part_path = os.path.join(chunk_dir, f"{i}.part")
                with open(part_path, "rb") as part:
                    final_file.write(part.read())

        # チャンクファイルの削除（任意）
        # import shutil
        # shutil.rmtree(chunk_dir)

        return {
            "filename": final_file_name,
            "message": "すべてのチャンクを受信し、結合が完了しました"
        }

    return {
        "chunkIndex": chunkIndex,
        "message": "チャンクを保存しました"
    }
