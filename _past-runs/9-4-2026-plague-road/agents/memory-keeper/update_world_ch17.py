import json
from pathlib import Path

BASE = Path('/home/jakub/repositories/afternoon-writer/.afternoon/plans/memory/world')
CH = 'chapter17'


def append_unique(items, new_items):
    seen = {json.dumps(item, sort_keys=True) for item in items}
    for item in new_items:
        marker = json.dumps(item, sort_keys=True)
        if marker not in seen:
            items.append(item)
            seen.add(marker)


def update_topic(slug, new_facts, md_intro):
    path = BASE / f'{slug}.json'
    data = json.loads(path.read_text())
    append_unique(data.setdefault('facts', []), new_facts)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')

    lines = [f"# {data['topic'].title()}", '', md_intro, '', '## Key facts']
    for fact in data['facts'][-6:]:
        lines.append(f"- {fact['fact']} ({fact['established']})")
    lines.append('')
    (BASE / f'{slug}.md').write_text('\n'.join(lines))


update_topic(
    'geography',
    [
        {'fact': 'Stratholme’s inner wall can be reached from the main gate by service lanes that let small groups move laterally without crossing the main kill zones.', 'established': CH},
        {'fact': 'Crusaders’ Square is visible from the wall line, making it a public stage for what the city is becoming rather than an unseen interior district.', 'established': CH},
        {'fact': 'Alonsus Chapel’s bells can carry over the wall and adjacent districts, tying sacred sound to the same urban space as the purge.', 'established': CH},
    ],
    'Chapter 17 turns Stratholme’s map into witness geometry. The city is no longer just a destination; it is a set of routes, walls, and sightlines that determine who can escape, who can observe, and what can no longer be denied.',
)

update_topic(
    'politics',
    [
        {'fact': 'Arthas claims immediate crown authority at Stratholme and treats contradiction as refusal rather than counsel.', 'established': CH},
        {'fact': 'Uther’s public refusal turns private worry about the prince into an open command rupture inside Lordaeron’s own hierarchy.', 'established': CH},
        {'fact': 'Jaina’s refusal leaves the purge without Kirin Tor moral cover and makes her split with Arthas visible to witnesses on the ground.', 'established': CH},
    ],
    'Chapter 17 makes the crisis constitutional as well as moral. Authority stops being abstract and becomes a visible struggle over who can command soldiers, define necessity, and still claim legitimacy afterward.',
)

update_topic(
    'military',
    [
        {'fact': 'Uther withdraws every knight and soldier he can pull from Arthas’s line rather than lend the purge the legitimacy of the Silver Hand.', 'established': CH},
        {'fact': 'The Culling is presented as tactically coherent from the wall: once distribution has reached the population, the prince’s answer is legible as containment through annihilation.', 'established': CH},
        {'fact': 'Service-lane movement and wall observation become survival tactics for noncombatant witnesses trapped inside a city that has become an active kill box.', 'established': CH},
    ],
    'Chapter 17 records military truth without softening moral truth. The purge reads as something soldiers can understand tactically, which is exactly why the chapter treats it as so horrifying.',
)

update_topic(
    'economy',
    [
        {'fact': 'Grain carters, service routes, kitchens, and market access are all part of the same urban distribution web that makes Stratholme impossible to save cleanly once contamination is widespread.', 'established': CH},
        {'fact': 'A fleeing grain carter can still give useful routing intelligence, showing that commercial movement remains the city’s most legible map even during collapse.', 'established': CH},
        {'fact': 'The Culling only becomes thinkable because the contaminated grain economy has already crossed from warehouses into ordinary household consumption.', 'established': CH},
    ],
    'The chapter keeps proving that logistics decide fate first. By the time princes argue at the gate, the grain economy has already done its work in kitchens, carts, and bodies.',
)

update_topic(
    'religion',
    [
        {'fact': 'Alonsus Chapel and its bells place the purge inside explicitly sacred civic space rather than at a remove from Lordaeron’s religious life.', 'established': CH},
        {'fact': 'Uther’s refusal at Stratholme binds the ethics of the Silver Hand to disobedience rather than obedience when royal command demands atrocity.', 'established': CH},
    ],
    'Chapter 17 lets religion ring through the horror instead of standing outside it. Sacred architecture, paladin conscience, and public slaughter all occupy the same audible space.',
)

timeline_path = BASE / 'timeline.json'
timeline = json.loads(timeline_path.read_text())
entry = {
    'chapter': CH,
    'timespan': 'One compressed stretch from the gate confrontation through the first visible hours of the purge.',
    'keyEvents': [
        'Arthas hears Jaina confirm that it is too late to save Stratholme cleanly and orders the Culling.',
        'Uther refuses publicly and withdraws his people; Jaina refuses as well, severing herself from Arthas in plain view.',
        'Sylvanas, Jaina, and Cyndia use a service lane to reach the inner wall and witness the purge take hold below them.',
        'Arthas reappears beneath the wall with his hands washed clean, giving the chapter its final image.',
    ],
}
if not any(ch.get('chapter') == CH for ch in timeline.get('chapters', [])):
    timeline.setdefault('chapters', []).append(entry)
timeline_path.write_text(json.dumps(timeline, indent=2, ensure_ascii=False) + '\n')

timeline_md = [
    '# Timeline',
    '',
    '## Chapter chronology',
]
for ch in timeline['chapters'][-5:]:
    timeline_md.append(f"### {ch['chapter']}")
    timeline_md.append(ch['timespan'])
    timeline_md.append('')
    for ev in ch['keyEvents']:
        timeline_md.append(f"- {ev}")
    timeline_md.append('')
(BASE / 'timeline.md').write_text('\n'.join(timeline_md))

index_path = BASE / '_index.json'
index = json.loads(index_path.read_text())
for entry in index['entries']:
    if entry['slug'] in {'geography', 'politics', 'military', 'economy', 'religion', 'timeline'}:
        entry['lastAppearance'] = CH
index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + '\n')
