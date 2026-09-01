# Queued Revision: Charles Quest Voice and Mobile Terminal

Status: **Implemented 2026-08-14; in-game visual and voice review remains.**

No quest text, quest data, item models, or textures were changed when this
revision brief was created.

## Narrative correction

Charles is the author and active speaker of the quest material. His text reaches
the player as direct advice through the voice in their headset. The quest book
is therefore not an impersonal manual describing Charles, nor a transcript that
should routinely place his own speech in quotation marks.

When authorized, audit every quest title, subtitle, description, instruction,
and chapter introduction for the following:

- Rewrite references to Charles in the third person when Charles is actually
  speaking. Use first person where his identity matters and omit self-reference
  where direct instruction is more natural.
- Remove quotation marks that incorrectly frame Charles's own quest prose as a
  quote attributed by a separate narrator.
- Address the player directly in the second person.
- Present instructions as live headset guidance, warnings, observations, and
  mission direction from Charles.
- Preserve quotation marks for genuinely quoted third parties, recovered logs,
  signage, archival records, or deliberate reported speech.
- Preserve all mechanical requirements, item quantities, dependencies,
  objectives, rewards, and progression gates unless a separate change is
  explicitly authorized.
- Keep Charles's voice consistent across tutorial, exploration, industrial,
  dimensional, and endgame chapters rather than changing only the most obvious
  quoted passages.

## Quest-interface recontextualization

The physical quest interface should be presented as the installed Cyberspace
mobile terminal:

- Existing quest-book item: `ftbquests:book`
- Visual reference item: `cyberspace:mobile_terminal`
- Related stationary block, not the requested reference: `cyberspace:terminal`

When authorized:

1. Inspect the shipped models and textures for both items and determine whether
   the Cyberspace asset can be referenced directly or must be copied into an
   Infinite Domain resource namespace.
2. Override the FTB Quests book model/texture so it visually reads as the mobile
   terminal while retaining the original quest-opening behavior.
3. Update the item name and tooltip, if supported without breaking localization,
   to describe Charles's headset-linked mission terminal.
4. Verify the held model, inventory icon, GUI entry points, JEI appearance, and
   multiplayer resource-pack behavior.
5. Avoid changing `cyberspace:mobile_terminal` itself or replacing either item's
   gameplay functionality.

## Required execution order

1. Back up or diff the current quest language files.
2. Produce an audit of every Charles/quotation occurrence before rewriting.
3. Establish a short voice guide from representative approved examples.
4. Rewrite chapter-by-chapter and preserve objective data exactly.
5. Run the full FTB Quests structural and dependency audits.
6. Implement and visually verify the mobile-terminal quest-book override.
7. Present a change summary and a short sample of the revised voice for final
   review.

Execution was authorized after Minecraft was shut down. See
`docs/CHARLES_VOICE_GUIDE.md` for the adopted characterization.
