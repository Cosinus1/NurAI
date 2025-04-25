#!/usr/bin/env python
import os
from app import create_app

app_env = os.environ.get('FLASK_ENV', 'default')
app = create_app(app_env)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=(app_env != 'production'))