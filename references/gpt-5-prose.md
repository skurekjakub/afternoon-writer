# GPT-5 / GPT-5.4 Prose Issues Research Notes

User-requested workspace note.

Purpose: capture five focused web-search rounds on commonly reported GPT-5 / GPT-5.4 fiction-writing problems, then turn those findings into a practical revision checklist for prose work in this repo.

This is not a formal literature review. Most sources are a mix of writer blogs, editor writeups, community threads, product commentary, and comparison pieces. That is still useful here because the goal is not model benchmarking in the abstract; it is finding the recurring "this sounds AI-written" complaints that human readers actually notice.

## Search rounds

### Round 1 — Sentence rhythm, repetitiveness, sameness of structure

Main finding: GPT-5 prose is often reported as structurally repetitive even when it is grammatically clean.

Common complaints:
- sentence lengths cluster too narrowly
- paragraphs repeat the same description -> action -> thought rhythm
- prose can go choppy in an attempt to sound tense
- the model overfits prompt structure and mirrors it too literally

Useful takeaway: if a scene reads competent but monotonous, check rhythm before you check plot.

### Round 2 — Dialogue beats, character voice, subtext

Main finding: GPT-5 often makes everyone sound like variations of one polite, efficient speaker.

Common complaints:
- repetitive dialogue cadence
- flat or interchangeable voices across characters
- dialogue beats that only label emotion instead of revealing character
- subtext explained too directly
- scenes that paraphrase the emotional point after the dialogue already carried it

Useful takeaway: "same-mouth syndrome" is one of the fastest human-reader tells.

### Round 3 — Hedging, filter words, tentative language

Main finding: even when the scene skeleton works, small local phrasing still gives AI prose away.

Common complaints:
- overuse of qualifiers: `almost`, `maybe`, `probably`, `seemed`
- filter words: `noticed`, `realized`, `felt`, `thought`, `saw`, `heard`
- stacked uncertainty in one sentence
- noncommittal emotional wording that weakens impact

Useful takeaway: local diction can make otherwise good prose feel synthetic.

### Round 4 — Over-explaining, conflict flattening, pleasantness bias

Main finding: GPT-5 often tries to make fiction cleaner, safer, and less sharp than the scene wants to be.

Common complaints:
- emotional and thematic over-explanation
- scenes resolving tension too quickly
- reluctance to leave conflict raw or unresolved
- sanitized or "corporate" tone
- preference for harmony over friction

Useful takeaway: if a scene turns nicer than the characters are, the model is smoothing it.

### Round 5 — Paragraph mechanics, essay structure, tidy scene construction

Main finding: GPT-5 often defaults to essay habits inside fiction.

Common complaints:
- topic-sentence paragraphs
- list paragraphs
- scene endings that summarize instead of push forward
- tidy explanatory closure instead of ambiguity
- clean mini-essay structure where fiction should feel lived-in

Useful takeaway: paragraph shape is diagnostic, not just sentence wording.

## Consolidated failure modes

Across the five rounds, the same cluster kept resurfacing:

1. **Rhythmic sameness**
   The prose is readable but mechanically even. Sentence length, paragraph cadence, and beat shape repeat often enough that the reader begins to feel the template.

2. **Dialogue-beat genericism**
   Characters answer in similar sentence shapes, with the same kinds of micro-reactions. The result is voice flattening.

3. **Filter/hedge drag**
   The model pads direct perception with cognitive language and cushions strong beats with qualifiers.

4. **Narrative over-translation**
   The prose explains what just happened instead of trusting the image, gesture, or line of dialogue.

5. **Pleasantness bias**
   Conflict gets softened. Moral texture gets cleaned up. Tension gets resolved too politely.

6. **Essay brain**
   Paragraphs open with a claim, support it, then restate it. Scenes close with interpretation instead of propulsion.

7. **Closure addiction**
   The model likes to finish the emotional sentence. Human fiction often gets stronger by stopping earlier.

## Practical audit checklist for prose chapters

Use this after drafting or after a first cleanup pass:

### Sentence-level
- Are too many sentences built the same way in one page?
- Are there repetitive comma-plus-`ing` tails?
- Are there too many qualifiers (`almost`, `maybe`, `probably`, `seemed`)?
- Are filter verbs doing work that direct description could do better?
- Are generic dialogue-adjacent beats carrying emotion instead of specific action?

### Paragraph-level
- Do paragraphs keep opening with the same word or same structure?
- Do paragraphs sound like mini-essays?
- Does the last sentence of a paragraph explain the paragraph instead of moving it forward?
- Are there too many list paragraphs or inventory paragraphs?

### Scene-level
- Do characters sound distinct in rhythm, diction, and evasions?
- Does subtext stay under the dialogue, or does the narration translate it?
- Does the scene keep some friction alive, or does it rush to emotional neatness?
- Does the prose trust ambiguity where ambiguity is stronger?
- Does the scene end on a shift, an image, a question, or an action rather than a summary?

## What to watch for specifically in this repo

Given the repo's existing anti-slop rules, the external GPT-5 research lines up especially well with these local dangers:

- participial tail overuse
- filter words and hedge chains
- generic smile/laugh/glance scaffolding
- explanatory restatement after dialogue
- sentence/paragraph monotony
- elegant but flattened voice
- safe conflict handling
- essay-style paragraph closure

In other words: the repo hitlist is already aimed at the right target. The web research mostly confirms that the local rules are catching the exact failure modes people report for GPT-5 family fiction.

## Sources referenced during the five rounds

### Round 1
- Novelcrafter — "How Good is GPT-5 for Writing Fiction?"
  https://www.novelcrafter.com/blog/is-gpt-5-any-good-for-writing-fiction
- OpenAI Community — "Story writing - change in writing style"
  https://community.openai.com/t/story-writing-change-in-writing-style/1115400
- OpenTools — "Why GPT-5 is Frustrating Users: New Theories Emerge"
  https://opentools.ai/news/why-gpt-5-is-frustrating-users-new-theories-emerge

### Round 2
- Novelcrafter — "How Good is GPT-5 for Writing Fiction?"
  https://www.novelcrafter.com/blog/is-gpt-5-any-good-for-writing-fiction
- Tom's Hardware — "ChatGPT users revolt over GPT-5 release"
  https://www.tomshardware.com/tech-industry/artificial-intelligence/chatgpt-users-revolt-over-gpt-5-release-openai-battles-claims-that-the-new-models-accuracy-and-abilities-fall-short
- Digital Trends — "GPT-5 gave ChatGPT a new personality..."
  https://www.digitaltrends.com/computing/gpt-5-gave-chatgpt-a-whole-new-personality-and-im-not-sure-if-i-like-it/

### Round 3
- Grammarly — "Common Words and Phrases in AI-Generated Text"
  https://www.grammarly.com/blog/ai/common-ai-words/
- Knowadays — "What to Do with Tentative Language"
  https://knowadays.com/blog/what-to-do-with-tentative-language/
- Oxford Lifelong Learning — "Hedging"
  https://lifelong-learning.ox.ac.uk/about/hedging

### Round 4
- Type — "Claude vs. ChatGPT vs. Gemini: Who Wrote it Better?"
  https://blog.type.ai/post/claude-vs-gpt
- MakeUseOf — "8 Big Problems With OpenAI's ChatGPT"
  https://www.makeuseof.com/openai-chatgpt-biggest-probelms/
- Harvard Business Review — "How Generative AI Could Disrupt Creative Work"
  https://hbr.org/2023/04/how-generative-ai-could-disrupt-creative-work

### Round 5
- Wikipedia — "Signs of AI writing"
  https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- How-To Geek — "How to Get ChatGPT to Write Better Fiction"
  https://www.howtogeek.com/883023/how-to-get-chatgpt-to-write-better-fiction/
- Books+Publishing — "Can ChatGPT edit fiction? Four editors put it to the test"
  https://www.booksandpublishing.com.au/articles/2024/02/21/247408/can-chat-gpt-edit-fiction-four-editors-put-it-to-the-test/

## Bottom line

The recurring GPT-5 prose problems are not just "bad wording." They cluster at three levels:

- **micro**: qualifiers, filters, generic beats
- **meso**: paragraph sameness, essay structure, repetitive scene rhythm
- **macro**: softened conflict, explanatory closure, flattened voice

If a prose pass attacks all three levels, the output stops sounding "model-clean" and starts sounding authored.
