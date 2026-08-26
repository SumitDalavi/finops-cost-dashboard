"""Tests for cost analyzers."""
import pytest
from app.analyzers.anomaly_detector import detect_anomalies, CostAnomaly
from app.analyzers.recommendations import analyze_ec2_utilization, analyze_idle_resources, total_savings


def make_series(amounts, service="api"):
    return [{"date": f"2024-01-{i+1:02d}", "service": service, "amount": a} for i, a in enumerate(amounts)]


def test_no_anomalies_flat_series():
    series = make_series([100.0] * 14)
    anomalies = detect_anomalies(series, window=7)
    assert len(anomalies) == 0


def test_detects_spike():
    amounts = [100.0] * 10 + [5000.0]  # massive spike on day 11
    series = make_series(amounts)
    anomalies = detect_anomalies(series, window=7)
    assert len(anomalies) >= 1
    assert anomalies[-1].severity in ("HIGH", "CRITICAL")


def test_spike_deviation_pct_positive():
    amounts = [100.0] * 10 + [500.0]
    anomalies = detect_anomalies(make_series(amounts), window=7)
    assert all(a.deviation_pct > 0 for a in anomalies)


def test_ec2_high_priority_rec():
    instances = [{"id": "i-abc", "type": "m5.4xlarge", "avg_cpu_pct": 2.0, "avg_mem_pct": 5.0, "monthly_cost": 400.0}]
    recs = analyze_ec2_utilization(instances)
    assert len(recs) == 1
    assert recs[0].priority == "HIGH"
    assert recs[0].projected_saving > 0


def test_ec2_no_rec_for_healthy_usage():
    instances = [{"id": "i-def", "type": "m5.xlarge", "avg_cpu_pct": 60.0, "avg_mem_pct": 70.0, "monthly_cost": 200.0}]
    recs = analyze_ec2_utilization(instances)
    assert len(recs) == 0


def test_idle_resource_detection():
    resources = [{"id": "lb-1", "type": "ALB", "monthly_cost": 50.0, "requests_7d": 0, "connections_7d": 0}]
    recs = analyze_idle_resources(resources)
    assert len(recs) == 1
    assert recs[0].saving_pct == 100.0


def test_total_savings_calculation():
    from app.analyzers.recommendations import Recommendation
    recs = [
        Recommendation("r1", "EC2", 400, 160, 40, "Downsize", "Low CPU", "HIGH"),
        Recommendation("r2", "ALB", 50, 50, 100, "Delete", "Idle", "HIGH"),
    ]
    assert total_savings(recs) == 210.0
