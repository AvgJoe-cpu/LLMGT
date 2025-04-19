# Game Building

We generate structured 2x2 games for evaluation and experimentation.

## Core Functions
---

##### `sample_payoffs()`

Samples a list of four random payoff values between 1 and 10.

```python
def sample_payoffs() -> list[int]:
    return [random.randint(1, 10) for _ in range(4)]
```

---

##### `sample_fn(condition)`
Samples payoff tuples until a given condition is satisfied.

```python
def sample_fn(condition: Callable[[int, int, int, int], bool]):
    while True:
        a = sample_payoffs()
        if condition(*a):
            return tuple(a)
```
---
 
##### `cond_p1_dominant_top(x1, x2, x3, x4)`
Returns `True` if Player 1 strictly prefers the top row.

```python
def cond_p1_dominant_top(x1, x2, x3, x4):
    return x1 > x3 and x2 > x4
```
Player 1 prefers the top row if: x1 > x3 and x2 > x4

---

##### `cond_p1_dominant_bot(x1, x2, x3, x4)`
Returns `True` if Player 1 strictly prefers the bot row.

```python
def cond_p1_dominant_top(x1, x2, x3, x4):
    return x3 > x1 and x4 > x2
```
Player 1 prefers the bot row if: x3 > x1 and x4 > x2

---

##### `cond_p2_dominant_lef(y1, y2, y3, y4)`
Returns `True` if Player 2 strictly prefers the left column.

```python
def cond_p2_dominant_left(y1, y2, y3, y4):
    return y1 > y2 and y3 > y4
```
Player 2 prefers the left column if: y1 > y2 and y3 > y4

---

##### `cond_p2_dominant_right(y1, y2, y3, y4)`
Returns `True` if Player 2 strictly prefers the right column.

```python
def cond_p2_dominant_right(y1, y2, y3, y4):
    return y2 > y1 and y4 > y1
```
Player 2 prefers the left column if: y2 > y1 and y4 > y1

---


## Configuration

The `CONFIG_GAMES` dictionary defines structural presets for sampling 2x2 games.

- Player dominance conditions
- Structural descriptors
- Expected Nash equilibrium (NE) locations

```python
{
    "p1_cond": cond_p1_dominant_top,
    "p2_cond": cond_p2_dominant_left,
    "structure": {
        "dominance": {
            "p1": "top",
            "p2": "left"
        }
    },
    "nash_locations": ["TL"]
}
```