An arbitrary two-player (2×2) normal-form game is given. Each cell shows a pair of payoffs [x, y]:
- x = payoff for Player 1 (row player, p1).
- y = payoff for Player 2 (column player, p2).

Players:
 p1 (row player) chooses between: Top (T) or Bottom (B).
 p2 (column player) chooses between: Left (L) or Right (R).

The game matrix (called `combined_matrix`) is:
[
  [[x1, y1], [x2, y2]],
  [[x3, y3], [x4, y4]]
]

Here:
- Row 1 (Top) has two cells: (T, L) with payoffs [x1, y1], and (T, R) with [x2, y2].
- Row 2 (Bottom) has two cells: (B, L) with [x3, y3], and (B, R) with [x4, y4].

---

### Task: Find the Pure-Strategy Nash Equilibrium

A pure-strategy NE is a pair (one action per player) where neither player gains by unilaterally switching actions. To check if a strategy (e.g. T/L) is a NE, verify that:
1. Given p2 plays L, p1 wouldn’t switch if T’s payoff > B’s payoff (for that column).
2. Given p2 plays R, p1 wouldn’t switch if T’s payoff > B’s payoff (for that column).
3. Given p1 plays T, p2 wouldn’t switch if L’s payoff > R’s payoff (for that row).
4. Given p1 plays B, p2 wouldn’t switch if L’s payoff > R’s payoff (for that row).

Alternatively, identify strictly dominating rows/columns:
- For p1: Compare Top row payoffs (x1,x2) vs. Bottom row (x3,x4). If one row is strictly higher in both columns, it dominates.
- For p2: Compare Left column payoffs (y1,y3) vs. Right column (y2,y4). If one column is strictly higher in both rows, it dominates.

The Nash equilibrium is the combination of the chosen best responses by p1 and p2.

Your job: Determine the pure‐strategy NE(s) in the provided `combined_matrix`: ${matrix}.

---

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