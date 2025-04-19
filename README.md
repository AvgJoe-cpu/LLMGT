# 🧠 LLMGT

[![Docs](https://img.shields.io/badge/docs-live-blue?style=flat-square)](https://avgjoe-cpu.github.io/LLMGT/)

Structured evaluation of large language models in 2x2 competitive-simultaneous games.


📚 **Documentation**  
→ [View the full site](https://avgjoe-cpu.github.io/LLMGT/)

--- 

## Dataset creation

We construct a dataset of 2×2 games with labeled structure: NE, dominance profiles, and payoff matrices derived from constraint-based sampling.
We support two formats: NE-only and fully labeled.

For dataset construction, see the [build_games module documentation](https://avgjoe-cpu.github.io/LLMGT/build_games.html)  
or the [source file](src/llmgt/data/build_games.py).

For intuition, see the [Game-Theoretic Justification (PDF)](docs/game_theory_description.pdf).

See [Duan et al., 2024](#-references) (GTBench) and [Wang et al., 2024](#-references) (TMGBench) for benchmark-style LLM evaluations.



## References
- **Duan et al. (2024).**  
  *GTBench: Uncovering the Strategic Reasoning Limitations of LLMs via Game-Theoretic Evaluations*.  
  arXiv:2402.12348. [arXiv](https://arxiv.org/abs/2402.12348)

- **Wang et al. (2024).**  
  *TMGBench: A Systematic Game Benchmark for Evaluating Strategic Reasoning Capabilities of LLMs*.  
  arXiv:2410.10479. [arXiv](https://arxiv.org/abs/2410.10479)

- **Sreedhar & Chilton (2024).**  
  *Simulating Human Strategic Behavior: Comparing Single and Multi-agent LLMs*.  
  arXiv:2402.08189. [arXiv](https://arxiv.org/abs/2402.08189)
