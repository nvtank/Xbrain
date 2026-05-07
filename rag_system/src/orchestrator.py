from src.bedrock_kb import (
    retrieve_from_kb
)

from src.tools.api_tool import (
    get_incidents,
    get_service_status,
    get_service_metrics
)

from src.tools.db_tool import (
    execute_sql
)

def run_orchestrator(
    query: str
):

    lower_query = query.lower()

    results = {
        "kb_results": [],
        "tool_outputs": []
    }

    #
    # KB Retrieval
    #

    kb_results = retrieve_from_kb(
        query
    )

    results["kb_results"] = (
        kb_results
    )

    #
    # Incident Tool
    #

    if any(
        word in lower_query

        for word in [
            "incident",
            "outage",
            "failure",
            "reliability"
        ]
    ):

        incidents = (
            get_incidents()
        )

        payment_incidents = [

            i for i in incidents

            if i["service"]
            == "PaymentGW"
        ]

        results[
            "tool_outputs"
        ].append({

            "tool": (
                "incident_history"
            ),

            "summary":
            (
                "Historical incidents "
                "for PaymentGW"
            ),

            "data":
            payment_incidents
        })

    #
    # Metrics Tool
    #

    if any(
        word in lower_query

        for word in [
            "latency",
            "health",
            "status",
            "performance",
            "p99"
        ]
    ):

        metrics = (
            get_service_metrics(
                "PaymentGW"
            )
        )

        status = (
            get_service_status(
                "PaymentGW"
            )
        )

        results[
            "tool_outputs"
        ].append({

            "tool":
            "service_metrics",

            "summary":
            (
                "Current performance "
                "metrics"
            ),

            "data":
            metrics
        })

        results[
            "tool_outputs"
        ].append({

            "tool":
            "service_status",

            "summary":
            (
                "Current service "
                "health"
            ),

            "data":
            status
        })

    #
    # SQL Tool
    #

    if any(
        word in lower_query

        for word in [
            "cost",
            "revenue",
            "expense",
            "q1"
        ]
    ):

        sql = """
        SELECT
            SUM(total_cost) AS total
        FROM monthly_costs
        WHERE service = 'PaymentGW'
        AND month IN (
            '2026-01',
            '2026-02',
            '2026-03'
        )
        """

        sql_results = (
            execute_sql(sql)
        )

        total_cost = (
            sql_results[0]["total"]
        )

        results[
            "tool_outputs"
        ].append({

            "tool":
            "database_query",

            "summary":
            (
                "Q1 2026 PaymentGW "
                "infrastructure cost"
            ),

            "important_result":
            (
                f"Q1 infrastructure "
                f"cost = "
                f"${total_cost:,.0f}"
            ),

            "data":
            sql_results
        })

    return results
