# Game Sampling

We sample generated 2x2 games.

## Core Functions


---

##### `build_labelled_payoffs(p1, p2)`

Labels Player 1 and Player 2's payoffs using the standard ["TL", "TR", "BL", "BR"] format.

```python
def build_labelled_payoffs(p1: tuple[int, int, int, int],
                           p2: tuple[int, int, int, int]) -> Tuple[dict, dict]:
    labels = ["TL", "TR", "BL", "BR"]
    return dict(zip(labels, p1)), dict(zip(labels, p2))
```
Returns
Two dictionaries mapping quadrant to payoffs for P1 and P2.

---

##### `build_matrix_fn(data)`
Constructs a 2x2 matrix from a labeled dictionary.
```python
def build_matrix_fn(data: dict) -> list[list]:
    return [[data["TL"], data["TR"]], [data["BL"], data["BR"]]]
```
Returns A 2D list structured as a payoff matrix.

---

### Full game wrapping 