from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import boto3
import uuid
from botocore.client import Config

# =============================
# 🎯 このAPIはマルチパートアップロードの管理API
# - フロントからアップロード準備・URL発行・完了指示を受ける
# - ファイルデータ自体はpresigned URL経由で直接MinIOに送信される
# =============================

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)

# =============================
# ✅ MinIOクライアント設定（S3互換）
# - boto3で MinIO に接続するためのクライアントを作成
# - v4署名を使用（presigned URL に必要）
# =============================
s3_client = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",  # MinIOのエンドポイント
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
    region_name="us-east-1",
    config=Config(signature_version='s3v4')  # presigned URLに必要
)

BUCKET_NAME = "tmp"

# =============================
# ✅ バケット存在確認＆作成（初回用）
# - 指定したバケットが無ければ作成
# =============================
try:
    s3_client.head_bucket(Bucket=BUCKET_NAME)
except s3_client.exceptions.ClientError:
    s3_client.create_bucket(Bucket=BUCKET_NAME)


# =============================
# 📦 リクエストボディ定義
# =============================
class StartUploadRequest(BaseModel):
    fileName: str  # ファイル名のみ（MinIO上のオブジェクト名）


class PresignRequest(BaseModel):
    uploadId: str      # アプリ側で発行したアップロードセッションID
    chunkIndex: int    # チャンク番号（0始まり）
    fileName: str      # ファイル名（確認用）


class CompleteUploadRequest(BaseModel):
    uploadId: str
    fileName: str
    parts: list[dict]  # 完了時に必要なETag+PartNumberのリスト


# =============================
# 🧠 簡易的なアップロード状態管理ストア
# - uploadId → MultipartUpload情報（UploadId, Key, Parts[]）
# - 本番ではRedisやDBを使って永続化すべき
# =============================
UPLOADS = {}  # uploadId -> {"UploadId": ..., "Key": ..., "Parts": [...]}


# =============================
# 🚀 アップロード開始エンドポイント
# - フロントからファイル名を受け取り
# - MinIOに対して create_multipart_upload を実行
# - アプリ側の uploadId を返す
# =============================
@router.post("/start")
async def start_upload(req: StartUploadRequest):
    try:
        # MinIO（S3）側にマルチパートアップロード開始を通知
        s3_resp = s3_client.create_multipart_upload(
            Bucket=BUCKET_NAME,
            Key=req.fileName
        )

        # アプリケーション側で独自のuploadIdを発行
        upload_id = str(uuid.uuid4())

        # メモリストアにアップロードセッションを登録
        UPLOADS[upload_id] = {
            "UploadId": s3_resp["UploadId"],  # S3用の本物のID
            "Key": req.fileName,              # ファイル名（S3上のキー）
            "Parts": []                       # 完了時に使うPart情報リスト
        }

        # フロントにuploadIdを返す
        return {"uploadId": upload_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================
# 🔐 presigned URL 発行エンドポイント
# - 各チャンクのアップロードURLを発行
# - フロントはこのURLに対して直接PUTアップロード
# =============================
@router.post("/presign")
async def presign_chunk(req: PresignRequest):
    if req.uploadId not in UPLOADS:
        raise HTTPException(status_code=404, detail="Invalid uploadId")

    upload_data = UPLOADS[req.uploadId]

    try:
        # boto3で一時的な署名付きPUT URLを発行（PartNumberは1始まり）
        url = s3_client.generate_presigned_url(
            ClientMethod="upload_part",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": upload_data["Key"],
                "UploadId": upload_data["UploadId"],
                "PartNumber": req.chunkIndex + 1
            },
            ExpiresIn=3600,
            HttpMethod="PUT"
        )

        return {
            "url": url,  # フロントはこのURLに対して直接PUTする
            "partNumber": req.chunkIndex + 1
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================
# ✅ アップロード完了エンドポイント
# - フロントが全てのチャンクをアップロード後に呼び出す
# - partNumberとETagのリストを受け取り、アップロードを確定する
# =============================
@router.post("/complete")
async def complete_upload(req: CompleteUploadRequest):
    if req.uploadId not in UPLOADS:
        raise HTTPException(status_code=404, detail="Invalid uploadId")

    upload_data = UPLOADS[req.uploadId]

    try:
        # MinIOに対してアップロード完了を通知
        s3_client.complete_multipart_upload(
            Bucket=BUCKET_NAME,
            Key=upload_data["Key"],
            UploadId=upload_data["UploadId"],
            MultipartUpload={
                "Parts": req.parts  # 例: [{"PartNumber": 1, "ETag": "xxxxx"}, ...]
            }
        )

        # セッション情報を削除
        del UPLOADS[req.uploadId]

        return {
            "message": "アップロード完了",
            "url": f"s3://{BUCKET_NAME}/{upload_data['Key']}"  # 完成したファイルのS3 URL
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
