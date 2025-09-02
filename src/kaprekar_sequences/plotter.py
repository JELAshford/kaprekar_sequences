import matplotlib.pylab as plt
from functools import cache
import numpy as np


@cache
def next_number(number: int) -> int:
    sorted_numbers = sorted(str(number).zfill(NUM_DIGITS))
    min_num = int("".join(sorted_numbers))
    max_num = int("".join(sorted_numbers[::-1]))
    return max_num - min_num


NUM_DIGITS = 7
MAX_LINES = 10_000


start_numbers = range(10**NUM_DIGITS)
if MAX_LINES < len(start_numbers):
    start_numbers = np.random.randint(0, 10**NUM_DIGITS, MAX_LINES)

all_histories = []
longest_history = 0
for start_number in start_numbers:
    number = start_number
    history = [start_number]
    while history[-1] not in history[:-1]:
        # Generate new number
        number = next_number(number)
        history.append(number)

    # Update longest history
    all_histories.append(history)
    longest_history = max(longest_history, len(history) - 1)

# Plot all histories padded
fig, ax = plt.subplots(1, 1, figsize=(12, 6))
for history in all_histories:
    history = [None] * (longest_history - len(history) + 1) + history
    # ax.plot(history, c="lightblue", alpha=min(100 / len(start_numbers), 1))
    ax.plot(history, c="lightblue", linewidth=10 ** -min(NUM_DIGITS - 2, 2))
ax.set_xlim(0, longest_history)
ax.set_xticks(range(longest_history + 1), labels=list(range(longest_history + 1))[::-1])
ax.set_ylabel("Value")
ax.set_xlabel("Steps until converged")
fig.suptitle(
    f"Ordered Subtraction Process on {len(start_numbers)} starting numbers of length {NUM_DIGITS}"
)
plt.show()
