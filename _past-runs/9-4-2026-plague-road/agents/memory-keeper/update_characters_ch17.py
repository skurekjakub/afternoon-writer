import json
from pathlib import Path

BASE = Path('/home/jakub/repositories/afternoon-writer/.afternoon/plans/memory/characters')
CH = 'chapter17'

updates = {
    'sylvanas-windrunner': {
        'append': {
            'physicalDetails': [
                {'detail': "At Stratholme's gate she reads as held violence: bow-ready, road-hard, and still enough that the whole arch seems to brace around her while Arthas decides.", 'chapter': CH},
                {'detail': 'On the wall she becomes pure witness geometry — both hands on the parapet, body angled toward the citywide pattern and toward Jaina at once, carrying horror without letting it shake her out of function.', 'chapter': CH},
            ],
            'voiceMarkers': [
                {'detail': 'Chapter 17 pares her speech down to command bone — “Move,” “Which road,” “Don’t stop” — because anything longer would only waste breath inside catastrophe already choosing its shape.', 'chapter': CH},
                {'detail': 'Her silence becomes a marker in its own right once the wall witness begins: she stops translating horror into talk and keeps the chapter anchored in cold, exact judgment.', 'chapter': CH},
            ],
            'beliefs': [
                {'belief': 'A tactically coherent answer can still be morally unforgivable.', 'trueOrFalse': 'Confirmed in chapter 17; Sylvanas reads the Culling clearly enough to see why it works and refuses to let that clarity excuse it.', 'chapter': CH},
                {'belief': 'Once the clean rescue is gone, witness becomes its own duty.', 'trueOrFalse': 'Confirmed in chapter 17 by her choice to reach the wall instead of either fleeing the city or joining Arthas’s line.', 'chapter': CH},
            ],
            'formerBeliefs': [
                {'belief': 'Arthas might still remain a usable hard ally if his answer stayed inside brutal containment rather than crossing into something worse.', 'chapter': 'chapter16', 'changedIn': CH, 'whyItChanged': 'Chapter 17 shows Arthas answering “too late” with deliberate civic slaughter, not contained quarantine. The line Sylvanas hoped still existed is gone by the time he emerges under the gate with washed hands.'}
            ],
            'decisionsThisChapter': [
                {'detail': 'The moment Arthas turns Jaina’s answer into policy, Sylvanas abandons any hope of influencing the decision and focuses on getting Jaina clear without losing sight of what the prince is doing.', 'chapter': CH},
                {'detail': 'She follows Cyndia into the service side instead of staying beneath the main arch, choosing witness and survival over futile argument.', 'chapter': CH},
                {'detail': 'She trusts a fleeing grain carter’s route intelligence long enough to reach the inner wall above Market Row.', 'chapter': CH},
                {'detail': 'She stays on the wall through the whole purge so the truth of Stratholme arrives to her as pattern, scale, and cost rather than rumor.', 'chapter': CH},
            ],
            'abilitiesDemonstrated': [
                {'ability': 'Can read a citywide military operation from partial sightlines fast enough to understand district sequencing, reserve use, and where method is replacing panic.', 'chapter': CH},
                {'ability': 'Can keep another witness moving and alive inside crowd crush and urban collapse without losing her own larger tactical read.', 'chapter': CH},
            ],
            'bodyLanguagePatterns': [
                {'detail': 'Catches Jaina by the elbow hard enough to get bone and turns that grip into motion before the gate can freeze them in place.', 'chapter': CH},
                {'detail': 'On the wall she keeps shifting by inches rather than steps, tracking Jaina in the corner of her eye while taking the city quarter by quarter across the parapet.', 'chapter': CH},
            ],
            'knowledge': [
                {'detail': 'Now knows Uther’s warning about Arthas has ripened into open fact: once the prince hears there is no clean save left, he crosses instantly into purge logic.', 'chapter': CH},
                {'detail': 'Knows Stratholme can be denied to a mass rising by controlled sectional slaughter, and that tactical truth has become one more damnation instead of any comfort.', 'chapter': CH},
                {'detail': 'Carries the image of Arthas emerging with washed hands and emptied eyes, a cleaner and more damning proof than battlefield blood could have been.', 'chapter': CH},
            ],
        },
        'goalsAtChapterEnd': {
            'active': 'Keep Jaina upright, hold the witness line, and carry the truth of Stratholme out alive.',
            'underlying': 'Track what Arthas has become now that the last hope of contained necessity has collapsed into deliberate atrocity.',
            'chapter': CH,
        },
        'emotionalStateAtChapterEnd': {
            'state': 'Horrified, ice-clear, and grimly fused to Jaina by shared witness. She understands the method below them and hates it more for being legible.',
            'chapter': CH,
        },
        'arc': {
            'currentPosition': 'Chapter 17 destroys Sylvanas’s last hope that Arthas might remain a hard ally inside a bounded answer. She ends the chapter as witness rather than partner, holding two truths at once: the Culling works tactically, and that fact damns the man who chose it.',
            'lastChapter': CH,
        },
    },
    'jaina-proudmoore': {
        'append': {
            'physicalDetails': [
                {'detail': 'At the gate she is flour-gray and visibly used up — one hand still dirty from the failed store run, ash on her cuff, knuckles raw from the staff, smaller without magic and harder hit for it.', 'chapter': CH},
                {'detail': 'On the wall she goes so still Sylvanas keeps tracking her like a weapon-hand: loose hair stuck to her temple, flour still in her skin seams, body holding itself together by refusal rather than strength.', 'chapter': CH},
            ],
            'voiceMarkers': [
                {'detail': 'Chapter 17 gives Jaina almost no language after the gate. Her most important speech act is refusal itself: plain, direct, and utterly unwilling to let necessity flatter itself into virtue.', 'chapter': CH},
                {'detail': 'After the refusal, silence becomes her voice marker. She keeps witness through posture and presence rather than explanation, as if anything more would only cheapen what the city is doing below them.', 'chapter': CH},
            ],
            'beliefs': [
                {'belief': 'Even when the city cannot be saved cleanly, refusal still matters.', 'trueOrFalse': 'Confirmed in chapter 17. Jaina cannot stop Arthas, but she will not let him borrow her authority for the slaughter.', 'chapter': CH},
                {'belief': 'Shared witness can carry moral truth farther than one more argument inside a broken command chain.', 'trueOrFalse': 'Active and supported in chapter 17 by the way she remains beside Sylvanas on the wall instead of retreating into private collapse.', 'chapter': CH},
            ],
            'decisionsThisChapter': [
                {'detail': 'Refuses Arthas outright when he turns her truthful answer into an order to purge the city.', 'chapter': CH},
                {'detail': 'Leaves the gate with Sylvanas and Cyndia instead of staying inside Arthas’s command line or following Uther out of the scene.', 'chapter': CH},
                {'detail': 'Keeps moving through the service lanes and up to the wall even after the first screams make clear there is nothing left to save cleanly.', 'chapter': CH},
                {'detail': 'Stays on the wall through the Culling, bearing witness instead of looking away from what her answer enabled but did not choose.', 'chapter': CH},
            ],
            'abilitiesDemonstrated': [
                {'ability': 'Can hold to the morally exact answer under direct command pressure even when that answer costs her the last usable fantasy of rescue.', 'chapter': CH},
                {'ability': 'Can endure prolonged witness after magical exhaustion, staying present to what is happening instead of dropping into abstraction or collapse.', 'chapter': CH},
            ],
            'bodyLanguagePatterns': [
                {'detail': 'Closes her flour-gray hand once on the staff before refusing Arthas, turning the whole argument into one visible act of self-command.', 'chapter': CH},
                {'detail': 'Flinches at the first human scream in the service lane and keeps moving anyway, making endurance look less like courage than like necessity.', 'chapter': CH},
                {'detail': 'By the final image her hand lies flat on the parapet, white at the knuckles, and stays there until the last of Arthas’s column has gone from sight.', 'chapter': CH},
            ],
            'knowledge': [
                {'detail': 'Now knows what her truthful answer becomes in Arthas’s hands once rescue has failed: public policy at the gate and district-by-district slaughter inside the walls.', 'chapter': CH},
                {'detail': 'Sees that Arthas’s method will prevent a full citywide turn while still remaining an atrocity beyond any language of clean necessity.', 'chapter': CH},
                {'detail': 'Leaves the chapter with the clean-hands image added to every earlier hurt attached to Arthas.', 'chapter': CH},
            ],
        },
        'goalsAtChapterEnd': {
            'active': 'Stay beside the truth of Stratholme and survive the witness of what Arthas has done.',
            'underlying': 'Refuse to let either failure or necessity turn the Culling into a lie she helps tell.',
            'chapter': CH,
        },
        'emotionalStateAtChapterEnd': {
            'state': 'Shocked, hollowed out, and rigid with witness. She is past argument and past rescue, left only with refusal, ruin, and the sight of Arthas returning with clean hands.',
            'chapter': CH,
        },
        'arc': {
            'currentPosition': 'Chapter 17 moves Jaina from truth-teller at the gate to silent co-witness on the wall. The chapter no longer asks whether her answer is correct; it makes her live inside what correctness costs when the only man with power turns it into slaughter.',
            'lastChapter': CH,
        },
    },
    'arthas-menethil': {
        'append': {
            'physicalDetails': [
                {'detail': 'At Stratholme’s gate he arrives road-dusted and all edge, the princely face emptied of heat the instant Jaina says no clean rescue remains.', 'chapter': CH},
                {'detail': 'During the Culling he appears only in flashes of white-blond hair, plate shoulder, and mounted command through smoke, more function than man.', 'chapter': CH},
                {'detail': 'When he returns under the arch, his gauntlets are off and his hands are washed clean to the wrists, with eyes that read not fevered but emptied out and wrong.', 'chapter': CH},
            ],
            'voiceMarkers': [
                {'detail': 'Chapter 17 flattens his voice instead of raising it. The calm is what makes the order carry: level enough to travel farther than a shout and colder for never sounding out of control.', 'chapter': CH},
                {'detail': 'He answers moral resistance with curt finality — “They’re dead already,” “Then stand aside,” “I didn’t ask” — as if contradiction is only delay in another uniform.', 'chapter': CH},
                {'detail': 'His command voice to Falric is stripped to execution language, not persuasion or rallying speech; the city is treated as a task already underway.', 'chapter': CH},
            ],
            'beliefs': [
                {'belief': 'If a city is already seeded, killing the living in controlled sections is preferable to letting the dead claim it all at once.', 'trueOrFalse': 'Active in chapter 17. The prose makes the logic tactically legible while refusing to redeem the choice morally.', 'chapter': CH},
                {'belief': 'Once he has the answer he needs, dissent becomes obstruction rather than counsel.', 'trueOrFalse': 'Confirmed in chapter 17 by the speed with which he sheds both Uther and Jaina from the command chain.', 'chapter': CH},
            ],
            'decisionsThisChapter': [
                {'detail': 'Orders the gates sealed once his column is through so no one leaves without his word.', 'chapter': CH},
                {'detail': 'Publicly announces the Culling and frames it as a street-by-street, house-by-house military necessity.', 'chapter': CH},
                {'detail': 'Rejects Uther’s refusal and Jaina’s refusal alike, then gives Falric direct instructions to take the first companies through Market Row and burn resistance.', 'chapter': CH},
                {'detail': 'Continues the purge district by district until the city falls quiet under ordered fire and rotation.', 'chapter': CH},
                {'detail': 'Returns beneath the gate only after washing, presenting himself to the wall witnesses in a deliberately cleaner state than the city he has just destroyed.', 'chapter': CH},
            ],
            'abilitiesDemonstrated': [
                {'ability': 'Can convert a citywide atrocity into disciplined urban doctrine, sequencing troops, fire, reserves, and cleared lanes instead of letting the action degrade into riot.', 'chapter': CH},
                {'ability': 'Can hold command cohesion even through a public moral split with both mentor and former lover, keeping his officers and soldiers moving at his chosen pace.', 'chapter': CH},
            ],
            'nameUsagePatterns': {
                'howOthersAddressHim': [
                    {'speaker': 'Captain Falric', 'pattern': 'Uses “my prince” in immediate obedience, confirming that the command edge around Arthas is still personal as well as hierarchical.', 'chapter': CH}
                ],
                'howHeAddressesOthers': [
                    {'target': 'Captain Falric', 'pattern': 'Uses Falric’s name as a release trigger for action; by chapter 17 the captain is less confidant than execution hinge.', 'chapter': CH}
                ]
            },
            'bodyLanguagePatterns': [
                {'detail': 'His face empties rather than flares when Jaina answers, making blankness itself the warning sign.', 'chapter': CH},
                {'detail': 'Turns away from Uther and Jaina without losing pace, as if shedding them is only one more movement inside the larger operation.', 'chapter': CH},
                {'detail': 'Looks straight up at the wall after the purge, holding the witness line long enough to make the pause feel chosen.', 'chapter': CH},
            ],
            'knowledge': [
                {'detail': 'Now knows beyond dispute that Jaina’s source-side method was real and still too late at city scale.', 'chapter': CH},
                {'detail': 'Knows Uther and Jaina have both refused him in public and proceeds anyway, which means he understands the moral line and chooses to cross it knowingly.', 'chapter': CH},
            ],
        },
        'goalsAtChapterEnd': {
            'active': 'Finish the purge and move on to the next necessity without surrendering command momentum.',
            'underlying': 'Deny the plague a full citywide rising by forcing the city into sections he can still control.',
            'chapter': CH,
        },
        'emotionalStateAtChapterEnd': {
            'state': 'Emptied out, colder than fury, and past the need to justify himself. By chapter end he reads less like a prince under strain than like a man who has made room inside himself for atrocity and already moved beyond it.',
            'chapter': CH,
        },
        'arc': {
            'currentPosition': 'Chapter 17 is the irreversible crossing. Arthas no longer merely hardens under truth; he turns truth into mass killing, breaks publicly with every remaining restraint, and returns from the city washed clean enough to make the choice feel finished inside him.',
            'lastChapter': CH,
        },
    },
    'uther': {
        'append': {
            'physicalDetails': [
                {'detail': 'At the gate he stands with his hammer low and final, the older body reading less as hesitation than as an oath refusing to move one inch toward the prince’s order.', 'chapter': CH},
            ],
            'voiceMarkers': [
                {'detail': 'Chapter 17 distills Uther’s voice to blunt moral plainness: “No” and then the harder sentence, “They are alive until you kill them.” He does not sermonize because the field no longer needs explanation.', 'chapter': CH},
            ],
            'beliefs': [
                {'belief': 'No future corruption makes the living expendable before they have actually died.', 'trueOrFalse': 'Confirmed in chapter 17 by Uther’s public refusal at the gate.', 'chapter': CH},
            ],
            'decisionsThisChapter': [
                {'detail': 'Refuses Arthas’s purge order publicly at the main gate instead of saving the disagreement for a private aftermath.', 'chapter': CH},
                {'detail': 'Takes with him every knight and soldier willing to follow the moral line he names, creating an immediate open break inside the command chain.', 'chapter': CH},
            ],
            'abilitiesDemonstrated': [
                {'ability': 'Can turn moral authority into immediate military consequence, pulling real men out of a prince’s line simply by naming the difference aloud.', 'chapter': CH},
            ],
            'bodyLanguagePatterns': [
                {'detail': 'Steps forward without rush and without visible uncertainty, making refusal read as weight rather than as reaction.', 'chapter': CH},
                {'detail': 'Takes Arthas’s dismissal by wheeling his horse instead of arguing into futility, turning the break physical in front of everyone at the gate.', 'chapter': CH},
            ],
            'knowledge': [
                {'detail': 'Now knows Arthas will answer “too late” with civic slaughter rather than any narrower containment.', 'chapter': CH},
                {'detail': 'Leaves the gate having witnessed the exact moment his warning about Arthas stopped being forecast and became public fact.', 'chapter': CH},
            ],
        },
        'goalsAtChapterEnd': {
            'active': 'Stand outside Arthas’s purge and carry away every man he can still keep from participating in it.',
            'underlying': 'Refuse the prince’s line in public before necessity can overwrite the difference between living citizens and condemned dead.',
            'chapter': CH,
        },
        'emotionalStateAtChapterEnd': {
            'state': 'Final, heartsick, and morally unbent. Chapter 17 strips him of any remaining hope that warning or side lanes might brake Arthas in time.',
            'chapter': CH,
        },
        'arc': {
            'currentPosition': 'Chapter 17 carries Uther from warning witness to open breaker of the command chain. He no longer stands beside Arthas as counterweight; he stands against him and leaves with whoever still understands the difference.',
            'lastChapter': CH,
        },
    },
    'falric': {
        'append': {
            'physicalDetails': [
                {'detail': 'At the gate Falric reads as pure command edge under strain: already moving before orders finish, stone-faced beneath dust and exhaustion, one of the men through whom the prince’s will becomes civic disaster.', 'chapter': CH},
            ],
            'voiceMarkers': [
                {'detail': 'Chapter 17 reduces him to immediate assent — “My prince,” “Yes, my prince” — the language of a man whose usefulness lies in never adding friction.', 'chapter': CH},
            ],
            'beliefs': [
                {'belief': 'Once Arthas commits, the officer nearest him must make the order real before anyone else can stop it.', 'trueOrFalse': 'Confirmed in chapter 17 by Falric’s instant conversion of the gate space into purge logistics.', 'chapter': CH},
            ],
            'decisionsThisChapter': [
                {'detail': 'Moves to seal the gate before Arthas’s sentence has fully cleared the arch.', 'chapter': CH},
                {'detail': 'Takes command of the first companies entering the city through Market Row under Arthas’s purge order.', 'chapter': CH},
                {'detail': 'Keeps the execution edge stone-clean even through the public split with Uther and Jaina.', 'chapter': CH},
            ],
            'abilitiesDemonstrated': [
                {'ability': 'Can turn a prince’s spoken decision into immediate gate action, troop movement, and urban-entry sequencing with almost no lag.', 'chapter': CH},
            ],
            'nameUsagePatterns': {
                'howOthersAddressHim': [
                    {'speaker': 'Arthas Menethil', 'pattern': 'Uses “Falric” as the name that means the argument is over and execution begins.', 'chapter': CH}
                ],
                'howHeAddressesOthers': []
            },
            'bodyLanguagePatterns': [
                {'detail': 'Moves before the sentence clears, making obedience look less like choice than like preloaded motion.', 'chapter': CH},
            ],
            'knowledge': [
                {'detail': 'By the end of chapter 17 Falric is operating with full practical knowledge of Arthas’s answer at Stratholme: seal, enter, burn, and do not wait for consensus.', 'chapter': CH},
            ],
        },
        'goalsAtChapterEnd': {
            'active': 'Drive the first companies through the city and keep the purge line functioning.',
            'underlying': 'Make Arthas’s order operational before moral rupture at the gate can slow the army.',
            'chapter': CH,
        },
        'emotionalStateAtChapterEnd': {
            'state': 'Stone-faced, overdriven, and fully subsumed into execution work. Chapter 17 gives him no visible private reaction, only function.',
            'chapter': CH,
        },
        'arc': {
            'currentPosition': 'Chapter 17 turns Falric from worn logistics hinge into the prince’s immediate cutting edge. He is still not the source of the decision, but now he is unmistakably one of the men who makes it real.',
            'lastChapter': CH,
        },
    },
    'cyndia': {
        'append': {
            'physicalDetails': [
                {'detail': 'In chapter 17 she is the body that makes motion possible: hauling a horse broadside across the lane, running ahead through service turns, and taking the wall without once asking whether the route is the right one emotionally.', 'chapter': CH},
                {'detail': 'Once on the wall she settles into outward scan again, taking the other crenel and working exits, rooflines, and fallback stairs while the city dies below them.', 'chapter': CH},
            ],
            'voiceMarkers': [
                {'detail': 'Her chapter-17 speech is nearly pure route shorthand — “Service side,” “Left here,” “Tallow cut. Wheelwright. Feed crane.” The fewer words, the faster the line survives.', 'chapter': CH},
                {'detail': 'After the wall view opens, her silence has the same quality as her earlier field reporting: she sees, sorts, and only speaks if a route fact will change something.', 'chapter': CH},
            ],
            'beliefs': [
                {'belief': 'When command space becomes moral wreckage, the ranger’s job is to find the survivable line and keep the witnesses moving through it.', 'trueOrFalse': 'Confirmed in chapter 17 by her immediate shift from gate chaos to service-lane extraction and wall placement.', 'chapter': CH},
            ],
            'decisionsThisChapter': [
                {'detail': 'Uses her horse as moving cover to break the first crush away from the gate and open a lane for Sylvanas and Jaina.', 'chapter': CH},
                {'detail': 'Calls the service-side route immediately instead of letting the trio freeze beneath Arthas’s order.', 'chapter': CH},
                {'detail': 'Takes the grain carter’s directions and converts them into an immediate path to the inner wall.', 'chapter': CH},
                {'detail': 'Once on the wall, shifts from movement support to exit-read duty, keeping fallback lanes in mind while Sylvanas and Jaina witness the purge.', 'chapter': CH},
            ],
            'abilitiesDemonstrated': [
                {'ability': 'Can improvise crowd-and-horse geometry inside urban panic, turning one mounted body into a temporary shield wall.', 'chapter': CH},
                {'ability': 'Can convert civilian route intelligence into immediate tactical movement through unfamiliar service geography.', 'chapter': CH},
            ],
            'bodyLanguagePatterns': [
                {'detail': 'Gets the horse broadside before anyone finishes thinking through the crush, making her response visibly faster than explanation.', 'chapter': CH},
                {'detail': 'On the wall she takes one look over Sylvanas’s shoulder at the city and says nothing, a silence that reads as comprehension rather than numbness.', 'chapter': CH},
            ],
            'knowledge': [
                {'detail': 'Now knows Stratholme’s service-side geography well enough to move from lane to stair under pressure: tallow cut, wheelwright yard, feed crane, inner wall.', 'chapter': CH},
                {'detail': 'Sees the Culling as organized district work rather than uncontrolled panic, even if Sylvanas is the one who fully prices the method below.', 'chapter': CH},
            ],
        },
        'goalsAtChapterEnd': {
            'active': 'Keep the witness line survivable by holding routes, exits, and fallback movement from the wall.',
            'underlying': 'Make sure Sylvanas and Jaina can see what is happening without being swallowed by the same urban machine.',
            'chapter': CH,
        },
        'emotionalStateAtChapterEnd': {
            'state': 'Tight, disciplined, and appalled into silence. Chapter 17 leaves her functioning at full usefulness while the scale below the wall strips reaction down to essentials.',
            'chapter': CH,
        },
        'arc': {
            'currentPosition': 'Chapter 17 extends Cyndia from source-run flank support into witness support: she is now the ranger who can get the others to the right wall, hold the exit geometry, and let the chapter’s moral center stay visible without collapse.',
            'lastChapter': CH,
        },
    },
}


def append_unique_list(existing, items, key):
    seen = {(entry.get(key), entry.get('chapter')) for entry in existing if isinstance(entry, dict)}
    for item in items:
        marker = (item.get(key), item.get('chapter'))
        if marker not in seen:
            existing.append(item)
            seen.add(marker)


def append_unique_exact(existing, items):
    seen = {json.dumps(entry, sort_keys=True) for entry in existing}
    for item in items:
        marker = json.dumps(item, sort_keys=True)
        if marker not in seen:
            existing.append(item)
            seen.add(marker)


def ensure_history(data, field, history_field):
    current = data.get(field)
    if not current:
        return
    if current.get('chapter') == CH:
        return
    hist = data.setdefault(history_field, [])
    marker = json.dumps(current, sort_keys=True)
    seen = {json.dumps(entry, sort_keys=True) for entry in hist}
    if marker not in seen:
        hist.append(current)


def ensure_arc_history(data):
    arc = data.get('arc') or {}
    current = arc.get('currentPosition')
    last = arc.get('lastChapter')
    if not current or last == CH:
        return
    hist = data.setdefault('arcHistory', [])
    entry = {'currentPosition': current, 'chapter': last}
    marker = json.dumps(entry, sort_keys=True)
    seen = {json.dumps(item, sort_keys=True) for item in hist}
    if marker not in seen:
        hist.append(entry)


def add_name_usage(data, extra):
    if not extra:
        return
    name_usage = data.setdefault('nameUsagePatterns', {})
    for section in ('howOthersAddressHim', 'howHeAddressesOthers', 'howOthersAddressHer', 'howSheAddressesOthers'):
        if section in extra:
            cur = name_usage.setdefault(section, [])
            append_unique_exact(cur, extra[section])


def render_markdown(data):
    latest_details = []
    for field, key in [
        ('physicalDetails', 'detail'),
        ('voiceMarkers', 'detail'),
        ('beliefs', 'belief'),
        ('decisionsThisChapter', 'detail'),
        ('abilitiesDemonstrated', 'ability'),
        ('knowledge', 'detail'),
    ]:
        vals = [item[key] for item in data.get(field, []) if isinstance(item, dict) and item.get('chapter') == CH and key in item]
        if vals:
            latest_details.append((field, vals))

    lines = []
    lines.append(f"# {data['name']}")
    lines.append('')
    lines.append('## Overview')
    lines.append(data['arc']['currentPosition'])
    lines.append('')
    lines.append('## Current chapter position')
    lines.append(
        f"At the end of {CH}, {data['goalsAtChapterEnd']['active'].lower()} {data['goalsAtChapterEnd']['underlying'].lower()} "
        f"The emotional register is {data['emotionalStateAtChapterEnd']['state'].lower()}"
    )
    lines.append('')
    lines.append('## The Gate update')
    for field, vals in latest_details:
        if field == 'physicalDetails':
            lines.append(f"Physically, {vals[0]}")
            if len(vals) > 1:
                lines.append(vals[1])
        elif field == 'voiceMarkers':
            lines.append(f"In voice and silence, {vals[0]}")
            if len(vals) > 1:
                lines.append(vals[1])
        elif field == 'beliefs':
            lines.append(f"The chapter locks in that {vals[0].lower()}")
            if len(vals) > 1:
                lines.append(vals[1])
        elif field == 'decisionsThisChapter':
            lines.append(f"Key choices: {vals[0]}")
            for extra in vals[1:3]:
                lines.append(extra)
        elif field == 'abilitiesDemonstrated':
            lines.append(f"What this chapter proves they can do: {vals[0]}")
            if len(vals) > 1:
                lines.append(vals[1])
        elif field == 'knowledge':
            lines.append(f"What the chapter leaves them knowing: {vals[0]}")
            for extra in vals[1:3]:
                lines.append(extra)
    lines.append('')
    lines.append('## Arc and carry-forward')
    lines.append(f"Lie: {data['arc']['lie']}")
    lines.append(f"Truth: {data['arc']['truth']}")
    lines.append(f"Current position: {data['arc']['currentPosition']}")
    lines.append('')
    return '\n'.join(lines).strip() + '\n'


for slug, upd in updates.items():
    path = BASE / f'{slug}.json'
    data = json.loads(path.read_text())
    data['lastAppearance'] = CH

    ensure_history(data, 'goalsAtChapterEnd', 'goalsHistory')
    ensure_history(data, 'emotionalStateAtChapterEnd', 'emotionalStateHistory')
    ensure_arc_history(data)

    app = upd['append']
    for field in ['physicalDetails', 'voiceMarkers', 'beliefs', 'decisionsThisChapter', 'abilitiesDemonstrated', 'bodyLanguagePatterns', 'knowledge']:
        if field in app:
            target = data.setdefault(field, [])
            key = 'belief' if field == 'beliefs' else ('ability' if field == 'abilitiesDemonstrated' else 'detail')
            append_unique_list(target, app[field], key)
    if 'formerBeliefs' in app:
        target = data.setdefault('formerBeliefs', [])
        append_unique_exact(target, app['formerBeliefs'])
    if 'nameUsagePatterns' in app:
        add_name_usage(data, app['nameUsagePatterns'])

    data['goalsAtChapterEnd'] = upd['goalsAtChapterEnd']
    data['emotionalStateAtChapterEnd'] = upd['emotionalStateAtChapterEnd']
    data['arc']['currentPosition'] = upd['arc']['currentPosition']
    data['arc']['lastChapter'] = upd['arc']['lastChapter']

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    (BASE / f'{slug}.md').write_text(render_markdown(data))

index_path = BASE / '_index.json'
index = json.loads(index_path.read_text())
for entry in index['entries']:
    if entry['slug'] in updates:
        entry['lastAppearance'] = CH
index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + '\n')
