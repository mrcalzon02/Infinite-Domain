#!/usr/bin/env python3
"""Aggregate later Old World implementation components.

This module contains no generation side effects. The authoritative executable
entrypoint imports SPECS and BUILDERS from here; institution, crisis and final
wave modules remain plain implementation components.
"""
from __future__ import annotations

import old_world_institution_waves as institutions
import old_world_crisis_waves as crisis
import old_world_final_waves as final

SPECS = tuple(institutions.SPECS) + tuple(crisis.SPECS) + tuple(final.SPECS)
BUILDERS = {
    **institutions.BUILDERS,
    **crisis.BUILDERS,
    **final.BUILDERS,
}
CURRENT_WAVE = final.CURRENT_WAVE
