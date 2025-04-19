## 1. Title and Short Introduction

"2x2 Normal-Form Game: Payoff Analysis and Nash Equilibrium"
We have a 2x2 normal-form game where two players each choose one of two strategies. Our goal is to identify any pure-strategy Nash Equilibrium (NE) for the given payoff matrix.

---

## 2. Glossary

- Player 1 (p1): The row player. Chooses between Top (T) or Bottom (B).
- Player 2 (p2): The column player. Chooses between Left (L) or Right (R).
- Payoffs [x, y]:
   - x = payoff for p1  
   - y = payoff for p2  
- 2x2 Normal-Form Game: A matrix with 2 rows (T, B) and 2 columns (L, R). Each cell is [x, y].
- Strict Dominance: A player's strategy strictly dominates another if it yields strictly higher payoff for every possible choice by the other player.
- Best Response: Given the opponent's fixed strategy, a best response is the strategy that gives the highest payoff to the player in question.
- Pure-Strategy Nash Equilibrium (NE): A pair of strategies (one for p1 and one for p2) such that neither player can increase their payoff by unilaterally changing their own strategy.
- Strategy Notation: p1 uses T or B. p2 uses L or R.

---

## 3. Game Matrix Specification

We have a 2x2 matrix labeled `combined_matrix`, containing the payoff pairs as follows:
[ [[x1, y1], [x2, y2]], [[x3, y3], [x4, y4]] ]

- Top-Left cell = (T, L) = [x1, y1]
- Top-Right cell = (T, R) = [x2, y2]
- Bottom-Left cell = (B, L) = [x3, y3]
- Bottom-Right cell = (B, R) = [x4, y4]

Here, x-values correspond to p1, y-values correspond to p2.
Determine the pure‐strategy NE(s) in the provided `combined_matrix`: ${matrix}.
---

## 4. Detailed Steps to Identify the Pure-Strategy NE

1. Extract Payoffs for Each Player
   - For p1, payoffs x1, x2 in the top row and x3, x4 in the bottom row.
   - For p2, payoffs y1, y3 in the left column and y2, y4 in the right column.

2. Check for Strict Dominance
   - p1: Compare Top row (x1, x2) to Bottom row (x3, x4). If x1 > x3 and x2 > x4, T strictly dominates B. If x1 < x3 and x2 < x4, B strictly dominates T.
   - p2: Compare Left column (y1, y3) to Right column (y2, y4). If y1 > y2 and y3 > y4, L strictly dominates R. If y1 < y2 and y3 < y4, R strictly dominates L.

3. Check Each Potential NE
   - If no strict dominance emerges, evaluate each strategy pair (T,L), (T,R), (B,L), (B,R).
   - For each pair, confirm that p1 and p2 would not want to deviate, given the other's choice.

4. Determine the Final Pure-Strategy NE
   - If none is found, the result is no pure-strategy NE.
   - If one or more NE pairs are found, those are your final answers.

---

## 5. Output Format

Return your final answer as a list of strings, where each string is a two-character code "XY", with X in {T, B} (p1's choice) and Y in {L, R} (p2's choice). For example:

- If the NE is p1 plays Top and p2 plays Left, return ["TL"].
- If there is no pure-strategy NE, return an empty list [].

Do not include explanations in your final output. Only return the result.

Example JSON output:
```json
{
  "NE": ["TL"]
}
