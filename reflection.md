# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- The game looked good. It seemed like it worked, but then it didn't. The interface was easy to navigate thru.
- The new game button didn't work when I didn't guess properly. And some of the hints didn't work. Also I noticed that some of the hints would be inconsistent.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Win a game, then click "New Game 🔁" | Fresh secret number, attempts back to full, board playable again | Screen stays on "You already won. Start a new game to play again." Typing a guess does nothing. Same thing happens after losing. | No error. The reset only cleared `secret` and `attempts`, so `status` stayed `"won"` in session state and `st.stop()` ran again on the next rerun. |
| Secret is 42, guess 70 | "Go LOWER" | "📈 Go HIGHER!" | No error. Both hint messages were attached to the wrong branch. |
| Secret is 100, guess 9 on an even-numbered attempt | "Go HIGHER" | "📉 Go LOWER!" | No error. On even attempts the secret was turned into text, so the comparison was `"9" > "100"`, which is true the way "zebra" comes after "apple". The `TypeError` was caught inside the function, so nothing printed. |
| Start on Normal (secret 87), switch difficulty to Easy (range 1-20) | New game with a secret inside 1-20 | Secret stays 87, which is outside the range, so the game cannot be won | No error. The secret was only generated once and never regenerated on a difficulty change. |
| Load the game on Normal, before guessing | "Attempts left: 8" | "Attempts left: 7" | No error. `attempts` was initialized to 1 instead of 0. |
| Type `abc`, click Submit Guess | Error message, attempt not counted | "That is not a number." and "Attempts left" drops by one anyway | No error. `attempts` was incremented before the input was validated. |
| Hard mode: 7 wrong guesses, then the correct one | A win should give a positive score | Final score: -15 | No error. Each miss cost 15 points (-5 directly, -10 off the decaying win bonus), and the formula ignored difficulty, so a well-played Hard game finished negative. |
| Any "Too High" guess on an even-numbered attempt | Score goes down 5 | Score goes **up** 5 | No error. The scoring function had an `attempt_number % 2` branch that added points instead of subtracting. |

Note: none of these bugs raised an exception or printed anything to the console. They were all silent logic errors, which is why the game looked like it worked at first.

---

## 2. How did you use AI as a teammate?

- So I used Claude code to help me find what didn't work. I had it explain to me why it didn't work and suggest other ways I could have the code work. The suggestions it gave was actually really helpful and I also had it explain the pros for each suggestion. Also, I rejected the idea that we have negative scores because that's what it suggested.

---

## 3. Debugging and testing your fixes

- I actually tested the game manually to see if any of the bugs that I was looking for specifically was fixed. I also had claude check for other glitches that could be fixed. One specific example as the point system. I noticed that it was doing negative scores and I didn't want that so I fixed it up.

---

## 4. What did you learn about Streamlit and state?

- I learned that any time you click anything in Streamlit, it re-runs your script from the top meaning normal variables get wiped. This would give you a brand-new secret number on every click, making the game unwinnable. The only thing that survives is the st.session_state.

---

## 5. Looking ahead: your developer habits

- One habit I would take away from this is to always double-check the code myself rather than having AI fix it and keep it pushing. I think that although AI can be helpful, it can make us complacent and lazy, but I do enjoy how easier it can make my work.
