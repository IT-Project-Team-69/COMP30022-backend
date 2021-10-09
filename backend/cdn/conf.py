import environ

env = environ.Env()
environ.Env.read_env()

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'it-project'
AWS_S3_ENDPOINT_URL = 'https://sgp1.digitaloceanspaces.com'

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400"
}
AWS_LOCATION = "https://it-project.sgp1.digitaloceanspaces.com"

DEFAULT_FILE_STORAGE = 'backend.cdn.backends.MediaRootS3Boto3Storage'
STATIC_FILE_STORAGE = 'backend.cdn.backends.StaticRootS3Boto3Storage'
