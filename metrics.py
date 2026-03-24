from prometheus_client import Counter

# Total marks created
marks_created_total = Counter(
    "marks_created_total",
    "Total number of marks created"
)

# Login failures
login_failures_total = Counter(
    "login_failures_total",
    "Total number of failed login attempts"
)