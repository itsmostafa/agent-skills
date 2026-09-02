#!/usr/bin/env python3
"""Deterministic diagram compiler for the /explain skill.

The JSON describes meaning only: nodes, edges, and coarse rank/row hints.
Every pixel is computed here. Failures name a semantic fix, never a coordinate.

    python3 compile.py DRAFT.html --root REPO   # -> index.html beside the draft
    python3 compile.py DIAGRAM.json --root REPO # validate only
    python3 compile.py --selftest
"""

import argparse
import html
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- constants

MARGIN, TITLE_H, PAD_X = 24, 38, 14
BOX_H, SRC_H, MIN_W = 48, 18, 96
RANK_GAP, ROW_GAP, LANE_GAP, LEGEND_H = 72, 28, 26, 26
TITLE_CW = 10            # title char advance, matches .dg-title
NF, NCW = 15, 9          # node label font size, monospace char advance
EF, ECW = 13, 8          # edge label
SF, SCW = 12, 7          # src caption
HEAD_H, MSG_STEP = 44, 40
SELF_W, SELF_H, MIN_LGAP = 44, 34, 48

ALL_TYPES = ("architecture", "workflow", "dataflow", "lifecycle", "sequence")
# Tuple, not a set: iteration order reaches the output via the legend.
KINDS = ("service", "store", "external", "terminal")
MSG_STYLES = ("call", "return", "async")

MAX_NODE_LABEL, MAX_EDGE_LABEL, MAX_MSG_LABEL = 48, 32, 40
COLUMN_W = 960           # the prose column, 60rem, in px -- see body{} in CSS
# A title is a full-width line of its own, so it alone can push a graph past the
# column: (COLUMN_W - 2 * MARGIN) // TITLE_CW. Capped here, where the fix is to
# shorten the title, rather than reported later as a diagram that is too wide.
MAX_TITLE = 91

NODE_SPEC = {
    "id": (str, True), "label": (str, True), "kind": (str, False),
    "rank": (int, False), "row": (int, False), "src": (object, False),
}
EDGE_SPEC = {
    "from": (str, True), "to": (str, True),
    "label": (str, False), "back": (bool, False),
}
GRAPH_SPEC = {
    "type": (str, True), "title": (str, False),
    "nodes": (list, True), "edges": (list, False),
}
PART_SPEC = {
    "id": (str, True), "label": (str, True),
    "kind": (str, False), "src": (object, False),
}
MSG_SPEC = {
    "from": (str, True), "to": (str, True),
    "label": (str, False), "style": (str, False),
}
SEQ_SPEC = {
    "type": (str, True), "title": (str, False),
    "participants": (list, True), "messages": (list, True),
}

CSS = """
:root{
  --dg-bg:#ffffff; --dg-fg:#1c1e21; --dg-muted:#6b7280; --dg-edge:#8b93a1;
  --dg-service:#e8effb; --dg-service-b:#5b86d6;
  --dg-store:#e9f6ee;   --dg-store-b:#4e9e6a;
  --dg-external:#f3eefb; --dg-external-b:#8a6fc4;
  --dg-terminal:#fdf0e6; --dg-terminal-b:#c9803c;
}
@media (prefers-color-scheme: dark){
  :root{
    --dg-bg:#16181c; --dg-fg:#e6e8eb; --dg-muted:#9aa1ac; --dg-edge:#6f7783;
    --dg-service:#1c2c48; --dg-service-b:#6f9ae4;
    --dg-store:#16301f;   --dg-store-b:#5cb27a;
    --dg-external:#2a2140; --dg-external-b:#9d85d4;
    --dg-terminal:#3a2617; --dg-terminal-b:#d8924e;
  }
}
/* The diagrams follow prefers-color-scheme, so the page has to as well —
   otherwise a dark palette lands on a white sheet and the knockouts and title
   turn unreadable. */
html{color-scheme:light dark}
body{background:var(--dg-bg);color:var(--dg-fg);
     margin:0 auto;padding:2rem 1.25rem;max-width:60rem;line-height:1.6;
     font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
/* The frame is the prose column, so a diagram starts and ends where the
   paragraphs do. Graphs fit inside it by rule (E_TOO_WIDE); a sequence, which
   is horizontal by nature, scrolls instead of being scaled down -- shrinking it
   would put its type below the size of the text around it. */
.dg-wrap{overflow-x:auto;margin:1.4rem 0}
.dg{display:block;height:auto;
    font-family:ui-monospace,SFMono-Regular,Menlo,"DejaVu Sans Mono",monospace}
.dg text{fill:var(--dg-fg)}
.dg .dg-title{font-size:17px;font-weight:600}
.dg .dg-src{fill:var(--dg-muted)}
.dg .dg-lifeline{stroke:var(--dg-edge);stroke-width:1;stroke-dasharray:3 4}
.dg .dg-e{fill:none;stroke:var(--dg-edge);stroke-width:1.5}
.dg .dg-e.dashed{stroke-dasharray:5 4}
.dg .dg-ah{fill:var(--dg-edge)}
.dg .dg-elb{fill:var(--dg-bg)}
.dg .dg-n rect{stroke-width:1.5}
.dg .k-service  rect{fill:var(--dg-service); stroke:var(--dg-service-b)}
.dg .k-store    rect{fill:var(--dg-store);   stroke:var(--dg-store-b)}
.dg .k-external rect{fill:var(--dg-external);stroke:var(--dg-external-b)}
.dg .k-terminal rect{fill:var(--dg-terminal);stroke:var(--dg-terminal-b)}
""" + (
    # Font sizes must match the advances the layout measured with, or textLength
    # squeezes default-sized glyphs into a width computed for a smaller font.
    ".dg .dg-nl{font-size:%dpx}\n"
    ".dg .dg-el{font-size:%dpx}\n"
    ".dg .dg-src{font-size:%dpx}\n" % (NF, EF, SF))

# ------------------------------------------------------------------- errors

FINDINGS = []


def err(code, where, msg):
    FINDINGS.append("%s %s: %s" % (code, where, msg))


def report():
    for line in dict.fromkeys(FINDINGS):   # a repeated diagram repeats its findings
        sys.stderr.write(line + "\n")
    return 1 if FINDINGS else 0


# --------------------------------------------------------------- validation

def _no_dupes(pairs):
    seen = {}
    for k, v in pairs:
        if k in seen:
            raise ValueError("duplicate key %r" % k)
        seen[k] = v
    return seen


def load_ir(path):
    """Read one diagram file. Returns None if it could not be parsed."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh, object_pairs_hook=_no_dupes)
    except OSError as exc:
        err("E_IO", os.path.basename(path), str(exc))
        return None
    except ValueError as exc:
        code = "E_JSON_DUPKEY" if "duplicate key" in str(exc) else "E_JSON_PARSE"
        err(code, os.path.basename(path), str(exc))
        return None


def check_obj(obj, spec, where):
    """Table-driven required / type / unknown-key check. True if usable."""
    if not isinstance(obj, dict):
        err("E_FIELD_TYPE", where, "expected an object, got %s" % type(obj).__name__)
        return False
    ok = True
    for key, (typ, required) in spec.items():
        if key not in obj:
            if required:
                err("E_FIELD_MISSING", "%s.%s" % (where, key), "required field")
                ok = False
            continue
        val = obj[key]
        if typ is object:
            continue
        # bool is a subclass of int, so "rank": true would pass isinstance.
        if typ is int and type(val) is not int:
            err("E_FIELD_TYPE", "%s.%s" % (where, key),
                "expected int, got %s" % type(val).__name__)
            ok = False
        elif typ is not int and not isinstance(val, typ):
            err("E_FIELD_TYPE", "%s.%s" % (where, key),
                "expected %s, got %s" % (typ.__name__, type(val).__name__))
            ok = False
    for key in obj:
        if key not in spec:
            err("E_FIELD_UNKNOWN", "%s.%s" % (where, key),
                "not a field. The compiler computes geometry; allowed here: %s"
                % ", ".join(sorted(spec)))
            ok = False
    return ok


def check_label(text, cap, where):
    if not text:
        err("E_LABEL_CHARSET", where, "label must not be empty")
        return
    for ch in text:
        if not (0x20 <= ord(ch) <= 0x7E):
            err("E_LABEL_CHARSET", where,
                "%r is not printable ASCII; width cannot be guaranteed" % ch)
            return
    if text != text.strip() or "  " in text:
        err("E_LABEL_CHARSET", where, "no leading, trailing, or doubled spaces")
        return
    if len(text) > cap:
        err("E_LABEL_LONG", where, "%d chars, max %d" % (len(text), cap))


def src_list(node):
    raw = node.get("src") or []
    return [raw] if isinstance(raw, str) else raw


def src_labels(node):
    """What a box prints: file name and line, not the whole repo path.

    A path like lakewatch/dasl-apiserver/src/export/V1Exporter.scala:57 pins the
    box three times wider than its own label. The directory is still checked,
    and still readable in the node's tooltip -- it just stops setting the width.
    """
    return [os.path.basename(s) for s in src_list(node)]


def check_src(node, root, where):
    raw = node.get("src")
    if raw is None:
        return
    if not isinstance(raw, (str, list)):
        err("E_SRC_FORMAT", where, "expected a string or list of strings")
        return
    for i, entry in enumerate(src_list(node)):
        at = "%s.src[%d]" % (where, i)
        if not isinstance(entry, str) or not entry:
            err("E_SRC_FORMAT", at, "expected a non-empty string")
            continue
        if "\\" in entry or re.match(r"^[A-Za-z]:", entry):
            err("E_SRC_FORMAT", at, "use POSIX-relative paths: %r" % entry)
            continue
        base = Path(root).resolve()
        path, line = entry, None
        head, sep, tail = entry.rpartition(":")
        if sep and tail.isdigit() and not (base / entry).is_file():
            path, line = head, int(tail)
        if not path or path.startswith("/"):
            err("E_SRC_ESCAPE", at, "must be relative to --root: %r" % entry)
            continue
        try:
            target = (base / path).resolve()
            target.relative_to(base)
        except (ValueError, OSError):
            err("E_SRC_ESCAPE", at, "%r resolves outside --root %s" % (path, base))
            continue
        if not target.is_file():
            err("E_SRC_MISSING", at, "no such file under --root: %s" % path)
            continue
        if line is not None:
            if line < 1:
                err("E_SRC_FORMAT", at, "line numbers start at 1")
                continue
            count = 0
            with open(target, "r", encoding="utf-8", errors="replace") as fh:
                for count, _ in enumerate(fh, 1):
                    if count >= line:
                        break
            if count < line:
                err("E_SRC_LINE", at,
                    "%s has fewer than %d lines" % (path, line))


def check_graph(d, root, name):
    start = len(FINDINGS)
    if not check_obj(d, GRAPH_SPEC, name):
        return False
    if d.get("title"):
        check_label(d["title"], MAX_TITLE, "%s.title" % name)
    nodes, edges = d["nodes"], d.get("edges") or []
    if not nodes:
        err("E_EMPTY", "%s.nodes" % name, "a diagram needs at least one node")
        return False

    ids = []
    for i, n in enumerate(nodes):
        at = "%s.nodes[%d]" % (name, i)
        if not check_obj(n, NODE_SPEC, at):
            continue
        if n["id"] in ids:
            err("E_ID_DUP", "%s.id" % at, "duplicate node id %r" % n["id"])
        ids.append(n["id"])
        check_label(n["label"], MAX_NODE_LABEL, "%s.label" % at)
        if n.get("kind", "service") not in KINDS:
            err("E_ENUM", "%s.kind" % at,
                "%r not in %s" % (n.get("kind"), ", ".join(KINDS)))
        check_src(n, root, at)

    known = set(ids)
    seen_edges = []
    for i, e in enumerate(edges):
        at = "%s.edges[%d]" % (name, i)
        if not check_obj(e, EDGE_SPEC, at):
            continue
        for side in ("from", "to"):
            if e[side] not in known:
                err("E_EDGE_REF", "%s.%s" % (at, side), "unknown node id %r" % e[side])
        if e["from"] == e["to"]:
            err("E_EDGE_SELF", at,
                "%r points at itself; graphs have no self-loop shape" % e["from"])
        key = (e["from"], e["to"])
        if key in seen_edges:
            err("E_EDGE_DUP", at, "%s -> %s already declared" % key)
        seen_edges.append(key)
        if e.get("label"):
            check_label(e["label"], MAX_EDGE_LABEL, "%s.label" % at)

    for field in ("rank", "row"):
        have = [n for n in nodes if isinstance(n, dict) and field in n]
        if have and len(have) != len(nodes):
            missing = [n.get("id") for n in nodes
                       if isinstance(n, dict) and field not in n]
            err("E_HINT_PARTIAL", "%s.nodes.%s" % (name, field),
                "%d of %d nodes set it; give every node a %s or none (missing: %s)"
                % (len(have), len(nodes), field, ", ".join(str(m) for m in missing[:4])))
    return len(FINDINGS) == start


def check_sequence(d, root, name):
    start = len(FINDINGS)
    if not check_obj(d, SEQ_SPEC, name):
        return False
    if d.get("title"):
        check_label(d["title"], MAX_TITLE, "%s.title" % name)
    parts, msgs = d["participants"], d["messages"]
    if len(parts) < 2:
        err("E_EMPTY", "%s.participants" % name, "a sequence needs at least two")
        return False
    if not msgs:
        err("E_EMPTY", "%s.messages" % name, "a sequence needs at least one message")
        return False

    ids = []
    for i, p in enumerate(parts):
        at = "%s.participants[%d]" % (name, i)
        if not check_obj(p, PART_SPEC, at):
            continue
        if p["id"] in ids:
            err("E_ID_DUP", "%s.id" % at, "duplicate participant id %r" % p["id"])
        ids.append(p["id"])
        check_label(p["label"], MAX_NODE_LABEL, "%s.label" % at)
        if p.get("kind", "service") not in KINDS:
            err("E_ENUM", "%s.kind" % at,
                "%r not in %s" % (p.get("kind"), ", ".join(KINDS)))
        check_src(p, root, at)

    known = set(ids)
    for i, m in enumerate(msgs):
        at = "%s.messages[%d]" % (name, i)
        if not check_obj(m, MSG_SPEC, at):
            continue
        for side in ("from", "to"):
            if m[side] not in known:
                err("E_EDGE_REF", "%s.%s" % (at, side),
                    "unknown participant id %r" % m[side])
        if m.get("style", "call") not in MSG_STYLES:
            err("E_ENUM", "%s.style" % at,
                "%r not in %s" % (m.get("style"), ", ".join(MSG_STYLES)))
        if m.get("label"):
            check_label(m["label"], MAX_MSG_LABEL, "%s.label" % at)
    return len(FINDINGS) == start


# ------------------------------------------------------------ graph ranking

def classify_and_rank(nodes, edges, name):
    """Rank nodes. Returns (rank, row, lane_edges) or None on failure.

    Back-edges are those flagged `back`, plus any edge that closes a cycle.
    Cycle detection is an iterative DFS in declaration order, so the choice of
    feedback edge is fixed by the input, not by the traversal.
    """
    start = len(FINDINGS)
    index = {n["id"]: i for i, n in enumerate(nodes)}
    fwd = [e for e in edges if not e.get("back")]

    out = {n["id"]: [] for n in nodes}
    for i, e in enumerate(fwd):
        out[e["from"]].append(i)

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n["id"]: WHITE for n in nodes}
    dropped = set()
    for n in nodes:                                   # declaration order
        if color[n["id"]] != WHITE:
            continue
        stack = [(n["id"], 0)]
        color[n["id"]] = GRAY
        while stack:
            node, cursor = stack[-1]
            if cursor < len(out[node]):
                stack[-1] = (node, cursor + 1)
                ei = out[node][cursor]
                if ei in dropped:
                    continue
                nxt = fwd[ei]["to"]
                if color[nxt] == GRAY:
                    dropped.add(ei)
                elif color[nxt] == WHITE:
                    color[nxt] = GRAY
                    stack.append((nxt, 0))
            else:
                color[node] = BLACK
                stack.pop()

    acyclic = [e for i, e in enumerate(fwd) if i not in dropped]

    hinted = all("rank" in n for n in nodes)
    if hinted:
        rank = {n["id"]: n["rank"] for n in nodes}
    else:
        rank = {n["id"]: 0 for n in nodes}
        for _ in range(len(nodes)):
            changed = False
            for e in acyclic:
                want = rank[e["from"]] + 1
                if rank[e["to"]] < want:
                    rank[e["to"]] = want
                    changed = True
            if not changed:
                break
    order = sorted(set(rank.values()))                # dense normalisation
    dense = {old: new for new, old in enumerate(order)}
    rank = {k: dense[v] for k, v in rank.items()}

    if all("row" in n for n in nodes):
        row = {n["id"]: n["row"] for n in nodes}
        taken = {}
        for n in nodes:
            key = (rank[n["id"]], row[n["id"]])
            if key in taken:
                err("E_ROW_DUP", "%s.nodes[%d].row" % (name, index[n["id"]]),
                    "rank %d row %d already taken by node %r"
                    % (key[0], key[1], taken[key]))
            taken[key] = n["id"]
        order = sorted(set(row.values()))
        dense = {old: new for new, old in enumerate(order)}
        row = {k: dense[v] for k, v in row.items()}
    else:
        counter = {}
        row = {}
        for n in nodes:                               # declaration order
            r = rank[n["id"]]
            row[n["id"]] = counter.get(r, 0)
            counter[r] = counter.get(r, 0) + 1

    for i, e in enumerate(edges):
        if rank[e["from"]] == rank[e["to"]]:
            err("E_EDGE_SAMERANK", "%s.edges[%d]" % (name, i),
                "%s and %s are both at rank %d; give one a different rank"
                % (e["from"], e["to"], rank[e["from"]]))
        elif e.get("back") and rank[e["to"]] > rank[e["from"]]:
            err("E_EDGE_BACK_FORWARD", "%s.edges[%d]" % (name, i),
                "marked back but runs forward, rank %d to %d; drop back, or "
                "point the edge the other way"
                % (rank[e["from"]], rank[e["to"]]))
    return (None if len(FINDINGS) > start else (rank, row))


# ------------------------------------------------------------- graph layout

def node_size(n):
    widest_src = max((len(s) * SCW for s in src_labels(n)), default=0)
    w = max(MIN_W, 2 * PAD_X + max(len(n["label"]) * NCW, widest_src))
    return w, BOX_H + SRC_H * len(src_list(n))


def canvas(width, height, title, boxes):
    """Final canvas size. The legend and the title stick out past the boxes."""
    kinds = [k for k in KINDS if any(b["kind"] == k for b in boxes)]
    if len(kinds) > 1:
        legend_y = height
        height += LEGEND_H
        width = max(width, MARGIN + sum(38 + len(k) * SCW for k in kinds) + MARGIN)
    else:
        legend_y, kinds = 0, []
    if title:
        width = max(width, MARGIN + len(title) * TITLE_CW + MARGIN)
    return width, height, kinds, legend_y


def layout_graph(d, name):
    nodes, edges = d["nodes"], d.get("edges") or []
    ranked = classify_and_rank(nodes, edges, name)
    if ranked is None:
        return None
    rank, row = ranked

    size = {n["id"]: node_size(n) for n in nodes}
    nranks = max(rank.values()) + 1
    # Ranks stack down the page and rows spread across it, so the diagram grows
    # in the direction the page already scrolls. Width -- the one axis the prose
    # column pins -- comes from the widest rank, not from the longest chain.
    bandh = [max(size[n["id"]][1] for n in nodes if rank[n["id"]] == r)
             for r in range(nranks)]
    members = [sorted((n for n in nodes if rank[n["id"]] == r),
                      key=lambda n: row[n["id"]]) for r in range(nranks)]
    groupw = [sum(size[n["id"]][0] for n in g) + ROW_GAP * (len(g) - 1)
              for g in members]
    body_w = max(groupw)

    # An edge crosses the corridors between ranks. Which faces it leaves and
    # enters, and which corridors it crosses, follow from the ranks alone.
    plans = []
    for e in edges:
        ra, rb = rank[e["from"]], rank[e["to"]]
        if e.get("back"):            # validated backward, so always T -> B
            kind, fa, fb = "lane", "T", "B"
        elif rb == ra + 1:
            kind, fa, fb = "direct", "B", "T"
        elif rb > ra:
            kind, fa, fb = "lane", "B", "T"
        else:
            kind, fa, fb = "lane", "T", "B"
        if kind == "direct":
            crossed = [ra]
        else:                        # out through one corridor, in through another
            crossed = sorted({ra if rb > ra else ra - 1,
                              rb - 1 if rb > ra else rb})
        plans.append({"e": e, "kind": kind, "fa": fa, "fb": fb, "crossed": crossed})

    # Every crossing gets its own line in the corridor, and the corridor is deep
    # enough to hold them all. Sharing a line would be harmless between bare
    # arrows, but a label's knockout erases whatever else runs along it, and the
    # arrow then reads as if it belonged to that label.
    LINE = EF + 10
    lines, crossing = {}, {}
    for pi, plan in enumerate(plans):
        for r in plan["crossed"]:
            lines[(pi, r)] = crossing.get(r, 0)
            crossing[r] = crossing.get(r, 0) + 1
    gaph = [max(RANK_GAP, crossing.get(r, 0) * LINE + 24) for r in range(nranks - 1)]

    bandy, y = [], MARGIN + TITLE_H
    for r in range(nranks):
        bandy.append(y)
        y += bandh[r] + (gaph[r] if r < len(gaph) else 0)

    # A rank is packed as one block, in row order, and slid under the boxes that
    # feed it, so a child sits below its parent instead of on a global column
    # grid that can pull it to the far side of the page. The block is then
    # clamped into the widest rank's extent, so placing a rank can never widen
    # the canvas -- the widest rank alone sets the width, however deep the graph.
    # ponytail: one anchor per rank, so with several parents a child sits near,
    # not under, its own; per-node placement with overlap resolution if a real
    # diagram reads badly.
    boxes, placed = {}, []
    for r, group in enumerate(members):
        anchors = [boxes[e["from"]]["x"] + boxes[e["from"]]["w"] // 2
                   for e in edges
                   if rank[e["to"]] == r and rank[e["from"]] < r]
        x = (sum(anchors) // len(anchors) - groupw[r] // 2 if anchors
             else MARGIN + (body_w - groupw[r]) // 2)
        x = max(MARGIN, min(x, MARGIN + body_w - groupw[r]))
        for n in group:
            w, h = size[n["id"]]
            box = {"id": n["id"], "x": x, "y": bandy[r] + (bandh[r] - h) // 2,
                   "w": w, "h": h,
                   "label": n["label"], "kind": n.get("kind", "service"),
                   "src": src_labels(n), "src_full": src_list(n)}
            boxes[n["id"]] = box
            placed.append(box)
            x += w + ROW_GAP

    # Empty full-width bands between the rank rows. Routing never leaves them.
    corridor = [bandy[r] + bandh[r] + gaph[r] // 2 for r in range(nranks - 1)]
    body_right = max(b["x"] + b["w"] for b in placed)

    def crossing_y(pi, r):
        return corridor[r] + (2 * lines[(pi, r)] - (crossing[r] - 1)) * LINE // 2

    faces = {n["id"]: {"T": [], "B": []} for n in nodes}
    for pi, plan in enumerate(plans):
        faces[plan["e"]["from"]][plan["fa"]].append(pi)
        faces[plan["e"]["to"]][plan["fb"]].append(pi)

    port = {}
    for nid, sides in faces.items():
        box = boxes[nid]
        for side, members in sides.items():
            # ponytail: a 96px face holds ~96 distinct integer ports, so beyond
            # that two edges share a start pixel. Guidance is 6-12 nodes; widen
            # the box by face degree if a diagram ever really needs more.
            for i, pi in enumerate(members):
                port[(pi, nid, side)] = box["x"] + box["w"] * (i + 1) // (len(members) + 1)

    routed = []
    lane_labels = []
    lane_i = 0
    lane_right = 0
    for pi, plan in enumerate(plans):
        e = plan["e"]
        a, b = boxes[e["from"]], boxes[e["to"]]
        x1 = port[(pi, e["from"], plan["fa"])]
        x2 = port[(pi, e["to"], plan["fb"])]
        ay = a["y"] + a["h"] if plan["fa"] == "B" else a["y"]
        by = b["y"] if plan["fb"] == "T" else b["y"] + b["h"]
        if plan["kind"] == "direct":
            ym = crossing_y(pi, plan["crossed"][0])
            pts = [(x1, ay), (x1, ym), (x2, ym), (x2, by)]
        else:
            # Out past the right edge of the body, where nothing else runs.
            gx = body_right + LANE_GAP * (lane_i + 1)
            c1 = crossing_y(pi, plan["crossed"][0 if plan["fa"] == "B" else -1])
            c2 = crossing_y(pi, plan["crossed"][-1 if plan["fa"] == "B" else 0])
            pts = [(x1, ay), (x1, c1), (gx, c1), (gx, c2), (x2, c2), (x2, by)]
            lane_right = max(lane_right, gx)
            lane_i += 1
        routed.append({"pts": pts, "label": e.get("label", ""), "dashed": False})
        # Label here, not in check_layout, for two reasons: a lane label belongs
        # on the outboard run (index 2) and nowhere near the corridors the
        # direct labels use, and a label right of the body has to be inside the
        # canvas rather than clipped by it.
        if e.get("label"):
            routed[-1]["rect"] = label_rect(
                e["label"], pts, 2 if plan["kind"] == "lane" else None)
            if plan["kind"] == "lane":
                lane_labels.append(routed[-1]["rect"])

    # Lane labels go past the outermost lane, all of them, not each beside its
    # own. Lanes are LANE_GAP apart, so a label centred on one -- or merely
    # started at one -- covers the lanes outboard of it, and the knockout that
    # keeps the label legible then erases those arrows where it lands.
    for rect in lane_labels:
        rect["x"] = lane_right + 6
        rect["cx"] = rect["x"] + rect["w"] // 2

    right = max([body_right, lane_right]
                + [e["rect"]["x"] + e["rect"]["w"] for e in routed if e.get("rect")])

    title = d.get("title", "")
    width, height, kinds, legend_y = canvas(
        right + MARGIN, max(b["y"] + b["h"] for b in placed) + MARGIN,
        title, placed)
    return {"w": width, "h": height, "title": title,
            "nodes": placed, "edges": routed, "kinds": kinds,
            "legend_y": legend_y, "seq": False}


# ---------------------------------------------------------- sequence layout

def layout_sequence(d):
    parts, msgs = d["participants"], d["messages"]
    idx = {p["id"]: i for i, p in enumerate(parts)}
    headw = [max(MIN_W, 2 * PAD_X + max(len(p["label"]) * NCW,
                                        max((len(s) * SCW for s in src_labels(p)),
                                            default=0)))
             for p in parts]

    gaps = [MIN_LGAP] * max(0, len(parts) - 1)
    for m in msgs:
        i, j = idx[m["from"]], idx[m["to"]]
        if i == j:
            continue
        lo, hi = min(i, j), max(i, j)
        span = hi - lo
        need = (len(m.get("label", "")) * ECW + 16 + span - 1) // span
        for g in range(lo, hi):
            gaps[g] = max(gaps[g], need)

    cx, x = [], MARGIN + headw[0] // 2
    for i, _ in enumerate(parts):
        if i:
            x += headw[i - 1] // 2 + gaps[i - 1] + headw[i] // 2
        cx.append(x)

    head_y = MARGIN + TITLE_H
    right = 0
    y = head_y + HEAD_H + MSG_STEP
    routed = []
    for m in msgs:
        i, j = idx[m["from"]], idx[m["to"]]
        style = m.get("style", "call")
        if i == j:
            pts = [(cx[i], y), (cx[i] + SELF_W, y),
                   (cx[i] + SELF_W, y + SELF_H), (cx[i], y + SELF_H)]
            # the label is centred on the loop's right edge, so half of it
            # sticks out past SELF_W and has to be in the canvas width
            right = max(right, cx[i] + SELF_W
                        + (len(m.get("label", "")) * ECW + 8) // 2)
            y += SELF_H + MSG_STEP // 2
        else:
            pts = [(cx[i], y), (cx[j], y)]
            y += MSG_STEP
        routed.append({"pts": pts, "label": m.get("label", ""),
                       "dashed": style != "call"})

    boxes = []
    for i, p in enumerate(parts):
        src = src_labels(p)
        boxes.append({"id": p["id"], "x": cx[i] - headw[i] // 2, "y": head_y,
                      "w": headw[i], "h": HEAD_H + SRC_H * len(src),
                      "label": p["label"], "kind": p.get("kind", "service"),
                      "src": src, "src_full": src_list(p), "lab_h": HEAD_H})
    title = d.get("title", "")
    width, height, kinds, legend_y = canvas(
        max(cx[-1] + headw[-1] // 2 + SELF_W, right) + MARGIN,
        y + MARGIN, title, boxes)
    return {"w": width, "h": height, "title": title,
            "nodes": boxes, "edges": routed, "kinds": kinds,
            "legend_y": legend_y, "seq": True, "lifeline_to": y - MSG_STEP // 2}


# ----------------------------------------------------------------- collision

def label_rect(text, pts, seg=None):
    """Centre the label on the first longest segment, ties to the earlier one.

    Interior segments only when the route bends: the first and last are stubs
    against the node faces, and a label there rides up onto the box. `seg` pins
    the choice, for a route with one run that is deliberately out of the way.
    """
    segments = range(len(pts) - 1)
    if seg is not None:
        segments = [seg]
    elif len(pts) > 2:
        segments = range(1, len(pts) - 2)
    best, best_len = None, -1
    for i in segments:
        (x1, y1), (x2, y2) = pts[i], pts[i + 1]
        span = abs(x2 - x1) + abs(y2 - y1)
        if span > best_len:
            best, best_len = ((x1 + x2) // 2, (y1 + y2) // 2), span
    w = len(text) * ECW + 8
    h = EF + 6
    # A label wider than the run it names would hang off the left of the canvas
    # and be clipped. Slide it back on: it still covers its own arrow, and if it
    # now sits on a box, check_layout says so.
    x = max(0, best[0] - w // 2)
    return {"cx": x + w // 2, "cy": best[1], "x": x,
            "y": best[1] - h // 2, "w": w, "h": h, "text": text}


def overlaps(a, b):
    s = 2                                             # px of touching we forgive
    return not (a["x"] + a["w"] <= b["x"] + s or b["x"] + b["w"] <= a["x"] + s
                or a["y"] + a["h"] <= b["y"] + s or b["y"] + b["h"] <= a["y"] + s)


def check_layout(scene, name):
    labels = []
    for edge in scene["edges"]:
        if edge["label"]:
            edge.setdefault("rect", label_rect(edge["label"], edge["pts"]))
            labels.append(edge["rect"])
    for rect in labels:
        for box in scene["nodes"]:
            if overlaps(rect, box):
                err("E_LABEL_OVER_NODE", name,
                    "edge label %r sits on node %r. Shorten the label, or move "
                    "one of them to a different row."
                    % (rect["text"], box["id"]))
    for i, a in enumerate(labels):
        for b in labels[i + 1:]:
            if overlaps(a, b):
                err("E_LABEL_OVER_LABEL", name,
                    "edge labels %r and %r overlap. Shorten one, or move a node "
                    "to a different row." % (a["text"], b["text"]))


# ---------------------------------------------------------------- svg output

def esc(text):
    return html.escape(text, quote=False)


def svg_text(cls, x, y, text, cw, anchor="middle"):
    return ('<text class="%s" x="%d" y="%d" text-anchor="%s" textLength="%d" '
            'lengthAdjust="spacingAndGlyphs">%s</text>'
            % (cls, x, y, anchor, len(text) * cw, esc(text)))


def render(scene, uid):
    marker = "dg%s-ar" % uid
    out = ['<div class="dg-wrap">'
           '<svg class="dg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" '
           'aria-label="%s" xmlns="http://www.w3.org/2000/svg">'
           % (scene["w"], scene["h"], scene["w"], scene["h"],
              html.escape(scene["title"] or "diagram", quote=True))]
    out.append("<title>%s</title>" % esc(scene["title"] or "diagram"))
    out.append('<defs><marker id="%s" viewBox="0 0 9 8" refX="8" refY="4" '
               'markerWidth="7" markerHeight="6" orient="auto-start-reverse">'
               '<path class="dg-ah" d="M0,0 L9,4 L0,8 z"/></marker></defs>' % marker)
    if scene["title"]:
        out.append(svg_text("dg-title", MARGIN, MARGIN + 18, scene["title"], TITLE_CW, "start"))

    if scene["seq"]:
        out.append('<g class="dg-lifelines">')
        for box in scene["nodes"]:
            cx = box["x"] + box["w"] // 2
            out.append('<line class="dg-lifeline" x1="%d" y1="%d" x2="%d" y2="%d"/>'
                       % (cx, box["y"] + box["h"], cx, scene["lifeline_to"]))
        out.append("</g>")

    out.append('<g class="dg-edges">')
    for edge in scene["edges"]:
        d = "M" + " L".join("%d,%d" % p for p in edge["pts"])
        out.append('<path class="dg-e%s" d="%s" marker-end="url(#%s)"/>'
                   % (" dashed" if edge["dashed"] else "", d, marker))
    out.append("</g>")

    out.append('<g class="dg-nodes">')
    for box in scene["nodes"]:
        rx = box["h"] // 2 if box["kind"] == "terminal" else 6
        out.append('<g class="dg-n k-%s">' % box["kind"])
        if box.get("src_full"):
            out.append("<title>%s</title>" % esc(", ".join(box["src_full"])))
        out.append('<rect x="%d" y="%d" width="%d" height="%d" rx="%d"/>'
                   % (box["x"], box["y"], box["w"], box["h"], rx))
        lab_h = box.get("lab_h", BOX_H)
        base = box["y"] + (lab_h // 2 + 6 if box["src"] else box["h"] // 2 + 6)
        out.append(svg_text("dg-nl", box["x"] + box["w"] // 2, base, box["label"], NCW))
        for i, line in enumerate(box["src"]):
            out.append(svg_text("dg-src", box["x"] + box["w"] // 2,
                                box["y"] + lab_h + 5 + i * SRC_H, line, SCW))
        out.append("</g>")
    out.append("</g>")

    out.append('<g class="dg-elabels">')
    for edge in scene["edges"]:
        rect = edge.get("rect")
        if not rect:
            continue
        out.append('<rect class="dg-elb" x="%d" y="%d" width="%d" height="%d"/>'
                   % (rect["x"], rect["y"], rect["w"], rect["h"]))
        out.append(svg_text("dg-el", rect["cx"], rect["cy"] + 5, rect["text"], ECW))
    out.append("</g>")

    if scene["kinds"]:
        out.append('<g class="dg-legend">')
        x = MARGIN
        for kind in scene["kinds"]:                   # fixed enum order
            out.append('<g class="dg-n k-%s"><rect x="%d" y="%d" width="14" '
                       'height="14" rx="3"/></g>' % (kind, x, scene["legend_y"]))
            out.append(svg_text("dg-src", x + 20, scene["legend_y"] + 11, kind,
                                SCW, "start"))
            x += 20 + len(kind) * SCW + 18
        out.append("</g>")
    out.append("</svg></div>")
    return "\n".join(out)


# --------------------------------------------------------------------- build

def compile_one(path, root, uid):
    start = len(FINDINGS)
    name = os.path.basename(path)
    d = load_ir(path)
    if d is None:
        return None
    if not isinstance(d, dict):
        err("E_FIELD_TYPE", name,
            "a diagram is a JSON object, got %s" % type(d).__name__)
        return None
    kind = d.get("type")
    if kind not in ALL_TYPES:
        err("E_TYPE_UNKNOWN", "%s.type" % name,
            "%r not in %s" % (kind, ", ".join(ALL_TYPES)))
        return None
    if kind == "sequence":
        if not check_sequence(d, root, name):
            return None
        scene = layout_sequence(d)
    else:
        if not check_graph(d, root, name):
            return None
        scene = layout_graph(d, name)
    if scene is None:
        return None
    check_layout(scene, name)
    if not scene["seq"] and scene["w"] > COLUMN_W:
        # Width comes from the widest rank, so this is always reachable: a
        # shorter label or one fewer row. A sequence has no such lever -- its
        # participants are side by side by definition -- so it scrolls instead.
        err("E_TOO_WIDE", name,
            "%d px wide, max %d -- wider than the prose column. Shorten the "
            "longest labels in the widest rank, or split the diagram."
            % (scene["w"], COLUMN_W))
    return None if len(FINDINGS) > start else render(scene, uid)


PLACEHOLDER = re.compile(r"\{\{diagram:\s*([^}\s]+)\s*\}\}")


def build(draft, root):
    base = os.path.dirname(os.path.abspath(draft))
    try:
        with open(draft, "r", encoding="utf-8") as fh:
            page = fh.read()
    except OSError as exc:
        err("E_IO", os.path.basename(draft), str(exc))
        return None

    # Splice per occurrence rather than keying by placeholder text: the same
    # diagram used twice needs two uids, or both copies share one marker id.
    pieces, cut = [], 0
    for uid, match in enumerate(PLACEHOLDER.finditer(page)):
        ref = match.group(1)
        target = os.path.join(base, ref)
        pieces.append(page[cut:match.start()])
        cut = match.end()
        try:
            Path(target).resolve().relative_to(Path(base).resolve())
        except (ValueError, OSError):
            err("E_PLACEHOLDER_ESCAPE", os.path.basename(draft),
                "%r resolves outside the draft directory" % ref)
            continue
        if not os.path.isfile(target):
            err("E_PLACEHOLDER_MISSING", os.path.basename(draft),
                "no diagram %r beside the draft" % ref)
            continue
        pieces.append(compile_one(target, root, uid) or "")
    pieces.append(page[cut:])
    if FINDINGS:
        return None
    page = "".join(pieces)
    style = "<style>%s</style>" % CSS
    page = (page.replace("</head>", style + "\n</head>", 1)
            if "</head>" in page else style + "\n" + page)
    out = os.path.join(base, "index.html")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(page)
    return out


# ------------------------------------------------------------------ selftest

def check_geometry(page):
    """The load-bearing invariant: boxes never overlap, edges never cross one,
    and nothing drawn falls outside the canvas that has to hold it."""
    for i, svg in enumerate(re.findall(r"<svg.*?</svg>", page, re.S)):
        canvas_w = int(re.search(r'viewBox="0 0 (\d+)', svg).group(1))
        for x, w in re.findall(r'<rect class="dg-elb" x="(-?\d+)" y="-?\d+" '
                               r'width="(\d+)"', svg):
            assert 0 <= int(x) and int(x) + int(w) <= canvas_w, \
                "diagram %d: an edge label is clipped by the canvas" % i
        boxes = [tuple(int(v) for v in m) for m in re.findall(
            r'<rect x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)" rx="\d+"/>', svg)]
        boxes = [b for b in boxes if b[2] > 20]          # skip legend swatches
        for a in range(len(boxes)):
            for b in range(a + 1, len(boxes)):
                x1, y1, w1, h1 = boxes[a]
                x2, y2, w2, h2 = boxes[b]
                assert (x1 + w1 <= x2 or x2 + w2 <= x1
                        or y1 + h1 <= y2 or y2 + h2 <= y1), \
                    "diagram %d: nodes %s and %s overlap" % (i, boxes[a], boxes[b])
        for d in re.findall(r'<path class="dg-e[^"]*" d="([^"]+)"', svg):
            pts = [tuple(int(v) for v in p.split(","))
                   for p in d.replace("M", "").split(" L")]
            for p, q in zip(pts, pts[1:]):
                for rx, ry, rw, rh in boxes:
                    rx, ry, rw, rh = rx + 1, ry + 1, rw - 2, rh - 2
                    if (min(p[0], q[0]) < rx + rw and max(p[0], q[0]) > rx
                            and min(p[1], q[1]) < ry + rh and max(p[1], q[1]) > ry):
                        raise AssertionError(
                            "diagram %d: edge %s-%s crosses a node box" % (i, p, q))


def selftest():
    here = Path(__file__).resolve().parent
    examples = here / "examples"
    draft = examples / "demo.draft.html"
    files = sorted(examples.glob("*.json"))
    assert files, "no example diagrams found"

    for path in files:
        del FINDINGS[:]
        first = compile_one(str(path), str(here), 0)
        assert not FINDINGS, "%s: %s" % (path.name, FINDINGS)
        del FINDINGS[:]
        second = compile_one(str(path), str(here), 0)
        assert first == second, "%s is not deterministic" % path.name
        assert first.isascii(), "%s emitted non-ASCII" % path.name
        if json.loads(path.read_text(encoding="utf-8"))["type"] != "sequence":
            wide = int(re.search(r'viewBox="0 0 (\d+)', first).group(1))
            assert wide <= COLUMN_W, ("%s is %dpx, past the prose column"
                                      % (path.name, wide))

    del FINDINGS[:]
    out = build(str(draft), str(here))
    assert out and not FINDINGS, "build failed: %s" % FINDINGS
    with open(out, encoding="utf-8") as fh:
        one = fh.read()
    del FINDINGS[:]
    build(str(draft), str(here))
    with open(out, encoding="utf-8") as fh:
        two = fh.read()
    assert one == two, "build is not deterministic"
    assert "{{diagram" not in one, "unsubstituted placeholder"
    ids = re.findall(r'<marker id="([^"]+)"', one)
    assert len(ids) == len(set(ids)), "duplicate marker ids: %s" % ids
    assert "<script" not in one.lower(), "output must not carry script"
    assert one.count('<div class="dg-wrap">') == len(files), "an svg is unwrapped"
    external = [u for u in re.findall(r"https?://[^\s\"')]+", one)
                if "www.w3.org" not in u]
    assert not external, "output reaches the network: %s" % external
    check_geometry(one)
    print("selftest OK: %d diagrams, %d markers, 2 passes each; every graph "
          "inside the %dpx column, no overlaps, no edge crosses a node"
          % (len(files), len(ids), COLUMN_W))
    return 0


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("paths", nargs="*", help="a draft .html, or diagram .json files")
    ap.add_argument("--root", default=".", help="repo that src paths resolve against")
    ap.add_argument("--selftest", action="store_true")
    ns = ap.parse_args(argv)
    if ns.selftest:
        return selftest()
    if not ns.paths:
        ap.print_usage(sys.stderr)
        return 2
    if all(p.endswith(".json") for p in ns.paths):
        for uid, path in enumerate(ns.paths):
            compile_one(path, ns.root, uid)
        return report()
    if len(ns.paths) != 1 or not ns.paths[0].endswith(".html"):
        sys.stderr.write("give one .html draft, or one or more .json diagrams\n")
        return 2
    out = build(ns.paths[0], ns.root)
    code = report()
    if out and not code:
        print(out)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
