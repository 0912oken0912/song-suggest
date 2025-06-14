import json
import MeCab
from collections import Counter

def extract_keywords(text, top_n=50, stop_words=None):
    """MeCabを使ってテキストからキーワードを抽出する関数"""
    if stop_words is None:
        stop_words = ['こと', 'する', 'いる', 'なる', '思う', 'られる', 'の', 'もの', 'よう', 'みたい', 'さん', 'これ', 'それ', 'あれ', '言う', 'くださる', 'おる', 'いく', 'くる']
        
    mecab = MeCab.Tagger()
    node = mecab.parseToNode(text)
    
    keywords = []
    while node:
        features = node.feature.split(',')
        part_of_speech = features[0]
        
        if part_of_speech in ['名詞', '動詞', '形容詞']:
            base_form = features[6] if len(features) > 6 and features[6] != '*' else node.surface
            if base_form not in stop_words:
                keywords.append(base_form)
        node = node.next
        
    counter = Counter(keywords)
    top_keywords = [word for word, freq in counter.most_common(top_n)]
    return top_keywords

def jaccard_similarity(set1, set2):
    """2つのセットのジャカード係数を計算する"""
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

# このモジュールがインポートされた際に、キーワードDBを一度だけ読み込む
with open('song_keywords.json', 'r', encoding='utf-8') as f:
    SONG_KEYWORDS_DB = json.load(f)
print("model.py: キーワードDBの読み込みが完了しました。")


def find_best_match_song(user_text):
    """
    ユーザーの入力テキストを受け取り、最も類似度の高い曲とスコアを返すメイン関数。
    app.pyからはこの関数だけを呼び出す。
    """
    # ユーザー入力からキーワードを抽出
    user_keywords = set(extract_keywords(user_text, top_n=50))
    
    # 各曲との類似度を計算
    scores = {}
    for song_name, keywords in SONG_KEYWORDS_DB.items():
        song_keywords_set = set(keywords)
        similarity = jaccard_similarity(user_keywords, song_keywords_set)
        scores[song_name] = similarity
        
    # 最も類似度が高い曲を見つける
    if not scores:
        best_song = "見つかりませんでした"
        best_score = 0
    else:
        best_song = max(scores, key=scores.get)
        best_score = scores[best_song]

    # 結果を辞書として返す
    return {
        'song_name': best_song,
        'score': best_score,
        'text': user_keywords
    }