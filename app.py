import random

import streamlit as st

from logic_utils import (
    check_guess,
    get_attempt_limit,
    get_range_for_difficulty,
    hint_for,
    parse_guess,
    points_if_won_now,
    update_score,
)


def start_new_game(low: int, high: int):
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    # Bumping this changes the guess box's key, which is how the old guess
    # gets cleared: Streamlit sees a widget it has not met before.
    st.session_state.game_id = st.session_state.get("game_id", 0) + 1


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit = get_attempt_limit(difficulty)
low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

show_debug = st.sidebar.checkbox("Developer debug info", value=False)

# Starting up, or the player changed difficulty: deal a fresh secret that is
# actually inside the new range.
if st.session_state.get("difficulty") != difficulty:
    st.session_state.difficulty = difficulty
    start_new_game(low, high)

st.subheader("Make a guess")

# Reserve these two spots now, but fill them at the bottom of the script.
# Streamlit draws top to bottom, and the guess below can change attempts and
# score -- so anything written here would show the state from before this
# rerun's guess was processed.
info_slot = st.empty()
debug_slot = st.container()


def render_status_panels():
    """Fill the reserved slots. Call once, after the guess has been handled."""
    if st.session_state.status == "playing":
        next_win_value = points_if_won_now(
            st.session_state.attempts + 1, attempt_limit, difficulty
        )
        info_slot.info(
            f"Guess a number between {low} and {high}. "
            f"Attempts left: {attempt_limit - st.session_state.attempts}. "
            f"Win on this guess for {next_win_value} points."
        )
    else:
        info_slot.info(
            f"Game over after {st.session_state.attempts} attempts. "
            f"Final score: {st.session_state.score}."
        )

    if show_debug:
        with debug_slot.expander("Developer Debug Info"):
            if st.session_state.status == "playing":
                st.write("Secret: hidden while the game is in progress")
            else:
                st.write("Secret:", st.session_state.secret)
            st.write("Attempts:", st.session_state.attempts)
            st.write("Score:", st.session_state.score)
            st.write("Difficulty:", difficulty)
            st.write("History:", st.session_state.history)


raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{st.session_state.game_id}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    start_new_game(low, high)
    st.rerun()

if st.session_state.status != "playing":
    # Finished game: show the outcome and take no more guesses. This is an
    # elif chain rather than an st.stop() so the reserved slots below always
    # get filled, whichever path the script takes.
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")

elif submit:
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        st.error(err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        outcome = check_guess(guess_int, st.session_state.secret)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
            attempt_limit=attempt_limit,
            difficulty=difficulty,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.error(
                f"Out of attempts! "
                f"The secret was {st.session_state.secret}. "
                f"Score: {st.session_state.score}"
            )
        elif show_hint:
            st.warning(hint_for(outcome))

# State has settled for this rerun -- now the reserved slots can be filled
# with numbers that match what actually just happened.
render_status_panels()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
