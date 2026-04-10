import json
from pathlib import Path

BASE = Path('/home/jakub/repositories/afternoon-writer/.afternoon/plans/memory/threads')
CH = 'chapter17'


def append_unique(items, new_items):
    seen = {json.dumps(item, sort_keys=True) for item in items}
    for item in new_items:
        marker = json.dumps(item, sort_keys=True)
        if marker not in seen:
            items.append(item)
            seen.add(marker)


def render_md(data):
    lines = [
        f"# {data['thread']}",
        '',
        f"Status: **{data['status']}**",
        '',
        '## Reader knows',
        data['readerKnows'],
        '',
        '## POV knows',
        data['povCharacterKnows'],
        '',
        '## Chapter 17 evidence',
    ]
    for item in data.get('evidence', [])[-4:]:
        lines.append(f"- {item['clue']} ({item['chapter']})")
    lines.append('')
    lines.append('## Notes')
    lines.append(data['notes'])
    lines.append('')
    return '\n'.join(lines)


def update_existing(slug, status=None, resolved=False, notes=None, reader=None, pov=None, evidence=None, last_advanced=CH):
    path = BASE / f'{slug}.json'
    data = json.loads(path.read_text())
    if evidence:
        append_unique(data.setdefault('evidence', []), evidence)
    data['lastAdvanced'] = last_advanced
    if status:
        data['status'] = status
    if resolved:
        data['status'] = 'resolved'
        data['resolvedIn'] = CH
    if reader:
        data['readerKnows'] = reader
    if pov:
        data['povCharacterKnows'] = pov
    if notes:
        data['notes'] = notes
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    (BASE / f'{slug}.md').write_text(render_md(data))


update_existing(
    'new-grain-seller',
    status='advanced',
    notes='Advanced again in chapter 17. The fifth recurrence comes from an ordinary grain carter under immediate survival pressure, which strengthens the pattern precisely because he sounds uncurated.',
    reader='The repeating farewell has now surfaced five times across villages, trap ground, army movement, and urban flight. Chapter 17 makes the pattern harder to file as coincidence and still impossible to explain cleanly.',
    pov='Sylvanas now knows the phrase can surface from a frightened carter who also offers practical route intelligence, which widens the thread beyond simple roadside memory or camp coincidence.',
    evidence=[
        {'clue': 'A fleeing grain carter in Stratholme gives the route to the inner wall and then says “May the stars keep your road” as if it were habitual ordinary luck.', 'chapter': CH},
        {'clue': 'This is the fifth known recurrence of the farewell, and it appears under immediate urban survival pressure rather than in reflective conversation.', 'chapter': CH},
    ],
)

update_existing(
    'grain-distribution-network',
    status='advanced',
    notes='Advanced in chapter 17 by showing the city-phase consequences rather than only the distribution mechanics. The network is no longer just feeding bodies; its aftermath is what Arthas chooses to answer with the Culling.',
    reader='The grain network has reached its terminal urban form: warehouses, bread flow, homes, church kitchens, and living bodies all feeding one another fast enough that the city can only be read now through consequence rather than prevention.',
    pov='Sylvanas and Jaina know exactly where the network was vulnerable and can see, from the wall, how little those vulnerabilities matter once distribution has finished crossing into a population.',
    evidence=[
        {'clue': 'Stratholme’s service routes, Market Row, and inner districts show the network already fully distributed through a living city before Arthas enters in force.', 'chapter': CH},
        {'clue': 'The Culling only becomes tactically legible because the grain system has already crossed from stores into kitchens, houses, and bodies.', 'chapter': CH},
    ],
)

update_existing(
    'stratholme-source-plan',
    resolved=True,
    notes='Resolved in chapter 17. The answer is now publicly locked: the source plan was correct, locally effective, and too late to save the city cleanly.',
    reader='There is no remaining suspense about whether the source plan could save Stratholme cleanly. By chapter 17 the answer is fixed as no: it worked at warehouse scale, but the city had already eaten too much of the plague.',
    pov='Jaina, Sylvanas, and Cyndia know the method succeeded where it could touch concentrated stock. Arthas hears the same answer and turns it into purge logic instead of rescue.',
    evidence=[
        {'clue': 'Jaina’s plain no at the gate becomes the city’s final answer on the source plan before Arthas commits the purge.', 'chapter': CH},
        {'clue': 'Nothing in chapter 17 reopens the possibility of a clean citywide save; the chapter instead dramatizes the consequences of its loss.', 'chapter': CH},
    ],
)

update_existing(
    'uthers-warning-about-arthas',
    resolved=True,
    notes='Resolved in chapter 17. Uther’s warning mattered as diagnosis, not as brake; by the time the truth arrived plainly, Arthas was already beyond stopping.',
    reader='The answer is no. Uther understood Arthas correctly, but that understanding did not prevent the Culling. It only made the break at the gate legible when it came.',
    pov='Uther and Sylvanas now know the warning was accurate and late in the only way that matters: it predicted the line Arthas would cross, but not in time to stop him crossing it.',
    evidence=[
        {'clue': 'Uther refuses the purge order publicly and leaves with every knight and soldier he can pull out of Arthas’s line.', 'chapter': CH},
        {'clue': 'Arthas ignores the refusal and proceeds with the Culling anyway, confirming that Uther’s warning was not enough to prevent the disaster it named.', 'chapter': CH},
    ],
)

update_existing(
    'arthas-hearthglen-thread',
    resolved=True,
    notes='Resolved in chapter 17. Arthas becomes the outside force the field team reached for, but he answers Stratholme in the worst available way.',
    reader='The thread’s answer is yes, but catastrophically. Arthas is reached, present, and fully operational at Stratholme — and his intervention becomes the Culling.',
    pov='Sylvanas and Jaina no longer have to wonder what Arthas will do once he has the truth. Chapter 17 gives them the answer in full view of the gate and the wall.',
    evidence=[
        {'clue': 'Arthas reaches Stratholme’s gate in time to hear Jaina’s answer and to set policy for the city immediately.', 'chapter': CH},
        {'clue': 'His answer is the Culling, resolving the question of what kind of outside force Hearthglen and the road had delivered into the crisis.', 'chapter': CH},
    ],
)

clean_hands = {
    'thread': 'What does Arthas’s clean-hands image mean for the chapters after Stratholme?',
    'slug': 'arthas-clean-hands-image',
    'planted': CH,
    'lastAdvanced': CH,
    'status': 'open',
    'relevantCharacters': ['Arthas Menethil', 'Jaina Proudmoore', 'Sylvanas Windrunner'],
    'evidence': [
        {'clue': 'After the purge, Arthas emerges beneath the gate on foot with his gauntlets off and his hands washed clean to the wrists.', 'chapter': CH},
        {'clue': 'He looks up at the wall where Jaina and Sylvanas are standing, making the image consciously witnessed rather than accidental.', 'chapter': CH},
    ],
    'readerKnows': 'Stratholme hands the next chapter one unforgettable visual wound: Arthas has time to cleanse himself before returning to view, which makes the atrocity feel not only committed but absorbed.',
    'povCharacterKnows': 'Jaina and Sylvanas share the same image, but not the same history inside it. Both now know the sight will travel farther than a report ever could.',
    'notes': 'New in chapter 17. Keep this open into the immediate aftermath chapters, especially wherever Jaina has to look at Arthas again or name what changed in him.',
}
(BASE / 'arthas-clean-hands-image.json').write_text(json.dumps(clean_hands, indent=2, ensure_ascii=False) + '\n')
(BASE / 'arthas-clean-hands-image.md').write_text(render_md(clean_hands))

index_path = BASE / '_index.json'
index = json.loads(index_path.read_text())
entries = {entry['slug']: entry for entry in index['entries']}
for slug in [
    'new-grain-seller',
    'grain-distribution-network',
    'stratholme-source-plan',
    'uthers-warning-about-arthas',
    'arthas-hearthglen-thread',
]:
    entries[slug]['lastAppearance'] = CH
entries.setdefault('arthas-clean-hands-image', {
    'name': 'What does Arthas’s clean-hands image mean for the chapters after Stratholme?',
    'slug': 'arthas-clean-hands-image',
    'aliases': [],
    'firstAppearance': CH,
    'lastAppearance': CH,
})
index['entries'] = sorted(entries.values(), key=lambda x: x['name'].lower())
index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + '\n')
