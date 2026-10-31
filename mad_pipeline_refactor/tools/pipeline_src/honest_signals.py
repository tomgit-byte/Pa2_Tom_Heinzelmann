"""Section 3.1 of every notebook: honest signals of a multi agent trajectory.

Pentland's four honest signals (Activity, Influence, Mimicry, Consistency) are ported
from face to face conversation to logged multi agent interaction: agents are the actors,
agent turns are their signals and turn order is the time axis (thesis Section 2.6.1 and
Section 4.3.6). All thirteen metrics are deterministic, standard library only and
lexical: echo, repetition and drift measure literal word reuse, not paraphrase.

The turn taking balance pair (``turn_gini``, ``turn_evenness``) of the balance notebook is
included as two further Influence metrics because it reads the same agent turn stream.
"""

from __future__ import annotations

import math
import re
import statistics as pystats
from collections import Counter
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

import numpy as np
import pandas as pd

from .schema import Event, TraceRecord

SIGNAL_OF: Dict[str, str] = {
    "n_agent_turns": "Activity",
    "total_tokens": "Activity",
    "mean_turn_tokens": "Activity",
    "agent_turn_ratio": "Activity",
    "n_actors": "Influence",
    "participation_gini": "Influence",
    "dominant_actor_share": "Influence",
    "hub_share": "Influence",
    "turn_gini": "Influence",
    "turn_evenness": "Influence",
    "cross_echo": "Mimicry",
    "self_repetition": "Mimicry",
    "turn_length_cv": "Consistency",
    "rhythm_regularity": "Consistency",
    "topic_drift": "Consistency",
}

HONEST_SIGNAL_COLUMNS: List[str] = list(SIGNAL_OF)
SIGNAL_ORDER = ["Activity", "Influence", "Mimicry", "Consistency"]

METRIC_LABELS: Dict[str, str] = {
    "n_agent_turns": "agent turns", "total_tokens": "total tokens",
    "mean_turn_tokens": "mean tokens per turn", "agent_turn_ratio": "agent turn ratio",
    "n_actors": "actors", "participation_gini": "participation Gini",
    "dominant_actor_share": "dominant actor share", "hub_share": "hand off hub share",
    "turn_gini": "turn Gini", "turn_evenness": "turn evenness",
    "cross_echo": "cross speaker echo", "self_repetition": "self repetition",
    "turn_length_cv": "turn length CV", "rhythm_regularity": "rhythm regularity",
    "topic_drift": "topic drift",
}

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokens(text: str) -> List[str]:
    """Lower cased alphanumeric tokens."""
    return _TOKEN_RE.findall((text or "").lower())


def bigrams(toks: Sequence[str]) -> Set[Tuple[str, str]]:
    return set(zip(toks, toks[1:]))


def jaccard(a: Set, b: Set) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def gini(values: Iterable[float]) -> float:
    """Gini coefficient of non negative values (0 = equal, towards 1 = concentrated)."""
    xs = sorted(float(v) for v in values)
    n, total = len(xs), sum(xs)
    if n == 0 or total == 0:
        return 0.0
    cum = sum(i * x for i, x in enumerate(xs, start=1))
    return (2 * cum) / (n * total) - (n + 1) / n


def evenness(counts: Sequence[int]) -> float:
    """Pielou evenness ``H / log(k)`` of per actor turn counts."""
    total, k = sum(counts), len(counts)
    if k < 2 or total == 0:
        return 1.0
    h = -sum((c / total) * math.log(c / total) for c in counts if c)
    return h / math.log(k)


def collapse_floor(actors: Sequence[str]) -> List[str]:
    """Turn sequence with consecutive same speaker turns merged into one floor turn."""
    floor: List[str] = []
    for a in actors:
        if not floor or floor[-1] != a:
            floor.append(a)
    return floor


def signals_applicable(record: TraceRecord) -> bool:
    """The applicability gate: at least two agent turns by at least two distinct actors."""
    turns = record.agent_turns()
    return len(turns) >= 2 and len({t.actor for t in turns}) >= 2


def compute_honest_signals(record: TraceRecord) -> Dict[str, Optional[float]]:
    """All honest signal metrics of one trace.

    Returns a flat dict with ``signals_applicable`` and the fifteen metric columns
    (``None`` where the gate fails).
    """
    turns = record.agent_turns()
    n_events = len(record.events)
    out: Dict[str, Optional[float]] = {k: None for k in HONEST_SIGNAL_COLUMNS}
    out["n_agent_turns"] = float(len(turns))
    out["n_actors"] = float(len({t.actor for t in turns}))
    out["signals_applicable"] = signals_applicable(record)
    if not out["signals_applicable"]:
        return out

    actors = [str(t.actor) for t in turns]
    lengths = [t.n_tokens for t in turns]
    toks = [tokens(t.content) for t in turns]
    bgs = [bigrams(tk) for tk in toks]

    # Activity
    total = float(sum(lengths))
    out["total_tokens"] = total
    out["mean_turn_tokens"] = total / len(turns)
    out["agent_turn_ratio"] = len(turns) / n_events if n_events else 0.0

    # Influence
    volume = Counter()
    count = Counter()
    for a, ln in zip(actors, lengths):
        volume[a] += ln
        count[a] += 1
    out["participation_gini"] = gini(volume.values())
    out["dominant_actor_share"] = (max(volume.values()) / total) if total else 0.0
    floor = collapse_floor(actors)
    handoffs = list(zip(floor, floor[1:]))
    received = Counter(b for _, b in handoffs)
    out["hub_share"] = (max(received.values()) / len(handoffs)) if handoffs else 0.0
    out["turn_gini"] = gini(count.values())
    out["turn_evenness"] = evenness(list(count.values()))

    # Mimicry
    cross = [jaccard(bgs[i], bgs[i - 1]) for i in range(1, len(turns))
             if actors[i] != actors[i - 1] and (bgs[i] or bgs[i - 1])]
    out["cross_echo"] = pystats.mean(cross) if cross else 0.0
    last_by_actor: Dict[str, Set] = {}
    selfs = []
    for a, bg in zip(actors, bgs):
        if a in last_by_actor and (bg or last_by_actor[a]):
            selfs.append(jaccard(bg, last_by_actor[a]))
        last_by_actor[a] = bg
    out["self_repetition"] = pystats.mean(selfs) if selfs else 0.0

    # Consistency
    mean_len = pystats.mean(lengths)
    out["turn_length_cv"] = (pystats.pstdev(lengths) / mean_len) if mean_len else 0.0
    if handoffs:
        pair_counts = Counter(handoffs)
        probs = np.array(list(pair_counts.values()), dtype=float) / len(handoffs)
        entropy = float(-(probs * np.log(probs)).sum())
        n_possible = max(2, len(set(floor)) * (len(set(floor)) - 1))
        out["rhythm_regularity"] = 1.0 - entropy / math.log(n_possible)
    else:
        out["rhythm_regularity"] = 1.0
    third = max(1, len(turns) // 3)
    head = set(t for tk in toks[:third] for t in tk)
    tail = set(t for tk in toks[-third:] for t in tk)
    out["topic_drift"] = 1.0 - jaccard(head, tail)
    return out


def compute_honest_signals_table(records: Sequence[TraceRecord]) -> pd.DataFrame:
    """Honest signals for every record, indexed by ``trace_uid``."""
    rows = []
    for r in records:
        row = {"trace_uid": r.trace_uid}
        row.update(compute_honest_signals(r))
        rows.append(row)
    df = pd.DataFrame(rows).set_index("trace_uid", drop=False)
    for col in HONEST_SIGNAL_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def zscore_within(series: pd.Series) -> pd.Series:
    """Z score within a group; constant groups map to zero (no information)."""
    sd = series.std(ddof=0)
    if not sd or np.isnan(sd):
        return series * 0.0
    return (series - series.mean()) / sd


def standardise_within(df: pd.DataFrame, columns: Sequence[str], by: str) -> pd.DataFrame:
    """Z score ``columns`` within the groups of ``by`` (the within format standardisation of
    thesis Section 3.2.5)."""
    out = df.copy()
    for col in columns:
        out[col] = df.groupby(by)[col].transform(zscore_within)
    return out
