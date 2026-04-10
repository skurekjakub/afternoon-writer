import json
from pathlib import Path

BASE = Path('/home/jakub/repositories/afternoon-writer/.afternoon/plans/memory/relationships')
CH = 'chapter17'

updates = {
    'jaina--sylvanas': {
        'currentState': 'Shared witness welds the damaged partnership into something harder than reassurance. Chapter 17 leaves them side by side on the wall, saying almost nothing and not leaving each other.',
        'powerDynamic': 'Sylvanas controls movement, survival geometry, and the military read; Jaina controls the truth that made the gate break and the moral frame that keeps the wall witness from curdling into admiration for method. Neither woman can carry the chapter alone.',
        'physicalDynamics': [
            {'pattern': 'Sylvanas takes Jaina by the elbow at the gate and never really lets the chapter lose that line of bodily custody-turned-protection.', 'chapter': CH},
            {'pattern': 'In the service lane they move in compressed relay: Cyndia opening space, Sylvanas pushing, Jaina keeping pace because standing still would be worse.', 'chapter': CH},
            {'pattern': 'On the wall they keep falling into the same inches of shelter and the same parapet line, letting placement do the work of all the speech the chapter refuses them.', 'chapter': CH},
        ],
        'nameUsage': {
            'sylvanasCallsJaina': 'Very little spoken naming in chapter 17; the relationship is carried through imperative motion and silent witness rather than verbal address.',
            'jainaCallsSylvanas': 'Likewise reduced almost to silence. Whatever the partnership is by chapter end lives in where she stands, not in what she calls her.',
        },
        'history': [
            {'event': 'Sylvanas gets Jaina out from beneath Arthas’s order and onto the service-side witness route instead of leaving her alone at the gate.', 'chapter': CH},
            {'event': 'The inner-wall vigil finishes what the source run began: shared witness locks the partnership into place without requiring spoken repair.', 'chapter': CH},
            {'event': 'The final clean-hands image becomes something both women carry together, even though only Jaina owns the older history inside it.', 'chapter': CH},
        ],
        'trajectory': 'Hostile containment -> operational pair -> damaged persistence -> chosen recommitment through work -> chapter 17’s silent wall-side weld.',
    },
    'arthas--jaina': {
        'currentState': 'The old intimacy finally breaks on an irreversible moral line. Jaina gives Arthas the truth; Arthas turns that truth into slaughter and casts her refusal aside.',
        'powerDynamic': 'Jaina has the last accurate answer. Arthas still has the army, the gate, and the ability to decide what that answer becomes in the city below them.',
        'physicalDynamics': [
            {'pattern': 'The chapter begins with distance already charged: Jaina fixed where she answered, Arthas emptying out in front of her instead of breaking.', 'chapter': CH},
            {'pattern': 'Their final physical exchange is almost entirely about stance: Jaina holding the staff, Arthas turning the city into order, then later looking up at her from below the wall with washed hands.', 'chapter': CH},
        ],
        'nameUsage': {
            'jainaCallsArthas': 'Chapter 17 strips even his name out of her speech after the answer. Refusal replaces intimacy entirely.',
            'arthasCallsJaina': 'He stops using even formal courtesy once the truth is no longer useful for persuasion. She becomes one more dissenting voice to step past.',
        },
        'history': [
            {'event': 'Jaina refuses to help Arthas purge the city the instant he turns her answer into policy.', 'chapter': CH},
            {'event': 'Arthas answers her refusal with dismissal rather than argument, making the break public and final under the gate.', 'chapter': CH},
            {'event': 'The chapter ends with Jaina above him on the wall and Arthas below with clean hands, a visual separation that says more than any remaining dialogue could.', 'chapter': CH},
        ],
        'trajectory': 'Former lovers -> institutional bruise -> parallel answers -> chapter 17’s public and irreversible moral split.',
    },
    'arthas--sylvanas': {
        'currentState': 'Professional respect collapses into witness judgment. Sylvanas stops reading Arthas as a dangerous ally and starts reading him as the man who chose Stratholme.',
        'powerDynamic': 'Arthas still holds force, officers, and civic threshold. Sylvanas no longer contests that power directly; she holds the clearer judgment of what he has done and what image of him will carry forward.',
        'physicalDynamics': [
            {'pattern': 'They share the same gate only briefly before Arthas turns inward toward the city and Sylvanas turns sideways toward witness and survival.', 'chapter': CH},
            {'pattern': 'The last meaningful body language between them is vertical rather than conversational: Arthas below the wall looking up, Sylvanas above it refusing to move.', 'chapter': CH},
        ],
        'nameUsage': {
            'arthasCallsSylvanas': 'No meaningful direct address in chapter 17; the relationship has moved beyond consultation.',
            'sylvanasCallsArthas': 'He is no longer a field lever in her head by chapter end, but the man attached to the clean-hands image.',
        },
        'history': [
            {'event': 'Sylvanas watches Arthas convert Jaina’s no into the Culling without trying to pretend the act still belongs inside hard necessity.', 'chapter': CH},
            {'event': 'From the wall she reads the purge clearly enough to see both its tactical method and its moral rot, which permanently reclassifies Arthas in her internal file.', 'chapter': CH},
            {'event': 'Arthas deliberately looks up at the wall after the purge, acknowledging witnesses rather than avoiding them.', 'chapter': CH},
        ],
        'trajectory': 'Formal first contact -> useful but dangerous military lever -> clean strategic divergence -> chapter 17’s witness-based condemnation.',
    },
    'arthas--uther': {
        'currentState': 'Open rupture. Chapter 17 finally pays Uther’s warning off in public: mentor and prince choose opposite answers under the same city gate and part in full view of the line.',
        'powerDynamic': 'Arthas keeps the purge and the companies willing to follow him. Uther keeps moral authority and enough soldiers to make refusal physically real instead of merely verbal.',
        'physicalDynamics': [
            {'pattern': 'Uther steps forward with his hammer low while Arthas answers from the same stillness, making the whole split happen through posture before the men behind them choose sides.', 'chapter': CH},
            {'pattern': 'The horse wheel is the chapter’s decisive gesture between them: Uther turning away with his own people while Arthas rides into the city without slowing.', 'chapter': CH},
        ],
        'nameUsage': {
            'arthasCallsUther': 'The old direct-name habit now lands as pure dismissal rather than shared history.',
            'utherCallsArthas': 'Still bare Arthas, but chapter 17 turns the familiarity into accusation and last appeal at once.',
        },
        'history': [
            {'event': 'Uther publicly refuses the Culling instead of contesting Arthas only in private counsel.', 'chapter': CH},
            {'event': 'Arthas tells him to take every knight and soldier who still knows the difference, effectively acknowledging the split as irreparable in the moment.', 'chapter': CH},
        ],
        'trajectory': 'Mentor warning -> parallel answers -> chapter 17’s open command-chain fracture.',
    },
    'cyndia--jaina': {
        'currentState': 'Practical witness pair. Cyndia is no longer only Jaina’s movement support for the source plan; in chapter 17 she becomes one of the two people who physically carry Jaina into the wall witness.',
        'powerDynamic': 'Jaina still holds the truth that makes the chapter possible; Cyndia holds route clarity and immediate bodily support whenever that truth threatens to freeze the group in place.',
        'physicalDynamics': [
            {'pattern': 'Cyndia opens the first lane with her horse and keeps calling routes while Jaina, exhausted and stunned, obeys on the strength of motion rather than will.', 'chapter': CH},
            {'pattern': 'Once on the wall they do not pair emotionally, but they do pair functionally: Jaina at the parapet, Cyndia at the outward angle keeping the line survivable.', 'chapter': CH},
        ],
        'nameUsage': {
            'cyndiaCallsJaina': 'Very little direct naming; chapter 17 reduces them to pure movement coordination.',
            'jainaCallsCyndia': 'Equally sparse. Their relationship is now carried by trust in Cyndia’s route sense rather than spoken formality.',
        },
        'history': [
            {'event': 'Cyndia gets Jaina off the gate line by calling the service-side route before shock can freeze her in place.', 'chapter': CH},
            {'event': 'The chapter extends their chapter-15 head-start collaboration from source-run logistics into shared witness logistics.', 'chapter': CH},
        ],
        'trajectory': 'Guarded escort -> operational run pair -> chapter 17’s practical witness partnership.',
    },
    'cyndia--sylvanas': {
        'currentState': 'Trusted command pair in witness mode. Chapter 17 shows their shorthand surviving a moral catastrophe: Cyndia opens space and names routes, Sylvanas decides once and moves at once.',
        'powerDynamic': 'Sylvanas still chooses the line; Cyndia still makes that line physically usable before anyone else can explain it twice.',
        'physicalDynamics': [
            {'pattern': 'Cyndia hauls the horse across the lane and Sylvanas takes the gap instantly, a division of labor so practiced it barely registers as separate actions.', 'chapter': CH},
            {'pattern': 'On the wall Cyndia takes the adjacent crenel and runs exit geometry while Sylvanas takes the city read, preserving their old left-edge / whole-picture rhythm under new pressure.', 'chapter': CH},
        ],
        'nameUsage': {
            'sylvanasCallsCyndia': 'Still direct first-name command shorthand, almost stripped out of speech because the working trust is already assumed.',
            'cyndiaCallsSylvanas': 'Still compressed professional address, but chapter 17 lets route speech replace rank-heavy language whenever speed matters more.',
        },
        'history': [
            {'event': 'Cyndia’s “Service side” becomes the chapter’s first useful answer after Arthas’s order, and Sylvanas trusts it instantly.', 'chapter': CH},
            {'event': 'The pair convert a grain carter’s hurried route intelligence into a clean climb to the inner wall without breaking tempo.', 'chapter': CH},
        ],
        'trajectory': 'Trusted report chain -> survivor pair -> source-run command pair -> chapter 17’s witness-support command pair.',
    },
    'sylvanas--uther': {
        'currentState': 'Professional respect deepens into parallel moral clarity. Uther makes the public refusal; Sylvanas makes the witness line. Chapter 17 leaves them choosing different lanes for the same judgment.',
        'powerDynamic': 'Uther still names the moral line in public. Sylvanas still carries the harder tactical witness of what happens when Arthas ignores it.',
        'physicalDynamics': [
            {'pattern': 'They never need much direct interaction in chapter 17 because the chapter makes them legible through mirrored stillness on opposite sides of Arthas’s choice.', 'chapter': CH},
            {'pattern': 'Uther breaks left with the men he can save from the order while Sylvanas breaks into the city’s side lanes with the witness she can save from isolation.', 'chapter': CH},
        ],
        'nameUsage': {
            'utherCallsSylvanas': 'No major new direct naming in chapter 17; the relationship advances through coordinated moral position rather than dialogue.',
            'sylvanasCallsUther': 'Likewise minimal. He is fully inside her judgment already by the time his warning becomes fact.',
        },
        'history': [
            {'event': 'Uther’s public refusal at the gate confirms the warning he gave Sylvanas in earlier chapters.', 'chapter': CH},
            {'event': 'Sylvanas does not follow Uther out, but her wall witness becomes another form of agreement with his refusal: she will not let Arthas’s method pass for anything cleaner than atrocity.', 'chapter': CH},
        ],
        'trajectory': 'Shared alarm about Arthas -> active cooperation -> chapter 17’s parallel moral alignment under rupture.',
    },
}


def append_unique_exact(existing, items):
    seen = {json.dumps(entry, sort_keys=True) for entry in existing}
    for item in items:
        marker = json.dumps(item, sort_keys=True)
        if marker not in seen:
            existing.append(item)
            seen.add(marker)


def ensure_state_history(data):
    current = data.get('currentState')
    if not current:
        return
    if data.get('lastInteraction') == CH:
        return
    hist = data.setdefault('stateHistory', [])
    entry = {'currentState': current, 'chapter': data.get('lastInteraction')}
    marker = json.dumps(entry, sort_keys=True)
    seen = {json.dumps(item, sort_keys=True) for item in hist}
    if marker not in seen:
        hist.append(entry)


def render_md(data):
    lines = [
        f"# {' / '.join(data['characters'])}",
        '',
        '## Current state',
        data['currentState'],
        '',
        '## Power dynamic',
        data['powerDynamic'],
        '',
        '## Chapter 17 evidence',
    ]
    for item in data.get('history', [])[-3:]:
        lines.append(f"- {item['event']} ({item['chapter']})")
    lines.append('')
    lines.append('## Physical dynamic')
    for item in data.get('physicalDynamics', [])[-2:]:
        lines.append(f"- {item['pattern']} ({item['chapter']})")
    lines.append('')
    lines.append('## Trajectory')
    lines.append(data['trajectory'])
    lines.append('')
    return '\n'.join(lines)


for slug, upd in updates.items():
    path = BASE / f'{slug}.json'
    data = json.loads(path.read_text())
    ensure_state_history(data)
    data['currentState'] = upd['currentState']
    data['powerDynamic'] = upd['powerDynamic']
    data['lastInteraction'] = CH
    append_unique_exact(data.setdefault('physicalDynamics', []), upd['physicalDynamics'])
    data['nameUsage'] = upd['nameUsage']
    append_unique_exact(data.setdefault('history', []), upd['history'])
    data['trajectory'] = upd['trajectory']
    write = json.dumps(data, indent=2, ensure_ascii=False) + '\n'
    path.write_text(write)
    (BASE / f'{slug}.md').write_text(render_md(data))

index_path = BASE / '_index.json'
index = json.loads(index_path.read_text())
for entry in index['entries']:
    if entry['slug'] in updates:
        entry['lastAppearance'] = CH
index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + '\n')
