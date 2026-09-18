"""
Game rules for Glitchy Guesser.

Everything here is pure: no Streamlit, no session state, no randomness. That is
the point of splitting it out of app.py -- these functions can be tested by
calling them, without having to drive the web UI.
"""

# Number range per difficulty, and how many guesses you get.
DIFFICULTY_RANGES = {"Easy": (1, 20), "Normal": (1, 100), "Hard": (1, 200)}
ATTEMPT_LIMITS = {"Easy": 6, "Normal": 8, "Hard": 10}

# Points a win is worth at full value. A wider range needs more guesses, so it
# has to pay more, or choosing Hard would just punish the player.
DIFFICULTY_POINTS = {"Easy": 60, "Normal": 120, "Hard": 240}

# What to show the player for each outcome.
HINTS = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}

DEFAULT_DIFFICULTY = "Normal"


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    return DIFFICULTY_RANGES.get(difficulty, DIFFICULTY_RANGES[DEFAULT_DIFFICULTY])


def get_attempt_limit(difficulty: str):
    """Return how many guesses the player gets on this difficulty."""
    return ATTEMPT_LIMITS.get(difficulty, ATTEMPT_LIMITS[DEFAULT_DIFFICULTY])


def parse_guess(raw: str, low: int, high: int):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    raw = raw.strip()

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except ValueError:
        return False, None, "That is not a number."

    if value < low or value > high:
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome.

    Returns one of: "Win", "Too High", "Too Low". The wording shown to the
    player lives in hint_for(), so the rule and the phrasing stay separate.
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def hint_for(outcome: str):
    """The message to display for an outcome from check_guess()."""
    return HINTS.get(outcome, "")


def points_if_won_now(attempt_number: int, attempt_limit: int, difficulty: str):
    """
    What a win on `attempt_number` pays.

    Think of it as a pot that shrinks with every guess: you start with the
    difficulty's full value and bank whatever is left when you win. A win
    always pays at least 10, so a score can never go down.
    """
    budget_left = attempt_limit - attempt_number + 1
    full_value = DIFFICULTY_POINTS.get(
        difficulty, DIFFICULTY_POINTS[DEFAULT_DIFFICULTY]
    )
    earned = round(full_value * budget_left / attempt_limit)
    return max(10, earned)


def update_score(current_score: int, outcome: str, attempt_number: int,
                 attempt_limit: int, difficulty: str):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        return current_score + points_if_won_now(
            attempt_number, attempt_limit, difficulty
        )

    # Wrong guesses cost nothing directly. They still hurt, because each one
    # shrinks the pot above -- and that is what keeps a score from ever
    # going negative.
    return current_score
