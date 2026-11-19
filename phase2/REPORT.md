# GBPJPY PHASE II - DATA RECEIPT & DIGEST

Run: phase2_digest.py (python 3.12.14) at 2026-11-19 10:51:46 UTC. Input dir: `/workspace/GBPJPY`. Files found: 6.

## MANIFEST

| file | bytes | md5 | rows | first bar | last bar | tf | claimed | actual | symbol |
|---|---|---|---|---|---|---|---|---|---|
| CCMonthCapture GBPJPY D1 19850618-20261119.csv | 634130 | 3674eedd153c43891c41299b82b48a21 | 11787 | 1985-06-18 21:00:00 | 2026-11-18 22:00:00 | d1 | 1985-2026 | 1985-06-18 21:00:00 .. 2026-11-18 22:00:00 | GBPJPY |
| CCMonthCapture GBPJPY D1 20210101-20261113.csv | 13249 | fcd3f7a0857a9dfa462bb681883eda9d | 226 | 2026-01-01 22:00:00 | 2026-11-12 22:00:00 | d1 | 2021-2026 | 2026-01-01 22:00:00 .. 2026-11-12 22:00:00 | GBPJPY |
| CCMonthCapture GBPJPY h4 20140729-20261113.csv | 1011323 | 50c5a6ca395a8711e3dc91ad8f0dd4fa | 17578 | 2014-07-29 01:00:00 | 2026-11-13 18:00:00 | h4 | 2014-2026 | 2014-07-29 01:00:00 .. 2026-11-13 18:00:00 | GBPJPY |
| CCMonthCapture GBPJPY t1 20190613-20261119.csv | 18775748 | ce372aacd7aa08848ac02ae011959fdc | 472043 | 2019-06-13 09:00:00 | 2026-11-19 08:56:44 | t1 (tick) | 2019-2026 | 2019-06-13 09:00:00 .. 2026-11-19 08:56:44 | GBPJPY |
| CCMonthCapture GBPJPY t100 20210101-20261113.csv | 101023477 | c9abdeb2d46d30edf99214c8a18ff4ce | 1818579 | 2021-01-03 22:12:56 | 2026-11-13 21:56:29 | t100 | 2021-2026 | 2021-01-03 22:12:56 .. 2026-11-13 21:56:29 | GBPJPY |
| CCMonthCapture GBPJPY t750 20210101-20261113.csv | 13469550 | 567641a86d2de06042fcf875c6af6fde | 242477 | 2021-01-03 23:04:27 | 2026-11-13 21:54:05 | t750 | 2021-2026 | 2021-01-03 23:04:27 .. 2026-11-13 21:54:05 | GBPJPY |
| SYNTHETIC t500 from t100 (groups of 5, phase 0) | 0 | synthetic | 363715 | 2021-01-03 22:12:56 | 2026-11-13 21:46:42 | t500 (synth) | synthetic from t100 | 2021-01-03 22:12:56 .. 2026-11-13 21:46:42 | GBPJPY (derived) |

- **d1**: 11787 rows (2 files), 1985-06-18 21:00:00 .. 2026-11-18 22:00:00; overlap 226/226 identical, 0 conflicts.
- **h4**: 17578 rows (1 file), 2014-07-29 01:00:00 .. 2026-11-13 18:00:00; overlap 0/0 identical, 0 conflicts.
- **t100**: 1818579 rows (1 file), 2021-01-03 22:12:56 .. 2026-11-13 21:56:29; overlap 0/0 identical, 0 conflicts.
- **t500**: 363715 rows (1 file), 2021-01-03 22:12:56 .. 2026-11-13 21:46:42; overlap 0/0 identical, 0 conflicts.
- **t750**: 242477 rows (1 file), 2021-01-03 23:04:27 .. 2026-11-13 21:54:05; overlap 0/0 identical, 0 conflicts.
- **UNDER-DELIVERY vs filename**: CCMonthCapture GBPJPY D1 20210101-20261113.csv claims 2021-2026 but actual coverage starts 2026-01-01 (head missing 5+ years).

## FORMAT

- CCMonthCapture GBPJPY D1 19850618-20261119.csv: 7 fields date,time,O,H,L,C,V confirmed
- CCMonthCapture GBPJPY D1 20210101-20261113.csv: 7 fields date,time,O,H,L,C,V confirmed
- CCMonthCapture GBPJPY h4 20140729-20261113.csv: 7 fields date,time,O,H,L,C,V confirmed
- CCMonthCapture GBPJPY t1 20190613-20261119.csv: 4 fields date,time,bid,ask (raw ticks, ms-precision timestamps) - summarized as tick reference, not bar-scanned.
- CCMonthCapture GBPJPY t100 20210101-20261113.csv: 7 fields date,time,O,H,L,C,V confirmed
- CCMonthCapture GBPJPY t750 20210101-20261113.csv: 7 fields date,time,O,H,L,C,V confirmed
- SYNTHETIC t500 from t100 (groups of 5, phase 0): 7 fields date,time,O,H,L,C,V confirmed

## INTEGRITY

- **d1**: wrong-field-count 0; OHLC violations 0; duplicate ts 0; non-monotonic 0; zero-range 68; zero-volume 1267.
- **h4**: wrong-field-count 0; OHLC violations 0; duplicate ts 0; non-monotonic 0; zero-range 1; zero-volume 0.
- **t100**: wrong-field-count 0; OHLC violations 0; duplicate ts 0; non-monotonic 0; zero-range 0; zero-volume 0.
- **t500**: wrong-field-count 0; OHLC violations 0; duplicate ts 0; non-monotonic 0; zero-range 0; zero-volume 0.
- **t750**: wrong-field-count 0; OHLC violations 0; duplicate ts 0; non-monotonic 0; zero-range 0; zero-volume 0.

## GAPS & SEAMS

Timezone evidence (finest timeframe t100): UTC: session-open days (first bar after a >6h gap) start at 21:00-23:59 in 100% of cases; the 21/22 split flips with US DST (EDT/EST), matching the 21:00/22:00 UTC session boundary (histogram in receipt.json).
- d1 (thr 60.0h): weekend 779, holiday 16, UNEXPLAINED 43.
- h4 (thr 10.0h): weekend 588, holiday 11, UNEXPLAINED 1.
- t100 (thr 6.0h): weekend 305, holiday 4, UNEXPLAINED 0.
- t500 (thr 6.0h): weekend 305, holiday 4, UNEXPLAINED 0.
- t750 (thr 6.0h): weekend 305, holiday 4, UNEXPLAINED 0.
  - UNEXPLAINED 1986-04-02 22:00:00 -> 1986-04-05 22:00:00 (72.0h)
  - UNEXPLAINED 1986-04-09 22:00:00 -> 1986-04-12 22:00:00 (72.0h)
  - UNEXPLAINED 1986-04-16 22:00:00 -> 1986-04-19 22:00:00 (72.0h)
  - UNEXPLAINED 1986-04-23 22:00:00 -> 1986-04-26 22:00:00 (72.0h)
  - UNEXPLAINED 1986-04-30 21:00:00 -> 1986-05-03 21:00:00 (72.0h)
  - UNEXPLAINED 1987-04-01 22:00:00 -> 1987-04-04 22:00:00 (72.0h)
  - UNEXPLAINED 1987-04-08 21:00:00 -> 1987-04-11 21:00:00 (72.0h)
  - UNEXPLAINED 1988-03-30 22:00:00 -> 1988-04-02 22:00:00 (72.0h)
  - UNEXPLAINED 1988-04-06 21:00:00 -> 1988-04-09 21:00:00 (72.0h)
  - UNEXPLAINED 1989-03-29 22:00:00 -> 1989-04-01 22:00:00 (72.0h)
  - ... 34 more unexplained gaps in receipt.json
- holiday gaps by name: New Year's Day x19; Christmas x17; Good Friday x3
- hole map **d1**: 2424 zero-bar days (incl. 2099 Fridays - this timeframe has no Friday bars in part of its range): 1985-06-21, 1985-06-28 ... (full map in receipt.json)
- hole map **h4**: 308 zero-bar days (incl. 48 Fridays - this timeframe has no Friday bars in part of its range): 2017-01-01, 2017-12-24 ... (full map in receipt.json)
- hole map **t100**: 3 zero-bar days: 2022-12-25, 2023-12-24 ... (full map in receipt.json)
- hole map **t500**: 3 zero-bar days: 2022-12-25, 2023-12-24 ... (full map in receipt.json)
- hole map **t750**: 3 zero-bar days: 2022-12-25, 2023-12-24 ... (full map in receipt.json)
- weekend seams: 1501 total across timeframes, mean |drift| 0.07%, worst 5:
  - [h4] 2016-06-24 17:00:00 -> 2016-06-26 21:00:00 close 139.533 reopen 136.315 drift -3.218 (-2.31%)
  - [h4] 2017-01-13 18:00:00 -> 2017-01-15 22:00:00 close 139.553 reopen 137.137 drift -2.416 (-1.73%)
  - [h4] 2016-06-17 17:00:00 -> 2016-06-19 21:00:00 close 149.437 reopen 151.523 drift +2.086 (1.40%)
  - [h4] 2017-04-21 17:00:00 -> 2017-04-23 21:00:00 close 139.758 reopen 141.665 drift +1.907 (1.36%)
  - [h4] 2025-04-04 17:00:00 -> 2025-04-06 21:00:00 close 189.327 reopen 186.785 drift -2.542 (-1.34%)

## BAD TICKS

- **d1**: 785 flagged bars (wick x588; delta_close x462; C x4; H x2). Full rows in anomalies.csv.
- **h4**: 52 flagged bars (delta_close x43; wick x22; H x2). Full rows in anomalies.csv.
- **t100**: 3 flagged bars (H x3). Full rows in anomalies.csv.
  - CCMonthCapture GBPJPY t100 20210101-20261113.csv 2021-02-19 21:54:46 O=147.640 H=147.711 L=147.584 C=147.710 V=100 [H == next-session reopen 147.711]
  - CCMonthCapture GBPJPY t100 20210101-20261113.csv 2021-04-09 20:55:04 O=150.267 H=150.378 L=149.591 C=150.242 V=100 [H == next-session reopen 150.378]
- **t500**: 4 flagged bars (delta_close x3; H x1; wick x1). Full rows in anomalies.csv.
- **t750**: 2 flagged bars (delta_close x2; wick x1). Full rows in anomalies.csv.

## CROSS-VALIDATION

- same-timeframe overlaps: d1 226/226 identical
- t500 vs groups-of-5 t100, phase 0: 363715/363715 exact OHLCV matches (2021-01-03 22:12:56 .. 2026-11-13 21:46:42)
- t500 bars reproducible from t100 overall: 363715/363715 (100.00%); remainder = t500 tail beyond t100 end + phase-boundary groups
- t100 vs groups-of-100 t1 ticks: 0 exact matches across all phases (mid+bid) - only sparse-tick false alignments; inconclusive, tick file not dense over t100 range
- t750 vs groups-of-750 t1 ticks: 0 exact matches across all phases (mid+bid) - only sparse-tick false alignments; inconclusive, tick file not dense over t750 range
- no overlap between dense tick days (2026-11-16, 2026-11-17, 2026-11-18, 2026-11-19) and t100 coverage (t100 ends 2026-11-13) - implied-vs-measured tick-rate check inconclusive; dense-day tick rate stands alone.
- daily H/L t100 vs d1, printed-day: 1522 days, H match 62 (4.1%), L match 92 (6.0%)
- daily H/L t100 vs d1, session-day: 1523 days, H match 1438 (94.4%), L match 1133 (74.4%)
- daily H/L t100 vs h4, printed-day: 1520 days, H match 211, L match 197
- daily H/L t100 vs h4, session-day: 1266 days, H match 192, L match 136
- daily H/L h4 vs d1, session-day: 2676 days, H match 1784 (66.7%), L match 1691 (63.2%) - h4 grid is offset from the d1 day stamp, both readings reported

## CALIBRATION DIGEST

(per-year tables shown for 2021+; full history incl. pre-2021 in receipt.json. Cost tiers for GBPJPY: base 0.0050, stress 0.0070 per unit = 0.500/0.700 pips, as % of avg bar range.)

### tick reference (CCMonthCapture GBPJPY t1 20190613-20261119.csv)
- 472043 raw ticks, 2019-06-13 09:00:00 .. 2026-11-19 08:56:44, 2012 days covered; ticks/year (full in receipt.json): 2024:6240; 2025:6216; 2026:437495
- dense days (>1000 ticks): 2026-11-16, 2026-11-17, 2026-11-18, 2026-11-19
- measured ticks/day on dense days: median 121523, max 183966 (tick-rate reference); measured spread (ask-bid): min 0.000 p50 0.600 p90 0.800 p99 16.500 max 30.000 pips; mid price 123.998..219.608

### d1 (reference bars/day ~n/a; ref ticks/day ~121523)

- d1: cross-validation/synthetic frame; per-year table and 2021+ stats in receipt.json.

### h4 (reference bars/day ~n/a; ref ticks/day ~121523)

- h4: cross-validation/synthetic frame; per-year table and 2021+ stats in receipt.json.

### t100 (reference bars/day ~n/a; ref ticks/day ~121523)

| year | bars | days | bars/day | ticks/day | min/bar | avg rng | med rng | avg rng % | base % | stress % |
|---|---|---|---|---|---|---|---|---|---|---|
| 2021 | 197136 | 312 | 631.8 | 63185.0 | 1.4 | 0.035 | 0.032 | 0.02 | 14.18 | 19.85 |
| 2022 | 354010 | 311 | 1138.3 | 113830.0 | 0.83 | 0.046 | 0.039 | 0.03 | 10.92 | 15.28 |
| 2023 | 273882 | 311 | 880.6 | 88065.0 | 1.07 | 0.043 | 0.038 | 0.03 | 11.54 | 16.16 |
| 2024 | 366422 | 314 | 1166.9 | 116695.0 | 0.85 | 0.041 | 0.035 | 0.02 | 12.06 | 16.89 |
| 2025 | 328562 | 312 | 1053.1 | 105308.0 | 0.97 | 0.043 | 0.037 | 0.02 | 11.58 | 16.21 |
| 2026 | 298567 | 272 | 1097.7 | 109767.0 | 0.92 | 0.033 | 0.028 | 0.02 | 14.94 | 20.91 |

- implied ticks/day 2026 (t100 bars/day x 100): 109767 vs measured dense-day tick rate 121523/day.
- hourly bar density (00-24, printed hours): 00:75828 01:77967 02:63105 03:55081 04:51308 05:59054 06:79215 07:98869 08:100034 09:88768 10:81580 11:83043 12:102581 13:118918 14:125448 15:112257 16:89243 17:75872 18:71934 19:65555 20:46912 21:23915 22:30605 23:41487
- dead hours: none; top hours: 14,13,15,12,08,07
- Feb-Mar 2026: peak H 215.008 @ 2026-02-04 12:01:09; max close 214.995 @ 2026-02-04 12:00:12; max bar range 1.390 @ 2026-02-27 21:56:30; max |dC| 0.66% @ 2026-02-27 21:56:30; March trough close 209.322; drawdown from max close 2.64%.
### t500 (reference bars/day ~n/a; ref ticks/day ~121523)

- SYNTHETIC timeframe (derived from t100); per-year table omitted as redundant with t100 - see receipt.json.
- t500: cross-validation/synthetic frame; per-year table and 2021+ stats in receipt.json.

### t750 (reference bars/day ~n/a; ref ticks/day ~121523)

- t750: cross-validation/synthetic frame; per-year table and 2021+ stats in receipt.json.


## PHASE II READINESS

- t500 2021-01-03..2026-11-13: MA layer READY (363715 bars) (SYNTHETIC from t100, groups of 5 phase 0; native export preferred for chart parity).
- t100 2021-01-03..2026-11-13: entry layer READY (1818579 bars); faithful-transpose cells (entry t100 + MA t500, wall-time separation as the transposition key) runnable offline.
- not present in this run: t300. t300 would be derivable from t100 (groups of 3, phase calibrated by sweep) if t100 present; t750 from t1 ticks (groups of 750) where tick coverage exists; neither is derivable from a coarser bar file alone.
- present extra timeframes enabling cross-validation: t750, h4, d1. NOT present in this run: t300.
- No strategy backtest in this run - receipt and digest only; the strategy grid is a separate, later prompt.

## METHOD

- Tool: `phase2_digest.py` (python 3.12.14, stdlib only): `python3 phase2_digest.py <input_dir> [--instrument I --spread-base B --spread-stress S --pip P --synth-t500] [--out DIR]`; artifacts written next to the data; raw files read-only (in-memory copies).
- Parse: CSV, delimiter/header auto-detected; dates YYYY.MM.DD/YYYY-MM-DD/YYYY/MM/DD/YYYYMMDD; times HH:MM[:SS[.fff]]; bar files = 7 fields date,time,O,H,L,C,V (time,date auto-swapped); tick files = 4 fields date,time,bid,ask (ms timestamps) summarized as tick reference only. Bar timestamps are OPEN times, printed as-is; close-time = next bar open; last bar of each file open-ended.
- Symbol gate per file: median price outside the GBPJPY range (100-300) => SUSPECT wrong symbol, excluded from merge, both readings reported. XAUUSD ref 2021->2026 ~1798->~4500s; GBPJPY ref ~124-220.
- Merge per timeframe: dedupe by timestamp across files; overlaps compared bit-for-bit on printed OHLCV; conflicts reported with both readings (first file kept for stats, count disclosed). Integrity: field count != 7; H < max(O,C) or L > min(O,C); duplicate/non-monotonic timestamps; zero-range; zero-volume.
- Gap threshold per timeframe = max(6h, 2.5x median inter-bar gap). Class: weekend = Thu/Fri/Sat -> Sun/Mon 40-80h (intraday DST-adjusted 48-50h: 49h + Sun-Fri UTC offset, 4h EDT / 5h EST); holiday = span covers a computed US federal holiday 1998-2026 (Good Friday via computus, observance shifts, + 2025-01-09); else UNEXPLAINED (each listed). Hole map: zero-bar dates in [first,last] excl. Saturdays + listed holidays.
- Bad ticks (instrument-scaled, % of price): |dClose| > 1.5% of prev close (across_gap if gap > threshold), wick (H-L) > 2.5% of close, H or C == next session's reopen open (3dp) after such a gap (feed-contamination class). All flagged -> anomalies.csv; nothing deleted or fixed.
- Cross-validation: same-timeframe overlap equality; t500 = groups of 5 consecutive t100 (all 5 phases swept from file start, exact OHLCV + span); t300 = groups of 3; t100/t750 vs groups of 100/750 t1 ticks (mid and bid); daily H/L of finest frame vs h4/d1 under BOTH day definitions: printed date and DST-aware session day (open 22:00 UTC EDT / 23:00 UTC EST); --synth-t500 builds t500 from t100 groups of 5 phase 0, marked SYNTHETIC (on XAUUSD native t500 matched phase 3, 375380/375380 exact, so synthetic phase-0 grid is not bit-identical to the native chart).
- Digest: per-year bars/day, implied ticks/day = bars/day x tick size, median min/bar, avg/median range and % of close; cost ratio = spread / avg range (base 0.005, stress 0.007 per unit = 0.5/0.7 pips); hourly density on printed hours; Feb-Mar 2026 blowoff/crash metrics; weekend seam drift = reopen - prior close. Timezone: session-open first-bar hour histogram of finest timeframe vs the 21:00/22:00 UTC boundary (DST-shifting).
- Budget: REPORT.md hard-capped at 15 KB (long lists truncated here; full detail in receipt.json / anomalies.csv). Prices 3dp, percentages 2dp, timestamps full date+time as printed.
