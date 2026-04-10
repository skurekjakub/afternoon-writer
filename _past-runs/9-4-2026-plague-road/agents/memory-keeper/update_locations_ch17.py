import json
from pathlib import Path

BASE = Path('/home/jakub/repositories/afternoon-writer/.afternoon/plans/memory/locations')
CH = 'chapter17'


def write_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def render_location_md(data):
    lines = [
        f"# {data['name']}",
        '',
        '## Overview',
        f"{data['name']} sits in {data['region']}. In {CH}, the location is defined by {data['sensoryProfile']['atmosphere'].lower()}",
        '',
        '## Sensory profile',
        f"- Sight: {data['sensoryProfile']['sight']}",
        f"- Sound: {data['sensoryProfile']['sound']}",
        f"- Smell: {data['sensoryProfile']['smell']}",
        f"- Touch: {data['sensoryProfile']['touch']}",
        f"- Atmosphere: {data['sensoryProfile']['atmosphere']}",
        '',
        '## Established facts',
    ]
    for fact in data.get('establishedFacts', [])[-6:]:
        lines.append(f"- {fact['fact']} ({fact['chapter']})")
    lines.append('')
    lines.append('## Chapter 17 movement')
    for event in data.get('eventsHere', [])[-4:]:
        lines.append(f"- {event['event']} ({event['chapter']})")
    lines.append('')
    return '\n'.join(lines) + '\n'


stratholme_path = BASE / 'stratholme.json'
stratholme = json.loads(stratholme_path.read_text())
stratholme['lastAppearance'] = CH
stratholme['sensoryProfile'] = {
    'sight': 'The southern main gate choked with soldiers and horses, flour-white service lanes, smoke lifting in separate columns, torch lines cutting the street grid, and a city reduced from civic space to ordered districts under fire.',
    'sound': 'Alonsus Chapel bells still trying to mark an ordinary hour, shouted orders clipped short under the gate, doors being broken in rhythm, screams spreading and then thinning, and finally the quiet of burning timber after human voices are worked out of the streets.',
    'smell': 'Bread, wet burlap, horse piss, rank tallow, smoke, and the sweet-sour wrongness of the plague underneath every working urban smell.',
    'touch': 'Crushed sacks in mud, rough service-stair stone, soot on the parapet, and city air hot enough to carry sparks up to the wall.',
    'atmosphere': 'Chapter 17 turns Stratholme from a salvage target into a witnessed atrocity: logistically legible, militarily coherent, and morally unbearable.',
}

existing_facts = {(f['fact'], f['chapter']) for f in stratholme.get('establishedFacts', [])}
new_facts = [
    {'fact': "Stratholme's southern main gate functions as both ceremonial threshold and public command stage, which is why Arthas's order lands as theatre as well as policy.", 'chapter': CH},
    {'fact': 'The goods-side service lane can still carry civilians and scouts to an inner-wall stair above Market Row even after the main gate breaks into panic.', 'chapter': CH},
    {'fact': 'Market Row is the city’s broad commercial spine and the first district Arthas assigns to Falric’s companies.', 'chapter': CH},
    {'fact': 'From the inner wall, the city reads as separable districts with separate smoke columns and rotation lines rather than one uncontrolled riot.', 'chapter': CH},
    {'fact': 'Alonsus Chapel and the square around it remain audible and tactically central during the opening of the Culling, with bells sounding until the city’s silence overtakes them.', 'chapter': CH},
    {'fact': 'Arthas returns beneath the same gate on foot after the purge, washed clean enough to make the city look more stained by contrast.', 'chapter': CH},
]
for fact in new_facts:
    if (fact['fact'], fact['chapter']) not in existing_facts:
        stratholme.setdefault('establishedFacts', []).append(fact)

for name in ['Arthas Menethil', 'Jaina Proudmoore', 'Sylvanas Windrunner', 'Cyndia', 'Uther the Lightbringer', 'Captain Falric', 'grain carter']:
    if name not in stratholme['charactersPresentHere']:
        stratholme['charactersPresentHere'].append(name)

existing_events = {(e['event'], e['chapter']) for e in stratholme.get('eventsHere', [])}
new_events = [
    {'event': 'Arthas turns Jaina’s report into the public order to cull the city and breaks openly with both Uther and Jaina at the main gate.', 'chapter': CH},
    {'event': 'Sylvanas, Jaina, and Cyndia escape the gate crush through the service lane and reach the inner wall above Market Row with help from a fleeing grain carter.', 'chapter': CH},
    {'event': 'From the wall, the women witness the Culling as a district-by-district military process rather than a chaotic riot.', 'chapter': CH},
    {'event': 'Arthas emerges below the wall after the purge with washed hands, giving the chapter its final image of Stratholme.', 'chapter': CH},
]
for event in new_events:
    if (event['event'], event['chapter']) not in existing_events:
        stratholme.setdefault('eventsHere', []).append(event)

write_json(stratholme_path, stratholme)
(BASE / 'stratholme.md').write_text(render_location_md(stratholme))

alonsus = {
    'name': 'Alonsus Chapel',
    'slug': 'alonsus-chapel',
    'region': 'Stratholme, near the central civic square and the routes feeding Market Row.',
    'firstAppearance': CH,
    'lastAppearance': CH,
    'sensoryProfile': {
        'sight': 'Seen mostly at distance through smoke and square geometry, as a civic holy center still anchoring the city while soldiers and runners knot around it.',
        'sound': 'Its bells carry across the opening of the Culling, trying to impose hour and order on a city already sliding into slaughter.',
        'smell': 'Smoke, city ash, and the same bread-and-burning mixture that reaches the wall from the streets below.',
        'touch': 'Felt indirectly through the tolling that reaches the witnesses before the chapel itself does.',
        'atmosphere': 'A holy landmark trapped inside civic desecration.',
    },
    'establishedFacts': [
        {'fact': 'Alonsus Chapel is one of Stratholme’s major holy landmarks and the traditional birthplace of the Silver Hand.', 'chapter': CH},
        {'fact': 'Its bells are still sounding when Arthas announces the Culling at the gate.', 'chapter': CH},
        {'fact': 'The square around the chapel becomes one of the visible knots of reserve, runners, and controlled troop movement during the purge.', 'chapter': CH},
    ],
    'charactersPresentHere': ['Arthas Menethil forces below', 'reserve riders', 'runners'],
    'eventsHere': [
        {'event': 'The bells of Alonsus Chapel ring over Arthas’s order until the city’s silence finally swallows them.', 'chapter': CH},
    ],
}
write_json(BASE / 'alonsus-chapel.json', alonsus)
(BASE / 'alonsus-chapel.md').write_text(render_location_md(alonsus))

crusaders = {
    'name': "Crusaders' Square",
    'slug': 'crusaders-square',
    'region': 'Stratholme, just off the Market Row / Alonsus Chapel axis.',
    'firstAppearance': CH,
    'lastAppearance': CH,
    'sensoryProfile': {
        'sight': 'An open square visible from the wall, broad enough to hold shields, horses, and reserve movement while nearby streets burn in separate slices.',
        'sound': 'Runner traffic, barked orders, and the harder echo of organized movement through open stone instead of alley confinement.',
        'smell': 'Smoke and hot stone carried out of the city center.',
        'touch': 'Read at distance as a staging surface rather than intimate ground.',
        'atmosphere': 'A civic open space repurposed into one more clean lane inside massacre.',
    },
    'establishedFacts': [
        {'fact': "Crusaders' Square is a major open district of Stratholme tied to the city’s central civic / holy core.", 'chapter': CH},
        {'fact': "In chapter 17 it serves as a visible staging lane and reserve knot during Arthas's purge.", 'chapter': CH},
        {'fact': 'Its position near Market Row helps make the Culling readable from the wall as organized district work instead of simple collapse.', 'chapter': CH},
    ],
    'charactersPresentHere': ['Arthas Menethil forces below', 'runners', 'shield lines'],
    'eventsHere': [
        {'event': "Crusaders' Square functions as a holding and staging knot during the Culling, visible from the wall witness position.", 'chapter': CH},
    ],
}
write_json(BASE / 'crusaders-square.json', crusaders)
(BASE / 'crusaders-square.md').write_text(render_location_md(crusaders))

index_path = BASE / '_index.json'
index = json.loads(index_path.read_text())
entries = {entry['slug']: entry for entry in index['entries']}
entries['stratholme']['lastAppearance'] = CH
entries.setdefault('alonsus-chapel', {
    'name': 'Alonsus Chapel',
    'slug': 'alonsus-chapel',
    'aliases': [],
    'firstAppearance': CH,
    'lastAppearance': CH,
})
entries.setdefault("crusaders-square", {
    'name': "Crusaders' Square",
    'slug': "crusaders-square",
    'aliases': [],
    'firstAppearance': CH,
    'lastAppearance': CH,
})
index['entries'] = sorted(entries.values(), key=lambda x: x['name'].lower())
write_json(index_path, index)
