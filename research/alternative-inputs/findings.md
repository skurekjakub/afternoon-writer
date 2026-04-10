# Alternative Inputs to LLMs for Prose Writing

Date: 2026-04-07

## Question

Is there research support for giving an LLM something other than plain prose as input, and does that improve results, especially for prose writing and story generation?

## Method

I ran 10 differently worded web searches around:

1. structured prompts vs plain natural language
2. story generation from outlines / beat sheets / plot graphs
3. chain-of-thought / scratchpads / program-of-thought
4. controllable narrative generation from scene plans and event graphs
5. tabular / schema / markup prompt formats
6. beat plans / chapter outlines / scene cards in fiction writing
7. outline-conditioned long-range story consistency
8. plan-and-write vs direct story generation
9. narrative beats / event chains / plot graphs for character consistency
10. structured intermediate representations for long-form creative writing

Search quality was mixed. Conclusions below are weighted toward ACL / NAACL / AIIDE / ACM / arXiv / conference or formal research pages, not blog summaries.

## Executive conclusion

Short version:

- Yes, there is meaningful research support for using alternatives to plain prose input.
- For prose writing, the strongest support is for **structured narrative scaffolds**:
  - outlines
  - beat plans
  - scene cards
  - event graphs
  - multi-stage plan-then-draft pipelines
- There is much weaker direct evidence that **JSON/XML/tables by themselves** make fiction better at the sentence level.
- Structured formats help most reliably with:
  - coherence
  - long-range consistency
  - plot control
  - character/state tracking
  - constraint satisfaction

Practical reading of the literature:

- If the question is "Should the model receive a structured chapter/scene plan instead of only a prose brief?" -> **probably yes**.
- If the question is "Should I rewrite story notes into JSON/XML and expect better prose just because the format is structured?" -> **evidence is weak**.

## Confidence-weighted take

### High confidence

Structured narrative planning artifacts improve long-form story generation more than plain one-shot prose prompting.

This is the cleanest and most repeated signal across the narrative-generation papers that surfaced.

### Medium confidence

Machine-readable schemas help controllability and consistency when the task is heavily structured, but the gain is usually about reliability and constraint-following, not literary quality.

### Low confidence

Raw format swapping alone (for example, prose brief -> JSON brief, with no change in planning depth) reliably improves prose aesthetics.

I did not find strong evidence for that narrower claim.

## What the strongest prose-writing evidence supports

### 1) Detailed outlines improve long-story coherence

The clearest result I found is **DOC: Improving Long Story Coherence with Detailed Outline Control** (ACL 2023).

Reported gains from detailed outline control:

- +22.5% absolute gain in plot coherence
- +28.2% higher outline relevance
- +20.7% higher interestingness

The core move is simple: shift more work into a detailed plan, then expand locally instead of asking the model to carry the whole story in free prose at once.

Interpretation:

- the outline acts like external long-range memory
- it reduces contradiction and drift
- it keeps segment-level generation pointed at a larger shape

### 2) Outline-conditioned and plan-then-draft systems keep showing up

Multiple systems surfaced that follow the same broad pattern:

- make an outline or event plan first
- allocate events to sections or chapters
- expand one segment at a time
- optionally revise with another pass

Examples:

- **StoryWriter: A Multi-Agent Framework for Long Story Generation** (2025)
- **Navigating the Path of Writing: Outline-guided Text Generation with Planning**
- older **plan-and-write** style research repeatedly referenced in search summaries

The repeated reported benefits are:

- better global coherence
- better local-to-global alignment
- stronger theme / plot tracking
- fewer contradictions
- easier author control

### 3) Narrative beats and event graphs are a serious alternative input

The fiction-specific literature does not just use outlines. It also uses:

- narrative beats
- event chains
- plot graphs
- symbolic plot plans
- knowledge-enhanced story schemas

Relevant examples:

- **NarrativeGenie** uses narrative beats and partially ordered event structures
- **Coherent Story Generation with Structured Knowledge** uses schema-like structure before surface realization
- **NGEP** uses graph-based event planning
- **Guiding and Diversifying LLM-Based Story Generation via Answer Set Programming** uses symbolic high-level story structures before prose expansion
- **STORYTELLER** uses plot planning plus entity / relationship tracking

The reported benefits cluster around:

- better plot control
- stronger causal flow
- better character consistency
- more diversity without total drift
- better handling of long stories than direct free generation

### 4) Long-form story benchmarks support the same conclusion from the other side

Benchmark work like **Lost in Stories / ConStory-Bench** matters because it frames the failure mode directly:

- long plain generation drifts
- facts get contradicted
- timelines slide
- world rules get forgotten
- characters lose consistency

That does not by itself prove one specific replacement input is best, but it strongly supports the need for explicit scaffolding outside plain prose.

## What the broader prompt-format research says

This part is real, but it needs to be interpreted carefully.

Research on prompt formatting and structured inputs suggests that:

- format matters
- structure can change performance materially
- JSON / YAML / HTML / tables can improve consistency and controllability
- the best format is task-dependent

Examples that surfaced:

- **Does Prompt Formatting Have Any Impact on LLM Performance?** (2024)
- **Better Think with Tables**
- structured data prompt-comparison work across JSON / YAML / CSV / hybrids

But this literature is mostly strongest for tasks like:

- extraction
- reasoning
- structured generation
- schema-constrained outputs
- table understanding

For prose writing, this does **not** automatically translate to:

- better sentences
- better voice
- better dramatic pressure

It translates more safely to:

- better control
- better decomposition
- better routing between stages
- better verification surfaces

## Chain-of-thought and scratchpads

The searches also surfaced strong evidence that:

- chain-of-thought
- scratchpads
- explicit intermediate reasoning

can outperform plain direct prompting on reasoning-heavy tasks.

That matters here only indirectly.

For fiction systems, the closest analogue is not "make the draft read like a scratchpad." It is:

- give the system intermediate planning objects
- let one phase reason in structure
- let another phase write prose

So the lesson is architectural, not stylistic.

## Best-supported alternative inputs for prose pipelines

If the goal is better fiction output, the literature most strongly supports these alternatives to plain prose-only input:

1. **Hierarchical outlines**
   - chapter outline
   - scene outline
   - beat outline

2. **Beat plans / scene cards**
   - intention
   - conflict
   - turn
   - exit condition
   - continuity hooks

3. **Event or plot graphs**
   - useful when control and causal structure matter more than naturalness at planning time

4. **State representations**
   - character state
   - relationship state
   - world-state / rule tracking
   - unresolved thread lists

5. **Multi-stage plan -> draft -> verify pipelines**
   - planning representation first
   - prose second
   - verification against the plan afterward

## What seems weak or overstated

These claims are not well-supported by what I found:

- "JSON alone makes fiction prose better."
- "Any structured format is automatically better than prose."
- "Prompt formatting research on tables / schemas cleanly transfers to literary quality."

The more defensible version is:

- structure helps when it externalizes planning, memory, or constraints
- structure helps less when it is only cosmetic reformatting

## Working conclusion for this repo / similar fiction pipelines

If this repo wants to exploit the research direction cleanly, the most evidence-backed move is:

- keep prose writing in prose
- move planning and control upstream into structure
- use explicit scene / beat / continuity representations before drafting
- use verification passes that read the structure, not just the prose

In other words:

- **structured planning input** looks research-backed
- **structured markup alone as a prose-quality booster** looks much less backed

## Strongest sources from this pass

### Narrative / prose-writing relevant

- **DOC: Improving Long Story Coherence with Detailed Outline Control**  
  https://aclanthology.org/2023.acl-long.190/

- **StoryWriter: A Multi-Agent Framework for Long Story Generation**  
  https://arxiv.org/abs/2506.16445

- **Navigating the Path of Writing: Outline-guided Text Generation with Planning**  
  https://arxiv.org/html/2404.13919v1

- **Coherent Story Generation with Structured Knowledge**  
  https://aclanthology.org/2023.ranlp-1.74/

- **NarrativeGenie: Generating Narrative Beats and Dynamic Storytelling with Large Language Models**  
  https://ojs.aaai.org/index.php/AIIDE/article/download/31868/34035

- **Guiding and Diversifying LLM-Based Story Generation via Answer Set Programming**  
  https://arxiv.org/html/2406.00554v1

- **Wordcraft: Story Writing With Large Language Models**  
  https://dl.acm.org/doi/fullHtml/10.1145/3490099.3511105

- **Lost in Stories: Consistency Bugs in Long Story Generation by LLMs**  
  https://arxiv.org/abs/2603.05890

### Broader prompt-format / structure relevant

- **Does Prompt Formatting Have Any Impact on LLM Performance?**  
  https://arxiv.org/abs/2411.10541

- **Better Think with Tables: Tabular Structures Enhance LLM Comprehension**  
  https://arxiv.org/html/2412.17189v3

- **Prompt engineering for structured data: a comparative evaluation of styles and LLM performance**  
  https://www.cs.wm.edu/~dcschmidt/PDF/Optimizing_Prompt_Styles_for_Structured_Data_Generation_in_LLM.pdf

- **Chain-of-Thought Prompting Elicits Reasoning in Large Language Models**  
  https://arxiv.org/pdf/2201.11903

## Bottom-line answer

Yes, there is research support for alternative inputs to LLMs.

For prose writing, the strongest support is for **structured narrative plans** rather than plain prose prompts.

If forced into one sentence:

> The research mostly says "give the model a plan, beats, events, or state to write from," not "wrap the same story brief in JSON and expect magic."
