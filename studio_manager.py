# @Time    : 2019/6/14 5:36 PM
# @Author  : 白尚林
# @File    : app
# @Use     :
"""
 A master server to manage all node by Flask
"""
from web_studio.server import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
