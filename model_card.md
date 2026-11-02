# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Intended Use  

VibeMatch suggests 5 songs from a small catalog that best fit a user's taste. It assumes the user can describe their taste with one favorite genre, one favorite mood, a target energy level from 0.0 (very calm) to 1.0 (very intense), and whether they like acoustic music.

It is built for classroom exploration, to show how recommenders turn data into suggestions.

**Not intended for:** real users or a real music app. It does not learn from listening history, it only knows 18 made-up songs, and its weights were picked by hand, not tested on real people.

---

## 3. How the Model Works  

Every song gets points for how well it matches the user:

- **Same genre** as the user's favorite: +2 points. This is the biggest factor.
- **Same mood** as the user's favorite: +1 point.
- **Energy closeness:** up to +1 point. A song with exactly the energy the user wants gets the full point. The further away it is, the fewer points it gets. This rewards songs that are *close* to the target, not just louder or quieter ones.
- **Acoustic bonus:** +0.5 if the user likes acoustic music and the song is mostly acoustic.

After every song has a score, the songs are sorted from highest to lowest and the top 5 are shown. Each result also lists the reasons it earned points, like "genre match (+2.0)".

Changes from the starter: I wrote the CSV loader, the scoring rule, the ranking, and the explanations, and added the acoustic bonus so the `likes_acoustic` setting actually does something.

---

## 4. Data  

- **18 songs** in `data/songs.csv`. The starter had 10, and I added 8.
- **Features:** genre, mood, energy, tempo, valence (how positive it sounds), danceability, and acousticness. Only genre, mood, energy, and acousticness are used for scoring.
- **Genres:** pop, indie pop, lofi, rock, ambient, jazz, synthwave, hip hop, classical, metal, r&b, edm, blues, country, reggaeton.
- **Moods:** happy, chill, intense, relaxed, moody, focused, confident, peaceful, angry, romantic, euphoric, sad, nostalgic, playful.
- **What I added:** hip hop, classical, metal, r&b, edm, blues, country, and reggaeton, plus moods like sad, angry, and romantic that were missing.
- **What is missing:** most genres have only one song, and lofi has the most with three. There is no k-pop, Latin pop, gospel, or world music. The songs are made up, so they say nothing about lyrics, language, or popularity.

---

## 5. Strengths  

- Users with a clear, common taste get great results. The Chill Lofi profile got all three lofi songs on top, followed by other calm, acoustic songs like ambient and jazz.
- The energy rule works well as a tie-breaker. When nothing matches genre or mood, the system still picks songs with the right "intensity."
- Every recommendation explains itself, so it is easy to see *why* a song showed up.
- Deep Intense Rock put *Storm Runner* first and then other loud songs (metal, edm), which matches my intuition.

---

## 6. Limitations and Bias 

The biggest weakness I found is that **genre is too powerful and is an exact text match**. In the "sad but high energy" test, *Empty Porch Blues* came first only because it is the single blues song, even though its energy (0.30) is far from what the user wanted (0.9). Meanwhile "indie pop" gets zero genre credit for a "pop" fan, and a "k-pop" fan gets no genre points at all, so their whole list is decided by mood and energy alone. Because each genre has only 1 to 3 songs, users with rare tastes quickly run out of real matches and get filled in with loud or quiet songs from unrelated genres. This creates a small "filter bubble": the system keeps rewarding the label on a song more than how the song actually feels.

---

## 7. Evaluation  

**Profiles tested:** High-Energy Pop, Chill Lofi, Deep Intense Rock, and two edge cases: "Sad but High Energy" (blues, sad, energy 0.9) and "Unknown Genre" (k-pop, happy, energy 0.7). I looked at whether the top 5 matched what I would expect, and ran one experiment where I halved the genre weight and doubled the energy weight.

**What surprised me:** *Gym Hero* showed up #2 for both the Pop and the Rock profiles. For a non-programmer: *Gym Hero* is labeled "pop," so a pop fan's list gives it 2 big points just for the label, even though it is an intense workout song, not a happy one. For the rock fan it is "intense" with very high energy, so it wins on mood and energy instead. One song that sits in the middle of two tastes can sneak onto both lists.

**Comparing profiles**

- **High-Energy Pop vs Chill Lofi:** Pop picks bright, upbeat songs around 0.8 energy. Lofi shifts to quiet, acoustic songs around 0.35. This makes sense because the energy targets are at opposite ends and the acoustic bonus only helps the lofi user.
- **High-Energy Pop vs Deep Intense Rock:** Both lean loud, so *Gym Hero* and *Sunrise City* appear on both. Pop ranks the happy song first while Rock ranks the intense one first, which shows the mood rule is doing its job.
- **High-Energy Pop vs Sad but High Energy:** Same high energy target, but the blues profile has almost no matching songs, so after the one blues song its list is just "the loudest songs in the catalog." That shows energy fills the gap when genre and mood run out.
- **High-Energy Pop vs Unknown Genre:** Both want happy songs, so *Rooftop Lights* and *Sunrise City* top both lists. Without any genre points, k-pop ranks indie pop above pop because its energy is a closer fit.
- **Chill Lofi vs Deep Intense Rock:** Complete opposites with no songs in common. Lofi gets calm, acoustic tracks and Rock gets loud, electric ones. This is the clearest proof the system can tell "intense rock" from "chill lofi."
- **Chill Lofi vs Sad but High Energy:** No overlap. The blues song is acoustic and calm and would fit the lofi user's vibe, but it does not show up for them because it does not match the lofi genre or the chill mood.
- **Chill Lofi vs Unknown Genre:** No overlap. Lofi gets strong 4+ point matches while k-pop's best score is under 2, which shows how much a missing genre hurts.
- **Deep Intense Rock vs Sad but High Energy:** Their lists overlap a lot (*Storm Runner*, *Gym Hero*, *Laser Heart*, *Iron Tempest*) because both want 0.9 energy. The only difference is the one blues song on top. Energy is doing most of the work for the edge case.
- **Deep Intense Rock vs Unknown Genre:** Rock has one perfect match and then loud songs. K-pop gets mid-energy songs like synthwave and hip hop because its target is 0.7, not 0.9.
- **Sad but High Energy vs Unknown Genre:** Both are "tricky" users. One has conflicting wishes and the other has a missing genre. In both cases the scores after #1 are all under 2 points, a sign the system is guessing.

**Experiment: halve genre weight, double energy weight.** For the pop user, *Rooftop Lights* (indie pop, happy) passed *Gym Hero* (pop, intense). That felt **more accurate**. For the rock user nothing moved. For the sad/high-energy user, the blues song stayed on top but its lead shrank from 2.41 to 0.82 points. Overall the change made some results better and others just different.

**Full output (original weights)**

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

============================================================
Profile: Chill Lofi
Preferences: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35, 'likes_acoustic': True}
============================================================
1. Library Rain by Paper Lanterns (lofi, chill)
   Score: 4.50
   Because: genre match (+2.0), mood match (+1.0), energy similarity (+1.00), acoustic sound (+0.5)
2. Midnight Coding by LoRoom (lofi, chill)
   Score: 4.43
   Because: genre match (+2.0), mood match (+1.0), energy similarity (+0.93), acoustic sound (+0.5)
3. Focus Flow by LoRoom (lofi, focused)
   Score: 3.45
   Because: genre match (+2.0), energy similarity (+0.95), acoustic sound (+0.5)
4. Spacewalk Thoughts by Orbit Bloom (ambient, chill)
   Score: 2.43
   Because: mood match (+1.0), energy similarity (+0.93), acoustic sound (+0.5)
5. Coffee Shop Stories by Slow Stereo (jazz, relaxed)
   Score: 1.48
   Because: energy similarity (+0.98), acoustic sound (+0.5)

============================================================
Profile: Deep Intense Rock
Preferences: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9}
============================================================
1. Storm Runner by Voltline (rock, intense)
   Score: 3.99
   Because: genre match (+2.0), mood match (+1.0), energy similarity (+0.99)
2. Gym Hero by Max Pulse (pop, intense)
   Score: 1.97
   Because: mood match (+1.0), energy similarity (+0.97)
3. Laser Heart by Pulse Theory (edm, euphoric)
   Score: 0.95
   Because: energy similarity (+0.95)
4. Iron Tempest by Grave Anvil (metal, angry)
   Score: 0.93
   Because: energy similarity (+0.93)
5. Sunrise City by Neon Echo (pop, happy)
   Score: 0.92
   Because: energy similarity (+0.92)

============================================================
Profile: Edge Case - Sad but High Energy
Preferences: {'genre': 'blues', 'mood': 'sad', 'energy': 0.9}
============================================================
1. Empty Porch Blues by Delta June (blues, sad)
   Score: 3.40
   Because: genre match (+2.0), mood match (+1.0), energy similarity (+0.40)
2. Storm Runner by Voltline (rock, intense)
   Score: 0.99
   Because: energy similarity (+0.99)
3. Gym Hero by Max Pulse (pop, intense)
   Score: 0.97
   Because: energy similarity (+0.97)
4. Laser Heart by Pulse Theory (edm, euphoric)
   Score: 0.95
   Because: energy similarity (+0.95)
5. Iron Tempest by Grave Anvil (metal, angry)
   Score: 0.93
   Because: energy similarity (+0.93)

============================================================
Profile: Edge Case - Unknown Genre
Preferences: {'genre': 'k-pop', 'mood': 'happy', 'energy': 0.7}
============================================================
1. Rooftop Lights by Indigo Parade (indie pop, happy)
   Score: 1.94
   Because: mood match (+1.0), energy similarity (+0.94)
2. Sunrise City by Neon Echo (pop, happy)
   Score: 1.88
   Because: mood match (+1.0), energy similarity (+0.88)
3. Night Drive Loop by Neon Echo (synthwave, moody)
   Score: 0.95
   Because: energy similarity (+0.95)
4. Concrete Crown by Block Theory (hip hop, confident)
   Score: 0.92
   Because: energy similarity (+0.92)
5. Fuego Lento by Sol Rivera (reggaeton, playful)
   Score: 0.90
   Because: energy similarity (+0.90)
```

---

## 8. Future Work  

- **Partial genre matching:** give some credit for related genres, for example "indie pop" or "k-pop" for a pop fan.
- **Use more features:** add valence, tempo, and danceability to the score, so "sad" and "happy" can be judged by sound, not just by the label.
- **More diversity in the top 5:** avoid showing several songs from the same artist or genre, and add more songs per genre so rare tastes have real options.

---

## 9. Personal Reflection  

My biggest learning moment was seeing that a recommender is just a scoring rule plus a sort. Once every song had a number, "recommending" was just picking the biggest numbers.

AI tools helped me write the loader, scoring, and ranking functions quickly and suggest edge-case profiles. I still had to double-check them. For example, the starter `main.py` imported `recommender` directly, which crashes when you run `python -m src.main`, so the import had to be changed to `src.recommender`. I also checked the math on the energy rule by hand to make sure a perfect match really gets 1.0 points.

It surprised me how "real" the results felt with only four simple rules. The Chill Lofi list honestly looks like a playlist I would get from an app.

If I kept going, I would add partial genre matches, use valence and tempo in the score, and try mixing in a simple collaborative-filtering step using fake listening histories from several users.
