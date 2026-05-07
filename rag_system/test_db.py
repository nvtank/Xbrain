from src.tools.db_tool import execute_sql

query = """
SELECT SUM(total_cost) AS total
FROM monthly_costs
WHERE service = 'PaymentGW'
AND month IN (
    '2026-01',
    '2026-02',
    '2026-03'
)
"""

results = execute_sql(query)

print()
print(results)
print()
