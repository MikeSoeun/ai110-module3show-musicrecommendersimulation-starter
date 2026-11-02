import csv
import os
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict

GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.0
ACOUSTIC_BONUS = 0.5


@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP wrapper around the scoring and ranking logic."""

    def __init__(self, songs: List[Song]):
        """Stores the catalog of Song objects."""
        self.songs = songs

    def _user_to_prefs(self, user: UserProfile) -> Dict:
        """Converts a UserProfile into the preferences dictionary used by score_song."""
        return {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k Song objects for the user, highest score first."""
        prefs = self._user_to_prefs(user)
        ranked = sorted(self.songs, key=lambda song: score_song(prefs, asdict(song))[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a readable explanation of why a song was scored the way it was."""
        prefs = self._user_to_prefs(user)
        score, reasons = score_song(prefs, asdict(song))
        return f"Score {score:.2f}: " + ", ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Reads the songs CSV into a list of dictionaries with numeric fields converted."""
    if not os.path.exists(csv_path):
        print(f"Error: file not found: {csv_path}")
        return []

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores one song against the user's preferences and returns (score, reasons)."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        score += GENRE_WEIGHT
        reasons.append(f"genre match (+{GENRE_WEIGHT:.1f})")

    if song["mood"] == user_prefs.get("mood"):
        score += MOOD_WEIGHT
        reasons.append(f"mood match (+{MOOD_WEIGHT:.1f})")

    if "energy" in user_prefs:
        energy_points = ENERGY_WEIGHT * (1 - abs(song["energy"] - user_prefs["energy"]))
        score += energy_points
        reasons.append(f"energy similarity (+{energy_points:.2f})")

    if user_prefs.get("likes_acoustic") and song["acousticness"] >= 0.6:
        score += ACOUSTIC_BONUS
        reasons.append(f"acoustic sound (+{ACOUSTIC_BONUS:.1f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song, sorts them from highest to lowest, and returns the top k."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, ", ".join(reasons)))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
