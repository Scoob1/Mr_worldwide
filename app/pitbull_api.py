from flask import Flask, jsonify, request
import mysql.connector
from flask_caching import Cache
from flask_rq2 import RQ
import redis
from rq.job import Job

app = Flask(__name__)
app.config['RQ_REDIS_URL'] = 'redis://localhost:6379/0'

# Basic cache config
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)
rq = RQ(app)

# background jobs
@rq.job
def generate_playlist(length):
    return [f"Track {i+1}" for i in range(length)]

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="0Akley11",
        database="mr_worldwide"
    )

@app.route("/")
def home():
    return {"message": "Mr._Worldwide API – Dale!"}

@app.route("/albums", methods=["GET"])
@cache.cached(timeout=300)  # cache for 5 minutes
def get_albums():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM albums")
    albums = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(albums)

@app.route("/tracks", methods=["GET"])
def get_tracks():
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)
    offset = (page - 1) * limit
    year = request.args.get("year")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if year:
        cursor.execute("""
            SELECT t.* FROM tracks t
            JOIN albums a ON t.album_id = a.id
            WHERE YEAR(a.release_date) = %s
            LIMIT %s OFFSET %s
        """, (year, limit, offset))
    else:
        cursor.execute("""
                       SELECT * FROM tracks
                       LIMIT %s OFFSET %s
                       """, (limit, offset))

    tracks = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({
        "page": page,
        "limit": limit,
        "results": tracks
    })

@app.route("/playlist", methods=["GET"])
@cache.cached(timeout=300, query_string=True)  # cache based on query params
def get_playlist():
    limit = request.args.get("limit", 10)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tracks ORDER BY RAND() LIMIT %s", (int(limit),))
    playlist = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(playlist)

@app.route("/queue/playlist", methods=["GET"])
def queue_playlist():
    length = int(request.args.get("length", 10))
    job = generate_playlist.queue(length)
    return jsonify({"job_id": job.id, "status": "Queued"})

@app.route("/queue/status/<job_id>", methods=["GET"])
def check_job_status(job_id):
    conn = redis.Redis()
    job = Job.fetch(job_id, connection=conn)

    if job.is_finished:
        return jsonify({"status": "done", "playlist": job.result})
    elif job.is_failed:
        return jsonify({"status": "failed"})
    else:
        return jsonify({"status": "processing"})

if __name__ == "__main__":
    app.run(debug=True)

