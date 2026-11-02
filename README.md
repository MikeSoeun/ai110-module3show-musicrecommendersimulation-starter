# 🎵 Music Recommender Simulation

## Project Summary

This project is a small, content-based music recommender written in Python. It reads a catalog of 18 songs from a CSV file, compares each song to a user's "taste profile" (favorite genre, favorite mood, target energy, and whether they like acoustic music), gives every song a score, and prints the top 5 matches with a plain-English reason for each score. It is a classroom simulation meant to show how apps like Spotify turn data into recommendations, and where that process can go wrong.

---

## How The System Works

**How real recommenders work.** Big platforms like Spotify and YouTube mix two main ideas. **Collaborative filtering** looks at other users' behavior: if people who like the same songs as you also love a new song, you will probably be shown that song too. It uses data like likes, skips, saves, replays, playlist adds, and listening time. **Content-based filtering** looks at the songs themselves: genre, mood, tempo, energy, danceability, and acousticness. If you play a lot of calm acoustic music, it finds other calm acoustic songs. Real systems combine both, at massive scale, and learn their weights from millions of users instead of having a person set them by hand.

**What my version prioritizes.** My simulation is purely content-based, since there are no other users in the data. It cares most about **genre**, then **mood**, then how close the song's **energy** is to what the user wants. Acoustic sound is a small bonus for users who like it.

**Features used**

- `Song`: `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness` (genre, mood, energy, and acousticness are used in scoring)
- `UserProfile`: `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`

**Algorithm Recipe (Scoring Rule, one song at a time)**

| Rule | Points |
|---|---|
| Genre matches the user's favorite genre | +2.0 |
| Mood matches the user's favorite mood | +1.0 |
| Energy similarity: `1 - abs(song_energy - target_energy)` | 0.0 to +1.0 |
| User likes acoustic and song acousticness ≥ 0.6 | +0.5 |

The energy rule rewards songs that are **close** to the target instead of songs that are simply higher or lower. A song with exactly the target energy earns the full 1.0 point, and the score drops the farther away it gets.

**Ranking Rule (the whole list)**

The scoring rule only judges one song. The ranking rule runs the scoring rule on every song in the catalog, sorts all of them from highest to lowest score, and keeps the top `k` (5 by default). You need both: without scores there is nothing to sort, and without sorting you just have a pile of numbers.

**Data flow**

```
User Prefs (genre, mood, energy, likes_acoustic)
        |
        v
For each song in data/songs.csv  -->  score_song()  -->  (score, reasons)
        |
        v
Sort all songs by score (highest first)  -->  Top K recommendations
```

**Expected biases.** Because a genre match is worth twice as much as a mood match, the system may over-prioritize genre and bury great songs from other genres that match the user's mood and energy. Also, every genre in the small catalog only has one to three songs, so users whose genre is rare or missing will get weaker results.

**Dataset changes.** I expanded `data/songs.csv` from 10 to 18 songs by adding genres and moods that were missing: hip hop (confident), classical (peaceful), metal (angry), r&b (romantic), edm (euphoric), blues (sad), country (nostalgic), and reggaeton (playful).

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Default "pop / happy" profile:

```
Loaded songs: 18

============================================================
Profile: High-Energy Pop
Preferences: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}
============================================================
1. Sunrise City by Neon Echo (pop, happy)
   Score: 3.98
   Because: genre match (+2.0), mood match (+1.0), energy similarity (+0.98)
2. Gym Hero by Max Pulse (pop, intense)
   Score: 2.87
   Because: genre match (+2.0), energy similarity (+0.87)
3. Rooftop Lights by Indigo Parade (indie pop, happy)
   Score: 1.96
   Because: mood match (+1.0), energy similarity (+0.96)
4. Fuego Lento by Sol Rivera (reggaeton, playful)
   Score: 1.00
   Because: energy similarity (+1.00)
5. Concrete Crown by Block Theory (hip hop, confident)
   Score: 0.98
   Because: energy similarity (+0.98)
```

---

## Experiments You Tried

**Multiple profiles.** I ran five profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and two edge cases (a "sad but high energy" blues fan and a fan of k-pop, a genre that is not in the catalog). Full output for every profile is in [`model_card.md`](model_card.md).

**Weight shift (genre halved, energy doubled).** I changed the genre weight from 2.0 to 1.0 and the energy weight from 1.0 to 2.0.

- High-Energy Pop: *Rooftop Lights* (indie pop, happy) moved up from #3 to #2 and passed *Gym Hero* (pop, intense). This felt **more accurate**, because a happy song with the right energy is closer to "happy pop" than an intense workout song.
- Deep Intense Rock: the top 5 stayed the same. The change only made the gaps between scores smaller.
- Sad but High Energy: *Empty Porch Blues* stayed #1, but its lead shrank from 2.41 points to 0.82 points. With a bit more weight on energy, loud songs would overtake the only sad song.

So the change made some results more accurate and others just different.

```
============================================================
Profile: High-Energy Pop
Preferences: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}
============================================================
1. Sunrise City by Neon Echo (pop, happy)
   Score: 3.96
   Because: genre match (+1.0), mood match (+1.0), energy similarity (+1.96)
2. Rooftop Lights by Indigo Parade (indie pop, happy)
   Score: 2.92
   Because: mood match (+1.0), energy similarity (+1.92)
3. Gym Hero by Max Pulse (pop, intense)
   Score: 2.74
   Because: genre match (+1.0), energy similarity (+1.74)
4. Fuego Lento by Sol Rivera (reggaeton, playful)
   Score: 2.00
   Because: energy similarity (+2.00)
5. Concrete Crown by Block Theory (hip hop, confident)
   Score: 1.96
   Because: energy similarity (+1.96)

============================================================
Profile: Deep Intense Rock
Preferences: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9}
============================================================
1. Storm Runner by Voltline (rock, intense)
   Score: 3.98
   Because: genre match (+1.0), mood match (+1.0), energy similarity (+1.98)
2. Gym Hero by Max Pulse (pop, intense)
   Score: 2.94
   Because: mood match (+1.0), energy similarity (+1.94)
3. Laser Heart by Pulse Theory (edm, euphoric)
   Score: 1.90
   Because: energy similarity (+1.90)
4. Iron Tempest by Grave Anvil (metal, angry)
   Score: 1.86
   Because: energy similarity (+1.86)
5. Sunrise City by Neon Echo (pop, happy)
   Score: 1.84
   Because: energy similarity (+1.84)

============================================================
Profile: Edge Case - Sad but High Energy
Preferences: {'genre': 'blues', 'mood': 'sad', 'energy': 0.9}
============================================================
1. Empty Porch Blues by Delta June (blues, sad)
   Score: 2.80
   Because: genre match (+1.0), mood match (+1.0), energy similarity (+0.80)
2. Storm Runner by Voltline (rock, intense)
   Score: 1.98
   Because: energy similarity (+1.98)
3. Gym Hero by Max Pulse (pop, intense)
   Score: 1.94
   Because: energy similarity (+1.94)
4. Laser Heart by Pulse Theory (edm, euphoric)
   Score: 1.90
   Because: energy similarity (+1.90)
5. Iron Tempest by Grave Anvil (metal, angry)
   Score: 1.86
   Because: energy similarity (+1.86)
```

---

## Limitations and Risks

- It only works on a tiny catalog of 18 songs, with 1 to 3 songs per genre.
- Genre is an exact text match, so "indie pop" gets no credit for a "pop" fan and "k-pop" gets no credit at all.
- It does not understand lyrics, language, or listening history.
- It might over-favor genre, and a single matching song can win even when its energy is far from what the user wants.

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

I learned that a recommender is really two simple pieces: a rule that gives one song a score, and a sort that puts the best scores on top. Even with only four rules, the results "felt" like real recommendations, which shows how much of the magic in real apps is just well-chosen features and weights. Turning a vibe into numbers like energy and acousticness was the step that made everything else possible.

I also saw how easily bias slips in. The weights I picked by hand decide whose taste counts most. A user who likes a genre that is missing from the data, or who has an unusual mix of preferences like sad but high energy, gets worse results without the system ever noticing. Real platforms have the same problem at a much bigger scale, where small choices about data and weights can push everyone toward the same popular songs.
