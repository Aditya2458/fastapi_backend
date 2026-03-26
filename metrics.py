from prometheus_client import Counter

login_success_total = Counter(
    "login_success_total",
    "Total successful logins"
)

login_failures_total = Counter(
    "login_failures_total",
    "Total failed login attempts"
)