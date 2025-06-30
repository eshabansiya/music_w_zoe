from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

app = Flask(__name__)
CORS(app)

df_orig = pd.read_csv('music-rec/public/spotify_tracks.csv')

audio_features = ['danceability', 'energy', 'valence', 'tempo', 'acousticness']

genre_clusters = {
    "Pop": ['pop', 'power-pop', 'pop-film', 'indie-pop', 'synth-pop'],
    "Hip-Hop": ['hip-hop', 'rap', 'trap'],
    "Rock": ['rock', 'punk', 'punk-rock', 'alt-rock', 'hard-rock', 'psych-rock', 'rock-n-roll', 'grunge', 'metal', 'heavy-metal', 'metalcore'],
    "Electronic": ['edm', 'electronic', 'electro', 'deep-house', 'house', 'techno', 'trance', 'minimal-techno', 'club', 'progressive-house', 'detroit-techno'],
    "Jazz": ['jazz', 'blues', 'soul', 'funk'],
    "Classical": ['classical', 'piano', 'opera'],
    "Latin": ['latin', 'reggaeton', 'salsa', 'brazil', 'mpb', 'pagode', 'forro', 'samba', 'latino'],
    "World": ['indian', 'iranian', 'turkish', 'malay', 'swedish', 'german', 'french', 'j-pop', 'k-pop', 'anime', 'mandopop', 'cantopop'],
    "Country": ['country', 'bluegrass', 'honky-tonk', 'folk'],
    "Other": ['ambient', 'new-age', 'sleep', 'study', 'comedy', 'disney', 'show-tunes', 'children', 'gospel', 'romance', 'happy', 'sad', 'party']
}

df_orig['broad_genre'] = df_orig['track_genre'].apply(
    lambda x: next((cluster for cluster, genres in genre_clusters.items() if x in genres), 'Other')
)

label_encoder = LabelEncoder()
df_orig['broad_genre_encoded'] = label_encoder.fit_transform(df_orig['broad_genre'])

@app.route("/api/classify", methods=["GET"])
def classify():
    X = df_orig[audio_features]
    y = df_orig['broad_genre_encoded']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train_scaled, y_train)
    y_pred = knn.predict(X_test_scaled)

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)

    return jsonify({
        "accuracy": accuracy,
        "report": report
    })

if __name__ == "__main__":
    app.run(debug=True)
