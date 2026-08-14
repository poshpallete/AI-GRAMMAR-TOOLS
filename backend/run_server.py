#!/usr/bin/env python3
# =========================================
# SERVER STARTUP SCRIPT
# =========================================

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from app import app, init_db

if __name__ == "__main__":
    init_db()
    port = int(os.getenv('PORT', 5000))
    print("====================================")
    print(f"  AI Writing System Started!")
    print(f"  Open: http://127.0.0.1:{port}")
    print("====================================")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False, threaded=True)
