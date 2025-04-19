An arbitrary two-player (2×2) normal-form game is given. Each cell shows a pair of payoffs [x, y]:
- x = payoff for Player 1 (row player, p1).
- y = payoff for Player 2 (column player, p2).

Players:
• p1 (row player) chooses between: Top (T) or Bottom (B).
• p2 (column player) chooses between: Left (L) or Right (R).

The game matrix (called `combined_matrix`) is:
[
  [[x1, y1], [x2, y2]],
  [[x3, y3], [x4, y4]]
]

Here:
- Row 1 (Top) → (T,L) = [x1, y1], (T,R) = [x2, y2]
- Row 2 (Bottom) → (B,L) = [x3, y3], (B,R) = [x4, y4]

---

### Detailed Steps for Payoff Comparison

Step 1: Extract Each Player’s Own Payoffs

1. Player 1’s matrix (the “x”-payoffs):
   - For Row T: payoffs are x1 and x2
   - For Row B: payoffs are x3 and x4
   - Example: If `combined_matrix[0]` = [[x1,y1],[x2,y2]] and `combined_matrix[1]` = [[x3,y3],[x4,y4]],
     then Player 1’s payoff matrix is:
     ```
     [ [x1, x2],
       [x3, x4] ]
     ```
2. Player 2’s matrix (the “y”-payoffs):
   - For Column L: payoffs are y1 and y3
   - For Column R: payoffs are y2 and y4
   - Example: Using the same combined_matrix, Player 2’s payoff matrix is:
     ```
     [ [y1, y2],
       [y3, y4] ]
     ```

---

Step 2: Compare Payoffs to Identify Domination

1. Player 1’s perspective (row domination):
   - Compare Row T vs. Row B element by element:
     - (T,L) payoff vs. (B,L) payoff → compare x1 vs. x3
     - (T,R) payoff vs. (B,R) payoff → compare x2 vs. x4
   - If x1 > x3 and x2 > x4, Row T strictly dominates Row B.
   - If x1 < x3 and x2 < x4, Row B strictly dominates Row T.
   - Otherwise, neither row is strictly dominant.

2. Player 2’s perspective (column domination):
   - Compare Column L vs. Column R element by element:
     - (T,L) payoff vs. (T,R) payoff → compare y1 vs. y2
     - (B,L) payoff vs. (B,R) payoff → compare y3 vs. y4
   - If y1 > y2 and y3 > y4, Column L strictly dominates Column R.
   - If y1 < y2 and y3 < y4, Column R strictly dominates Column L.
   - Otherwise, neither column is strictly dominant.

---

### Task: Determine the Pure-Strategy Nash Equilibrium

A pure-strategy NE is a pair of actions (one for Player 1, one for Player 2) where neither player has an incentive to deviate, given the other’s choice. Using the above steps:

- First, check if either player has a strictly dominated strategy.
- If so, you can reduce the matrix and see which (T/B, L/R) combination remains.
- If neither has a strictly dominated strategy, examine each possible action pair (T,L), (T,R), (B,L), (B,R) to see if it satisfies the definition of a Nash equilibrium.

Complete this by analyzing the provided `combined_matrix`: ${matrix}.

## Output format

Return your answer as a list of strings in the format:
`["XY"]`, where:
- X ∈ {"T", "B"} (Player 1’s choice: Top or Bottom)
- Y ∈ {"L", "R"} (Player 2’s choice: Left or Right)

Examples:
- If the equilibrium is Player 1 plays Top and Player 2 plays Left → `["TL"]`
- If there is no pure-strategy NE → `[]`

Do not explain your answer. Only return the final result.

---

Example:
```json
{
  "NE": ["insert answer here."]
}