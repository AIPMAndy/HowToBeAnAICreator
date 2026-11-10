#!/usr/bin/env python3
"""Synthetic advertising CSV audit. No AI, API access, or ad publishing."""
from __future__ import annotations

import argparse
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

REQUIRED = {"ad_id", "campaign", "headline", "description",
            "impressions", "clicks", "spend"}
FIELDS = ["ad_id", "campaign", "impressions", "clicks", "spend",
          "ctr", "cpc", "status"]


def parse_nonnegative(value: str, field: str) -> Decimal:
    try:
        result = Decimal(value)
    except (InvalidOperation, TypeError):
        raise ValueError(f"{field} must be numeric: {value!r}")
    if not result.is_finite() or result < 0:
        raise ValueError(f"{field} must be finite and nonnegative")
    return result


def audit_row(row: dict[str, str], min_ctr: Decimal = Decimal("0.02")) -> dict[str, str]:
    impressions = parse_nonnegative(row["impressions"], "impressions")
    clicks = parse_nonnegative(row["clicks"], "clicks")
    spend = parse_nonnegative(row["spend"], "spend")
    if impressions != int(impressions) or clicks != int(clicks):
        raise ValueError("impressions and clicks must be integers")
    if clicks > impressions:
        raise ValueError("clicks cannot exceed impressions")
    ctr = clicks / impressions if impressions > 0 else None
    cpc = spend / clicks if clicks > 0 else None
    if ctr is None:
        status = "no_impressions"
    elif ctr < min_ctr:
        status = "review_candidate"
    else:
        status = "not_flagged"
    return {
        "ad_id": row["ad_id"], "campaign": row["campaign"],
        "impressions": str(int(impressions)), "clicks": str(int(clicks)),
        "spend": str(spend),
        "ctr": "" if ctr is None else str(round(ctr, 6).normalize()),
        "cpc": "" if cpc is None else str(round(cpc, 4)),
        "status": status,
    }


def audit_csv(source: Path, destination: Path, min_ctr: Decimal) -> int:
    with source.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
            missing = sorted(REQUIRED - set(reader.fieldnames or []))
            raise ValueError(f"missing columns: {', '.join(missing)}")
        audited = [audit_row(row, min_ctr) for row in reader]
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(audited)
    return len(audited)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--min-ctr", default="0.02", help="Decimal ratio, e.g. 0.02")
    args = parser.parse_args()
    threshold = parse_nonnegative(args.min_ctr, "min_ctr")
    if threshold > 1:
        parser.error("--min-ctr must be <= 1")
    count = audit_csv(args.input, args.output, threshold)
    print(f"Audited {count} synthetic/example ads -> {args.output}")


if __name__ == "__main__":
    main()

