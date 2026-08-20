#!/usr/bin/env python3
"""Aggregate later Old World implementation components.

This module contains no generation side effects. The authoritative executable
entrypoint imports SPECS and BUILDERS from here; institution and crisis modules
remain plain implementation components.
"""
from __future__ import annotations

import old_world_institution_waves as institutions
import old_world_crisis_waves as crisis

SPECS = tuple(institutions.SPECS) + tuple(crisis.SPECS)
BUILDERS = {
    **institutions.BUILDERS,
    **crisis.BUILDERS,
}
CURRENT_WAVE = crisis.CURRENT_WAVE
