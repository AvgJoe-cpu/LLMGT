# 🧠 LLMGT

[![Docs](https://img.shields.io/badge/docs-live-blue?style=flat-square)](https://avgjoe-cpu.github.io/LLMGT/)

Structured evaluation of large language models in 2x2 competitive-simultaneous games.


📚 **Documentation**  
→ [View the full site](https://avgjoe-cpu.github.io/LLMGT/)

--- 

## Dataset creation

We construct a dataset of 2×2 games with labeled structure: NE, dominance profiles, and payoff matrices derived from constraint-based sampling.
Two formats are supported: NE-only and fully labeled.

For dataset construction, see the [build_games module documentation](build_games/)  
or the [source file](src/llmgt/data/build_games.py).

For theoretical context, see the [Game-Theoretic Justification (PDF)](https://avgjoe-cpu.github.io/LLMGT/games_intuition.pdf).





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
