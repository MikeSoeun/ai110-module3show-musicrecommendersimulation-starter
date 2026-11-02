from src.recommender import load_songs, recommend_songs

PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9},
    "Edge Case - Sad but High Energy": {"genre": "blues", "mood": "sad", "energy": 0.9},
    "Edge Case - Unknown Genre": {"genre": "k-pop", "mood": "happy", "energy": 0.7},
}


def print_recommendations(name: str, user_prefs: dict, songs: list) -> None:
    """Prints the top 5 recommendations for one profile in a readable layout."""
    print("=" * 60)
    print(f"Profile: {name}")
    print(f"Preferences: {user_prefs}")
    print("=" * 60)

    recommendations = recommend_songs(user_prefs, songs, k=5)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} by {song['artist']} ({song['genre']}, {song['mood']})")
        print(f"   Score: {score:.2f}")
        print(f"   Because: {explanation}")
    print()


def main() -> None:
    """Loads the catalog and prints recommendations for each test profile."""
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    for name, user_prefs in PROFILES.items():
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
