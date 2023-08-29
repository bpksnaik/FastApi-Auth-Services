from decouple import config

token_algo = config("TOKEN_ALGO")
db_name = config("DB_NAME")
user_collection_name = config("USER_COLLECTION_NAME")
movie_collection_name = config("MOVIE_COLLECTION_NAME")
mongo_url = config("MONGO_URL")
secret_key = config("SECRET_KEY")
redis_host = config("REDIS_HOST")
redis_port = config("REDIS_PORT")
