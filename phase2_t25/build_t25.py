"""GBPJPY t25 canonical master builder + digest. Usage: python3 build_t25.py <frag_dir> <t100_master_csv> <out_dir>"""

import bisect
import gzip
import hashlib
import json
import os
import re
import sys
from array import array
from collections import Counter
from datetime import datetime, timedelta
from functools import lru_cache
from statistics import median, mean

GAP_H = 6.0


@lru_cache(maxsize=None)
def us_dst(d):
    y = d.year
    mar = datetime(y, 3, 1)
    start = mar + timedelta(days=(6 - mar.weekday()) % 7 + 7)
    nov = datetime(y, 11, 1)
    end = nov + timedelta(days=(6 - nov.weekday()) % 7)
    return start <= d < end


def _easter(y):
    a = y % 19
    b, c = y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime(y, month, day)


def _nth_weekday(y, month, weekday, n):
    d = datetime(y, month, 1)
    return d + timedelta(days=(weekday - d.weekday()) % 7 + 7 * (n - 1))


def _last_weekday(y, month, weekday):
    d = (datetime(y, month + 1, 1) - timedelta(days=1)) if month < 12 else datetime(y, 12, 31)
    return d - timedelta(days=(d.weekday() - weekday) % 7)


def _obs(d):
    if d.weekday() == 5:
        return d - timedelta(days=1)
    if d.weekday() == 6:
        return d + timedelta(days=1)
    return d


def _build_holidays():
    h = {}
    for y in range(1998, 2027):
        h[_obs(datetime(y, 1, 1)).strftime("%Y-%m-%d")] = "New Year"
        h[_nth_weekday(y, 1, 0, 3).strftime("%Y-%m-%d")] = "MLK"
        h[_nth_weekday(y, 2, 0, 3).strftime("%Y-%m-%d")] = "Presidents"
        h[(_easter(y) - timedelta(days=2)).strftime("%Y-%m-%d")] = "Good Friday"
        h[_last_weekday(y, 5, 0).strftime("%Y-%m-%d")] = "Memorial"
        if y >= 2021:
            h[_obs(datetime(y, 6, 19)).strftime("%Y-%m-%d")] = "Juneteenth"
        h[_obs(datetime(y, 7, 4)).strftime("%Y-%m-%d")] = "Independence"
        h[_nth_weekday(y, 9, 0, 1).strftime("%Y-%m-%d")] = "Labor"
        h[_nth_weekday(y, 11, 3, 4).strftime("%Y-%m-%d")] = "Thanksgiving"
        h[_obs(datetime(y, 12, 25)).strftime("%Y-%m-%d")] = "Christmas"
    h["2025-01-09"] = "Mourning(Carter)"
    return h


HOLIDAYS = _build_holidays()


def parse_line(ln):
    p = ln.rstrip("\n").split(",")
    if len(p) != 7:
        return None
    try:
        ts = datetime.strptime(p[0] + " " + p[1], "%Y-%m-%d %H:%M:%S")
        o, h, l, c = float(p[2]), float(p[3]), float(p[4]), float(p[5])
        v = int(p[6])
        return ts, o, h, l, c, v
    except ValueError:
        return None


def fmt(ts):
    return ts.strftime("%Y-%m-%d %H:%M:%S")


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def classify_gap(t1, t2):
    gh = (t2 - t1).total_seconds() / 3600.0
    if t1.weekday() in (3, 4, 5) and t2.weekday() in (6, 0) and 40 <= gh <= 80:
        return "weekend"
    names = [HOLIDAYS.get((t1.date() + timedelta(days=k)).isoformat()) for k in range((t2.date() - t1.date()).days + 1)]
    names = [n for n in names if n]
    if names and gh <= 110:
        return "holiday:" + ";".join(sorted(set(names)))
    return "UNEXPLAINED"


def main():
    frag_dir, t100_path, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(out_dir, exist_ok=True)
    frags = sorted(os.path.join(frag_dir, f) for f in os.listdir(frag_dir) if os.path.isfile(os.path.join(frag_dir, f)))
    log = []
    frag_info = []
    for fp in frags:
        log.append("fragment %s bytes=%d md5=%s" % (os.path.basename(fp), os.path.getsize(fp), md5_of(fp)))
        frag_info.append({"name": os.path.basename(fp), "path": fp, "bytes": os.path.getsize(fp), "md5": md5_of(fp)})
    def _first_ts(fi):
        with open(fi["path"]) as f:
            for ln in f:
                r = parse_line(ln)
                if r:
                    return r[0]
        return datetime.max
    frag_info.sort(key=_first_ts)
    log.append("fragment chain order: " + " -> ".join(f["name"] for f in frag_info))

    all_ts = array("q")
    bad_rows = 0
    frag_rows = []
    prev_last = None
    seam_ok = True
    for fi in frag_info:
        n = 0
        first = last = None
        with open(fi["path"]) as f:
            for ln in f:
                if not ln.strip():
                    continue
                r = parse_line(ln)
                if r is None:
                    bad_rows += 1
                    continue
                ts = r[0]
                all_ts.append(int(ts.timestamp()))
                if first is None:
                    first = ts
                last = ts
                n += 1
        frag_rows.append(n)
        fi.update(rows=n, first=fmt(first), last=fmt(last))
        if prev_last is not None and first < prev_last:
            seam_ok = False
            log.append("SEAM OVERLAP: %s starts %s before previous ends %s" % (fi["name"], fmt(first), fmt(prev_last)))
        prev_last = last
    log.append("total parsed rows=%d bad_rows=%d fragments_in_order=%s" % (len(all_ts), bad_rows, seam_ok))

    ts_sorted = sorted(all_ts)
    dup_ts = set()
    i = 0
    while i < len(ts_sorted) - 1:
        if ts_sorted[i] == ts_sorted[i + 1]:
            dup_ts.add(ts_sorted[i])
            while i < len(ts_sorted) - 1 and ts_sorted[i] == ts_sorted[i + 1]:
                i += 1
        i += 1
    log.append("duplicate timestamps: %d rows involved, %d distinct ts" % (sum(1 for t in all_ts if t in dup_ts), len(dup_ts)))

    seen = set()
    dup_conflicts = []
    dup_identical = 0
    dup_dropped = 0
    first_dup_rows = {}
    canon_name = None
    canon_path = None
    n_written = 0
    per_year = Counter()
    per_day = Counter()
    prev_ts = None
    gaps = []
    durations = []
    first_bar = last_bar = None
    ohllc_bad = 0
    for fi in frag_info:
        with open(fi["path"]) as f, open(os.path.join(out_dir, "__tmp_canon.csv"), "a") as out:
            for ln in f:
                if not ln.strip():
                    continue
                r = parse_line(ln)
                if r is None:
                    continue
                ts, o, h, l, c, v = r
                key = int(ts.timestamp())
                if key in dup_ts:
                    if key in first_dup_rows:
                        if (first_dup_rows[key] == (o, h, l, c, v)):
                            dup_identical += 1
                        else:
                            dup_conflicts.append({"ts": fmt(ts), "kept": first_dup_rows[key], "dropped": (o, h, l, c, v), "file": fi["name"]})
                        dup_dropped += 1
                        continue
                    first_dup_rows[key] = (o, h, l, c, v)
                if key in seen:
                    continue
                seen.add(key)
                if prev_ts is not None:
                    dt = (ts - prev_ts).total_seconds()
                    if dt > GAP_H * 3600:
                        gaps.append({"from": fmt(prev_ts), "to": fmt(ts), "hours": round(dt / 3600, 2), "class": classify_gap(prev_ts, ts)})
                    elif dt > 0:
                        durations.append(dt)
                prev_ts = ts
                if first_bar is None:
                    first_bar = ts
                last_bar = ts
                per_year[ts.year] += 1
                per_day[ts.date()] += 1
                if h < max(o, c) - 1e-9 or l > min(o, c) + 1e-9:
                    ohllc_bad += 1
                out.write(ln if ln.endswith("\n") else ln + "\n")
                n_written += 1
    log.append("canonical rows written=%d dup_dropped=%d dup_identical=%d dup_conflicts=%d ohlc_violations=%d" % (
        n_written, dup_dropped, dup_identical, len(dup_conflicts), ohllc_bad))

    y0 = first_bar.strftime("%Y%m%d")
    y1 = last_bar.strftime("%Y%m%d")
    canon_name = "CCMonthCapture GBPJPY t25 %s-%s.csv" % (y0, y1)
    canon_path = os.path.join(out_dir, canon_name)
    os.rename(os.path.join(out_dir, "__tmp_canon.csv"), canon_path)
    canon_md5 = md5_of(canon_path)
    canon_bytes = os.path.getsize(canon_path)
    log.append("canonical %s bytes=%d md5=%s" % (canon_name, canon_bytes, canon_md5))

    active_days = len(per_day)
    bars_per_day = n_written / active_days
    ticks_per_day = {d: c * 25 for d, c in per_day.items()}
    tpd_vals = sorted(ticks_per_day.values())
    dense = [v for v in tpd_vals if v > 1000]
    def pct(a, p):
        return a[min(len(a) - 1, int(len(a) * p))]
    tpd_median = median(dense) if dense else None
    tpd_p10 = pct(dense, 0.10) if dense else None
    tpd_p90 = pct(dense, 0.90) if dense else None
    dur_median = median(durations) if durations else None
    dur_mean = mean(durations) if durations else None

    t100_ts = array("q")
    t100_l = array("d")
    t100_h = array("d")
    t100_first = t100_last = None
    t100_rows = 0
    t100_day = Counter()
    with open(t100_path) as f:
        for ln in f:
            r = parse_line(ln)
            if r is None:
                continue
            ts, o, h, l, c, v = r
            t100_ts.append(int(ts.timestamp()))
            t100_l.append(l)
            t100_h.append(h)
            t100_day[ts.date()] += 1
            if t100_first is None:
                t100_first = ts
            t100_last = ts
            t100_rows += 1
    t100_tpd = sorted(c * 100 for c in t100_day.values())
    t100_dense = [v for v in t100_tpd if v > 1000]
    t100_durs = []
    prev = None
    for k in t100_ts:
        if prev is not None and 0 < k - prev <= GAP_H * 3600:
            t100_durs.append(k - prev)
        prev = k
    t100_dur_median = median(t100_durs) if t100_durs else None

    overlap_rows = 0
    viol = []
    viol_n = 0
    checked = 0
    lo, hi = int(t100_first.timestamp()), int(t100_last.timestamp())
    with open(canon_path) as f:
        for ln in f:
            r = parse_line(ln)
            if r is None:
                continue
            ts, o, h, l, c, v = r
            k = int(ts.timestamp())
            if lo <= k <= hi:
                overlap_rows += 1
                i = bisect.bisect_right(t100_ts, k) - 1
                if i >= 0:
                    checked += 1
                    if not (t100_l[i] - 1e-9 <= c <= t100_h[i] + 1e-9):
                        viol_n += 1
                        if len(viol) < 20:
                            viol.append({"ts": fmt(ts), "t25_C": c, "t100_span": [fmt(datetime.fromtimestamp(t100_ts[i])), fmt(datetime.fromtimestamp(t100_ts[i + 1])) if i + 1 < len(t100_ts) else "END"], "t100_L": t100_l[i], "t100_H": t100_h[i]})
    t0 = int(first_bar.timestamp())
    t1 = int(last_bar.timestamp())
    c0 = int(t100_first.timestamp())
    c1 = int(t100_last.timestamp())
    window_overlap_pct = (min(t1, c1) - max(t0, c0)) / (t1 - t0) * 100
    row_overlap_pct = overlap_rows / n_written * 100

    per_year_t = {}
    for y in sorted(per_year):
        days = sum(1 for d in per_day if d.year == y)
        per_year_t[y] = {"bars": per_year[y], "days": days, "bars_per_day": round(per_year[y] / days, 1) if days else 0,
                         "ticks_per_day": round(per_year[y] / days * 25) if days else 0}
    t100_per_year = {}
    for y in sorted(set(d.year for d in t100_day)):
        days = sum(1 for d in t100_day if d.year == y)
        bars = sum(c for d, c in t100_day.items() if d.year == y)
        t100_per_year[y] = {"bars": bars, "bars_per_day": round(bars / days, 1), "ticks_per_day": round(bars / days * 100)}

    gz_path = canon_path + ".gz"
    with open(canon_path, "rb") as fi, gzip.open(gz_path, "wb", compresslevel=9) as fo:
        for chunk in iter(lambda: fi.read(1 << 22), b""):
            fo.write(chunk)
    gz_md5 = md5_of(gz_path)
    gz_bytes = os.path.getsize(gz_path)

    gap_classes = Counter(g["class"].split(":")[0] for g in gaps)

    result = {
        "canonical": {"name": canon_name, "bytes": canon_bytes, "md5": canon_md5, "rows": n_written,
                      "first_bar": fmt(first_bar), "last_bar": fmt(last_bar)},
        "gz": {"name": canon_name + ".gz", "bytes": gz_bytes, "md5": gz_md5},
        "fragments": frag_info, "fragment_rows": frag_rows, "bad_rows": bad_rows,
        "seam_ok": seam_ok, "dups": {"distinct_ts": len(dup_ts), "rows_involved": sum(1 for t in all_ts if t in dup_ts),
                                      "identical": dup_identical, "dropped": dup_dropped, "conflicts": dup_conflicts},
        "ohlc_violations": ohllc_bad,
        "scale": {"rows": n_written, "t100_rows": t100_rows, "ratio_vs_t100": round(n_written / t100_rows, 3),
                  "expected_ratio": 4.0, "active_days": active_days, "bars_per_day": round(bars_per_day, 1),
                  "ticks_per_day": {"median_dense": tpd_median, "p10_dense": tpd_p10, "p90_dense": tpd_p90},
                  "bar_duration_s": {"median": dur_median, "mean": round(dur_mean, 3)},
                  "t100_ticks_per_day_median_dense": median(t100_dense) if t100_dense else None,
                  "t100_bar_duration_s_median": t100_dur_median,
                  "t25_vs_t100_duration_ratio": round(dur_median / t100_dur_median, 4) if (dur_median and t100_dur_median) else None},
        "per_year_t25": per_year_t, "per_year_t100": t100_per_year,
        "gaps": {"count": len(gaps), "classes": dict(gap_classes), "list": gaps},
        "crosschecks": {"window_overlap_pct": round(window_overlap_pct, 3), "row_overlap_pct": round(row_overlap_pct, 3),
                        "spot_checked": checked, "violations": viol_n, "violation_samples": viol,
                        "t25_vs_t100_ticks_per_day": {y: {"t25": per_year_t[y]["ticks_per_day"], "t100": t100_per_year.get(y, {}).get("ticks_per_day")} for y in per_year_t}},
        "log": log,
    }
    with open(os.path.join(out_dir, "t25_result.json"), "w") as f:
        json.dump(result, f, indent=1, default=str)
    print(json.dumps({k: result[k] for k in ("canonical", "gz", "scale", "dups", "gaps", "crosschecks") if k != "gaps"}, indent=1, default=str)[:3000])
    print("gap classes:", dict(gap_classes), "gaps:", len(gaps))
    print("OK ->", canon_path)


if __name__ == "__main__":
    main()
