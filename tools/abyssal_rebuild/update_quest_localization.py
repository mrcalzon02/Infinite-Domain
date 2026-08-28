#!/usr/bin/env python3
"""[SYSTEM REPORT] Idempotently install Infinite Domain abyssal FTB Quests localization."""
from __future__ import annotations
import argparse
from pathlib import Path

LINES = [
    '\tchapter.7AB0550C00000001.title: "Abyssal Recovery"',
    '\tchapter.7AB0550C00000001.subtitle: "Submarine evidence recovery across the Pelagos and Karsic abyss"',
    '\tquest.5AB0550C00000001.title: "Western Continental Slope"',
    '\tquest.5AB0550C00000001.quest_desc: ["Take the pressure-capable submarine beyond the western shelf. Reaching the Pelagos-facing continental slope provides a recovery bearing to a drowned survey wreck."]',
    '\tquest.5AB0550C00000002.title: "Pelagos Survey Wreck"',
    '\tquest.5AB0550C00000002.quest_desc: ["Enter the mapped Pelagos survey wreck. The structure contains the navigation package needed to prove the voyage; merely finding the wreck is not the recovery."]',
    '\tquest.5AB0550C00000003.title: "Return the Navigation Core"',
    '\tquest.5AB0550C00000003.quest_desc: ["Recover the Abyssal Navigation Core from the wreck and carry it back into the settlement safe zone. Evidence only matters if civilization gets it home."]',
    '\tquest.5AB0550C00000004.title: "Eastern Continental Slope"',
    '\tquest.5AB0550C00000004.quest_desc: ["Repeat the deep-water survey on the Karsic-facing eastern slope. The bearing leads to a military-industrial patrol wreck rather than a Pelagos research vessel."]',
    '\tquest.5AB0550C00000005.title: "Karsic Patrol Wreck"',
    '\tquest.5AB0550C00000005.quest_desc: ["Enter the mapped Karsic patrol wreck and locate its protected subsea data recorder. The recorder is physical evidence, not an automatic exploration reward."]',
    '\tquest.5AB0550C00000006.title: "Return the Data Recorder"',
    '\tquest.5AB0550C00000006.quest_desc: ["Bring the recovered Karsic Subsea Data Recorder back into the settlement safe zone for analysis."]',
    '\tquest.5AB0550C00000007.title: "Two Sides of the Abyss"',
    '\tquest.5AB0550C00000007.quest_desc: ["Compare the Pelagos navigation core with the Karsic recorder. Together they establish that both powers maintained deep-ocean systems and expose routes farther into the abyss."]',
    '\tquest.5AB0550C00000008.title: "Pelagos Abyssal Plain"',
    '\tquest.5AB0550C00000008.quest_desc: ["Descend beyond the western slope into the abyssal plain. Survey data points toward a Pelagos communications and bathymetric relay on the seabed."]',
    '\tquest.5AB0550C00000009.title: "Pelagos Abyssal Relay"',
    '\tquest.5AB0550C00000009.quest_desc: ["Enter the flooded relay and recover its Pelagos Bathymetric Survey Log from the guaranteed evidence chest. The recovered depth record provides the next bearing into the fracture field."]',
    '\tquest.5AB0550C0000000A.title: "Pelagos Fracture Observatory"',
    '\tquest.5AB0550C0000000A.quest_desc: ["Reach the western fracture field, enter the observatory, and recover its hardened Fracture Sensor Core. The installation was measuring unstable terrain far below ordinary shipping depth."]',
    '\tquest.5AB0550C0000000B.title: "Pelagos Hadal Probe Station"',
    '\tquest.5AB0550C0000000B.quest_desc: ["Enter the western hadal trench and recover the Hadal Pressure Record from the probe station. This is the deepest surviving Pelagos evidence in the current expedition chain."]',
    '\tquest.5AB0550C0000000C.title: "Karsic Abyssal Plain"',
    '\tquest.5AB0550C0000000C.quest_desc: ["Descend beyond the eastern slope into the abyssal plain. Karsic records point toward a subsea pipeline maintenance station embedded in the industrial network."]',
    '\tquest.5AB0550C0000000D.title: "Karsic Pipeline Station"',
    '\tquest.5AB0550C0000000D.quest_desc: ["Enter the flooded pipeline station and recover its Telemetry Package from the evidence chest. The flow and maintenance record exposes a deeper surveillance route."]',
    '\tquest.5AB0550C0000000E.title: "Karsic Fracture Listening Post"',
    '\tquest.5AB0550C0000000E.quest_desc: ["Reach the eastern fracture field, enter the passive-acoustic listening post, and recover the Karsic Sonar Archive. Its final contacts point toward restricted hadal operations."]',
    '\tquest.5AB0550C0000000F.title: "Karsic Hadal Blacksite"',
    '\tquest.5AB0550C0000000F.quest_desc: ["Penetrate the breached outer bunker and inner archive vault of the Karsic hadal blacksite. Recover the encrypted Blacksite Cipher from its guaranteed evidence chest."]',
    '\tquest.5AB0550C00000010.title: "The Abyss Compared"',
    '\tquest.5AB0550C00000010.quest_desc: ["Bring together the Pelagos pressure record and Karsic blacksite cipher. The resulting Comparative Abyssal Dossier closes the first bilateral deep-ocean investigation without granting an industrial progression shortcut."]',
]

BLOCK = '\n'.join(LINES)
KEYS = [line.lstrip().split(':', 1)[0] for line in LINES]

def install(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    if BLOCK in text:
        print('abyssal localization already installed exactly')
        return False
    conflicts = [key for key in KEYS if f'{key}:' in text]
    if conflicts:
        raise SystemExit('Refusing to overwrite partial/conflicting abyssal localization: ' + ', '.join(conflicts))
    end = text.rfind('}')
    if end < 0 or text[end + 1:].strip():
        raise SystemExit('FTB Quests language file does not end in one root compound')
    updated = text[:end].rstrip() + '\n' + BLOCK + '\n}\n'
    path.write_text(updated, encoding='utf-8')
    print(f'installed {len(LINES)} abyssal localization entries into {path}')
    return True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('path', nargs='?', default='config/ftbquests/quests/lang/en_us.snbt')
    args = ap.parse_args()
    install(Path(args.path))

if __name__ == '__main__':
    main()
