# @Time    : 2019/7/17 1:06 PM
# @Author  : 白尚林
# @File    : agent
# @Use     :
"""
 A agent to manage worker node by Flask
 1. 启动、停止、查询 工作进程 -> (下载器、解析器)
 2. 节点、工作进程探活
"""
from agent.server import CreateApp

app = CreateApp().app()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
