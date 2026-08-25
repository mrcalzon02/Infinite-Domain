"""Lint gate for Lyran Research — in memory and after a real disk round trip."""
import json
import sys
import time
from collections import Counter

sys.path.insert(0, ".")
import structure_geometry_lint as L
import lyran_research as LR


def report(tag, size, positions):
    t0 = time.time()
    res = L.lint_structure("lyran_research", size, positions)
    print(f"[{tag}] linted in {time.time() - t0:.1f}s  positions={len(positions)}")
    print(f"[{tag}] hard_fail_count={res.hard_fail_count} passed={res.passed} findings={len(res.findings)}")
    c = Counter((f.check, f.severity) for f in res.findings)
    for k, v in sorted(c.items()):
        print(f"   {k[0]:<28} {k[1]:<12} {v}")
    for f in res.findings[:30]:
        print(f"   {f.severity}\t{f.check}\t{f.position}\t{f.detail[:150]}")
    return res


t0 = time.time()
t, rep = LR.build()
print(f"built in {time.time() - t0:.1f}s", json.dumps(rep))
size, positions = L.positions_from_template(t)
res_mem = report("memory", size, positions)
json.dump(res_mem.to_dict(), open("/tmp/lyranrepo/lint_report_memory.json", "w"), indent=1)

from convert_nbt_to_lostcities import load_structure  # noqa: E402
dsize, dblocks = load_structure(LR.OUT_NBT)
dpos = L.positions_from_load_structure(dsize, dblocks)
res_disk = report("disk", dsize, dpos)
json.dump(res_disk.to_dict(), open("/tmp/lyranrepo/lint_report_disk.json", "w"), indent=1)
