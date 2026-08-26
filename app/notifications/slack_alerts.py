"""Slack cost alert notifications."""
from __future__ import annotations
import os
from typing import List
from app.analyzers.anomaly_detector import CostAnomaly

try:
    import httpx
    _OK = True
except ImportError:
    _OK = False

SLACK_WEBHOOK = os.getenv("SLACK_COST_WEBHOOK", "")


def send_anomaly_alerts(anomalies: List[CostAnomaly], threshold: str = "HIGH") -> bool:
    """Send Slack alerts for anomalies at or above the given severity threshold."""
    severity_order = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
    min_sev = severity_order.get(threshold, 2)
    to_alert = [a for a in anomalies if severity_order.get(a.severity, 0) >= min_sev]

    if not to_alert or not SLACK_WEBHOOK or not _OK:
        return False

    fields = []
    for a in to_alert[:10]:
        fields.append({
            "type": "mrkdwn",
            "text": f"*{a.service}* ({a.date}): ${a.amount:,.2f} (+{a.deviation_pct:.0f}% vs baseline ${a.baseline:,.2f}) [{a.severity}]"
        })

    payload = {
        "blocks": [
            {"type": "header", "text": {"type": "plain_text", "text": ":money_with_wings: FinOps Cost Anomaly Alert"}},
            {"type": "section", "text": {"type": "mrkdwn",
                "text": f"*{len(to_alert)} anomaly(ies) detected* above threshold: {threshold}"}},
            {"type": "divider"},
            {"type": "section", "fields": fields},
        ]
    }
    try:
        r = httpx.post(SLACK_WEBHOOK, json=payload, timeout=8)
        return r.status_code == 200
    except Exception:
        return False
