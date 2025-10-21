import time

start_time = time.time()

def get_status():
    """
    Returns the API status, name, version, and uptime in seconds.
    """
    from main import app  # Import here to avoid circular import
    uptime = int(time.time() - start_time)
    return {
        "msg": "API status 🚀",
        "name": "timestamp-api",
        "version": app.version,
        "uptime": uptime,
    }
