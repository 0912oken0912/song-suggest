from flask import Flask, render_template, request
from model import find_best_match_song

# Flaskアプリケーションの初期化
app = Flask(__name__)

# トップページ (/) の処理
@app.route('/')
def home():
    # home.html を表示する
    return render_template('home.html')

# 結果表示ページ (/result) の処理
@app.route('/result', methods=['POST'])
def result():
    # フォームからユーザーの入力を受け取る
    user_text = request.form['user_text']
    
    # model.pyの関数を呼び出し、結果を受け取る
    result = find_best_match_song(user_text)
    
    # result.html に計算結果を渡して表示する
    return render_template('result.html', 
                           song_name = result['song_name'], 
                           score = result['score'],
                           extract = result['text'],
                           user_text = user_text)

# アプリケーションの実行
if __name__ == '__main__':
    app.run(debug=True)