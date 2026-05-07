import time

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

#
# Supported services
#

SERVICES = [
    "PaymentGW",
    "OrderSvc",
    "AuthSvc",
    "NotificationSvc",
    "ReportingSvc",
    "FraudDetector"
]

def detect_service(
    query: str
):

    for service in SERVICES:

        if service.lower() in query.lower():

            return service

    #
    # Default fallback
    #

    return "PaymentGW"

def run_orchestrator(
    query: str
):

    start_time = time.time()

    lower_query = query.lower()

    #
    # Detect target service
    #

    service = detect_service(
        query
    )

    results = {
        "kb_results": [],
        "tool_outputs": []
    }

    trace = {
        "query": query,
        "retrieved_docs": [],
        "tools_called": [],
        "sql_queries": [],
        "latency_ms": 0,
    }

    reasoning_steps = []

    #
    # KB Retrieval
    #

    kb_results = retrieve_from_kb(
        query
    )

    results["kb_results"] = (
        kb_results
    )

    for doc in kb_results:

        trace["retrieved_docs"].append({
            "source": doc["source"],
            "score": doc["score"],
        })

    reasoning_steps.append(
        "Retrieved relevant KB documents"
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

        filtered_incidents = [

            i for i in incidents

            if i["service"] == service
        ]

        results[
            "tool_outputs"
        ].append({

            "tool":
            "incident_history",

            "summary":
            (
                f"Historical incidents "
                f"for {service}"
            ),

            "data":
            filtered_incidents
        })

        trace["tools_called"].append({
            "tool": "incident_history"
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
            "p99",
            "sla"
        ]
    ):

        metrics = (
            get_service_metrics(
                service
            )
        )

        status = (
            get_service_status(
                service
            )
        )

        results[
            "tool_outputs"
        ].append({

            "tool":
            "service_metrics",

            "summary":
            (
                f"Current metrics "
                f"for {service}"
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
                f"Current health "
                f"for {service}"
            ),

            "data":
            status
        })

        trace["tools_called"].append({
            "tool": "service_metrics"
        })

        trace["tools_called"].append({
            "tool": "service_status"
        })

        reasoning_steps.append(
            "Fetched live monitoring metrics"
        )

    #
    # SQL Tool
    #

    if any(
        word in lower_query

        for word in [
            "cost",
            "revenue",
            "expense",
            "q1",
            "q2",
            "q3",
            "q4",
            "spend"
        ]
    ):

        #
        # Detect time filter
        #

        quarter_filter = ""

        if "q1" in lower_query:

            quarter_filter = """
            AND month IN (
                '2026-01',
                '2026-02',
                '2026-03'
            )
            """

        elif "q2" in lower_query:

            quarter_filter = """
            AND month IN (
                '2026-04',
                '2026-05',
                '2026-06'
            )
            """

        elif "march" in lower_query:

            quarter_filter = """
            AND month = '2026-03'
            """

        elif (
            "highest cost" in lower_query
            or "most expensive" in lower_query
            or "cost spike" in lower_query
            or "costs spike" in lower_query
        ):

            quarter_filter = """
            AND month IN (
                '2026-01',
                '2026-02',
                '2026-03'
            )
            """

        #
        # SQL
        #

        sql = f"""
        SELECT
            service,
            month,
            total_cost
        FROM monthly_costs
        WHERE service = '{service}'
        {quarter_filter}
        ORDER BY month ASC
        """

        sql_results = (
            execute_sql(sql)
        )

        trace["tools_called"].append({
            "tool": "database_query"
        })

        trace["sql_queries"].append(sql)

        reasoning_steps.append(
            "Queried structured cost data"
        )

        #
        # Exact grounded total
        #

        total_cost = sum(

            row["total_cost"]

            for row in sql_results
        )

        months_covered = [

            row["month"]

            for row in sql_results
        ]

        results[
            "tool_outputs"
        ].append({

            "tool":
            "database_query",

            "summary":
            (
                f"Infrastructure costs "
                f"for {service}"
            ),

            "important_result":
            (
                f"Total cost for "
                f"{service} "
                f"({', '.join(months_covered)}) "
                f"= ${total_cost:,.0f}"
            ),

            "data":
            sql_results
        })

    trace["latency_ms"] = int(
        (time.time() - start_time) * 1000
    )

    results["trace"] = trace
    results["reasoning_steps"] = reasoning_steps
    return results
