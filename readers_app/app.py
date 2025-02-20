from models import *
from function import *

# end of methods 
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    # app.run(debug=True, port=5000, host='0.0.0.0')
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    