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

        time_filter = ""

        if "q1" in lower_query:

            time_filter = """
            AND month IN (
                '2026-01',
                '2026-02',
                '2026-03'
            )
            """

        elif "q2" in lower_query:

            time_filter = """
            AND month IN (
                '2026-04',
                '2026-05',
                '2026-06'
            )
            """

        elif (
            "march" in lower_query
            or "tháng 3" in lower_query
        ):

            time_filter = """
            AND month = '2026-03'
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
        {time_filter}
        ORDER BY month ASC
        """

        sql_results = (
            execute_sql(sql)
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
    return results
