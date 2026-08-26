"""
Cost anomaly detector using z-score and rolling average methods.
Detects spend spikes that deviate significantly from recent baseline.
"""
from __future__ import annotations
import math
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CostAnomaly:
    service: str
    date: str
    amount: float
    baseline: float
    z_score: float
    deviation_pct: float
    severity: str    # LOW | MEDIUM | HIGH | CRITICAL


def detect_anomalies(
    cost_series: List[dict],  # [{date, service, amount}, ...]
    window: int = 7,
    z_threshold: float = 2.0,
) -> List[CostAnomaly]:
    """
    Detect cost anomalies using a rolling z-score on a time series.

    Args:
        cost_series: Chronologically ordered list of daily cost records
        window: Rolling window in days for baseline calculation
        z_threshold: z-score threshold above which a point is anomalous
    """
    anomalies = []
    amounts = [r["amount"] for r in cost_series]

    for i in range(window, len(cost_series)):
        window_slice = amounts[i - window : i]
        mean = sum(window_slice) / len(window_slice)
        variance = sum((x - mean) ** 2 for x in window_slice) / len(window_slice)
        std = math.sqrt(variance) if variance > 0 else 0.0001

        current = amounts[i]
        z_score = (current - mean) / std
        deviation_pct = ((current - mean) / mean * 100) if mean > 0 else 0.0

        if abs(z_score) >= z_threshold:
            severity = (
                "CRITICAL" if abs(z_score) >= 5 else
                "HIGH"     if abs(z_score) >= 3.5 else
                "MEDIUM"   if abs(z_score) >= 2.5 else "LOW"
            )
            anomalies.append(CostAnomaly(
                service=cost_series[i].get("service", "unknown"),
                date=cost_series[i].get("date", ""),
                amount=round(current, 2),
                baseline=round(mean, 2),
                z_score=round(z_score, 2),
                deviation_pct=round(deviation_pct, 1),
                severity=severity,
            ))

    return anomalies


def group_by_service(cost_records: List[dict]) -> dict:
    """Group cost records by service name."""
    groups = {}
    for rec in cost_records:
        svc = rec.get("service", "unknown")
        groups.setdefault(svc, []).append(rec)
    return groups
