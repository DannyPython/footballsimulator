import math
import re

# Data
data = input("Score: ")
parts = re.findall(r'\d+\s*-\s*\d+', data)              
score = [tuple(map(int, re.split(r'\s*-\s*', p))) for p in parts]


# Save each team's goals scored
a_num = []
b_num = []

# Separate goals
for i in score:
    a_num.append(i[0])
    b_num.append(i[1])

# Average Goal Rates
# (Added a check to avoid division by zero if list is empty)
if len(a_num) > 0:
    a_rate = sum(a_num) / len(a_num)
    b_rate = sum(b_num) / len(b_num)
else:
    a_rate = 0
    b_rate = 0

def poisson(k, rate):
    nume = (rate**k) * math.exp(-rate)
    deno = math.factorial(k)
    p = nume / deno
    return p


best_score = (0, 0) # Store the best score (A, B)
max_prob = 0.0      # Store the highest probability found

# We use nested loops to check every combination of A vs B
# From 0-0 up to 10-10
for goals_a in range(11):
    prob_a = poisson(goals_a, a_rate)

    for goals_b in range(11):
        prob_b = poisson(goals_b, b_rate)

        # Calculate the probability of this SPECIFIC scoreline
        # P(A) * P(B)
        current_prob = prob_a * prob_b

        # If this score is more likely than the previous best, save it
        if current_prob > max_prob:
            max_prob = current_prob
            best_score = (goals_a, goals_b)

# Print Result
print(f"Team A Rate: {a_rate}")
print(f"Team B Rate: {b_rate}")
print(f"The predicted result is {best_score[0]} - {best_score[1]}")
print(f"Probability: {max_prob * 100:.2f}%")
