import math
import re

# Data
data = input("Score: ")
parts = re.findall(r'\d+\s*-\s*\d+', data)              
score = [tuple(map(int, re.split(r'\s*-\s*', p))) for p in parts]

# Save each team's goals scored
a_num = []
b_num = []

for i in score:
    a_num.append(i[0])
    b_num.append(i[1])

# Average Goal Rates
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

# --- DIXON-COLES PARAMETER ---
# Rho represents the dependence between teams. 
# -0.13 is a common starting value for professional leagues.
rho = -0.13 

best_score = (0, 0)
max_prob = 0.0

# Loop through all possible scores (0-0 to 10-10)
for goals_a in range(11):
    prob_a = poisson(goals_a, a_rate)

    for goals_b in range(11):
        prob_b = poisson(goals_b, b_rate)

        # 1. Calculate Base Probability (Standard Poisson)
        base_prob = prob_a * prob_b

        # 2. Apply Dixon-Coles Adjustment
        correction_factor = 1.0 # Default: No change

        if goals_a == 0 and goals_b == 0:
            correction_factor = 1 - (a_rate * b_rate * rho)

        elif goals_a == 1 and goals_b == 0:
            correction_factor = 1 + (b_rate * rho)

        elif goals_a == 0 and goals_b == 1:
            correction_factor = 1 + (a_rate * rho)

        elif goals_a == 1 and goals_b == 1:
            correction_factor = 1 - rho

        # 3. Calculate Final Probability
        final_prob = base_prob * correction_factor

        # Save if this is the highest probability so far
        if final_prob > max_prob:
            max_prob = final_prob
            best_score = (goals_a, goals_b)

# Print Result
print(f"Team A Rate: {a_rate}")
print(f"Team B Rate: {b_rate}")
print(f"The predicted result is {best_score[0]} - {best_score[1]}")
print(f"Probability (Dixon-Coles): {max_prob * 100:.2f}%")