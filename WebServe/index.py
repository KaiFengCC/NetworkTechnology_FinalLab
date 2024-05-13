from flask import Flask, render_template, request
import Spider.spider as spider  # 导入你的爬虫程序

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')  # 返回主页

@app.route('/start_spider', methods=['POST'])
def start_spider():
    spider.main()  # 启动爬虫程序
    return '爬虫程序已启动'

if __name__ == '__main__':
    app.run()