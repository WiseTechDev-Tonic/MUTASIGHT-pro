from app import app, socketio
import logging

if __name__ == "__main__":
    logging.info("Starting MutaSight AI Drug Discovery Platform")
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
