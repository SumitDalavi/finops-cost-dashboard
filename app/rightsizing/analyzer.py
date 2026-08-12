"""
K8s right-sizing analyzer.
In production, this would query metrics-server or Prometheus for actual utilization.
"""

from ..models import RightsizingRecommendation

def get_recommendations() -> list[RightsizingRecommendation]:
    """Simulates analyzing K8s pod resource utilization."""
    
    return [
        RightsizingRecommendation(
            namespace="production",
            pod_name="api-gateway-7d8f9c6b5-x2k4n",
            container_name="api-gateway",
            current_cpu_request="500m",
            current_memory_request="512Mi",
            avg_cpu_usage="120m",
            avg_memory_usage="198Mi",
            recommended_cpu="200m",
            recommended_memory="256Mi",
            estimated_savings_pct=52.0
        ),
        RightsizingRecommendation(
            namespace="production",
            pod_name="payment-service-5c4d3b2a1-q9r8p",
            container_name="payment-service",
            current_cpu_request="1000m",
            current_memory_request="1Gi",
            avg_cpu_usage="85m",
            avg_memory_usage="256Mi",
            recommended_cpu="200m",
            recommended_memory="384Mi",
            estimated_savings_pct=72.5
        ),
        RightsizingRecommendation(
            namespace="staging",
            pod_name="worker-6e5d4c3b2-m1n0o",
            container_name="worker",
            current_cpu_request="250m",
            current_memory_request="256Mi",
            avg_cpu_usage="230m",
            avg_memory_usage="240Mi",
            recommended_cpu="250m",
            recommended_memory="256Mi",
            estimated_savings_pct=0.0
        ),
    ]
