# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- The game looked good. It seemed like it worked, but then it didn't. The interface was easy to navigate thru.
- The new game button didn't work when I didn't guess properly. Hard mode only had a range of 1 - 50 thus making it easier than 'Normal'. Also I noticed that some of the hints would be inconsistent.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|Bug 1:
 Win or lose game, the New Game button didn't refresh the page making replayability nonexistent 
|
| Bug 2:
Hints were inconsistent; sometimes it would just say Go higher or go lower 
The secret was 47 and I guessed 40, but it told me to go lower instead of go higher.
Bug 3:
Hard mode range wasn't harder than normal. Normal range was from 1 - 100 and Hard was 1 - 50. 
I expected hard mode to have a higher range of numbers than Normal so we fixed it from 1 - 50 to 1 - 200.

Bug 4: 
Beforehand, switching difficulties would not give you your attempts back making the game harder, I expected to get a fresh 8 attempts, but after going thru what was "broken", we fixed that problem so now every time you switch difficulties, you get a new set of attempts.
---

## 2. How did you use AI as a teammate?

- So I used Claude code to help me find what didn't work. I had it explain to me why it didn't work and suggest other ways I could have the code work. The suggestions it gave was actually really helpful and I also had it explain the pros for each suggestion. Before the fix, switching between the difficulties would NOT reset the game, but after the fix and the suggestion of claude, it fixed that problem so now everytime you switch difficulties, the game is essentially reset. I went back to the website and ran the game again to make sure it met the expected behavior. 

Claude suggested that we deduct points for every wrong guess, however, I was not a fan of the idea so I rejected the suggestion and kept the + point.

---

## 3. Debugging and testing your fixes

- I actually tested the game manually to see if any of the bugs that I was looking for specifically was fixed. I also had claude check for other glitches that could be fixed. One specific example as the point system. I noticed that it was doing negative scores and I didn't want that so I fixed it up.
- I added my own test for the negative score bug and it passed, but then I learned that a test passing doesn't always prove much. My test only called the scoring function one time for the win, and the negative score actually came from adding up all the wrong guesses before it, so my test would have passed even on the broken code. It also made me realize the 3 tests that came with the project only check the check_guess function, so they never would have caught the New Game bug I found in the first place. The lesson for me was that a test has to repeat the same steps I did when I actually ran into the bug, otherwise it is just passing for no reason.

---

## 4. What did you learn about Streamlit and state?

- I learned that any time you click anything in Streamlit, it re-runs your script from the top meaning normal variables get wiped. This would give you a brand-new secret number on every click, making the game unwinnable. The only thing that survives is the st.session_state.

---

## 5. Looking ahead: your developer habits

- One habit I would take away from this is to always double-check the code myself rather than having AI fix it and keep it pushing. I think that although AI can be helpful, it can make us complacent and lazy, but I do enjoy how easier it can make my work.
