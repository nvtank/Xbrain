import time

from src.bedrock_kb import (
    retrieve_from_kb
)

from src.tools.api_tool import (
    get_incidents,
    get_services,
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

DEPENDENCIES = {
    "AuthSvc": [
        "PaymentGW",
        "OrderSvc"
    ]
}

def detect_service(
    query: str,
    memory_context: str = ""
):

    search_text = f"{query}\n{memory_context}".lower()

    for service in SERVICES:

        if service.lower() in search_text:

            return service

    #
    # Default fallback
    #

    return "PaymentGW"

def run_orchestrator(
    query: str,
    memory_context: str = ""
):

    start_time = time.time()

    lower_query = query.lower()

    #
    # Detect target service
    #

    service = detect_service(
        query,
        memory_context
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
        f"{query}\n{memory_context}"
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

    if (
        "authsvc" in lower_query
        and any(
            phrase in lower_query
            for phrase in [
                "which services",
                "directly affected",
                "depend"
            ]
        )
    ):

        direct = DEPENDENCIES.get(
            "AuthSvc",
            []
        )

        results[
            "tool_outputs"
        ].append({

            "tool":
            "dependency_summary",

            "summary":
            "Direct dependencies on AuthSvc",

            "important_result":
            f"Direct dependencies: {', '.join(direct)}",

            "data":
            {
                "service": "AuthSvc",
                "direct_dependencies": direct,
            },
        })

    def summarize_doc(doc):
        content = (doc.get("content") or "").strip()
        if len(content) > 600:
            content = content[:600].rstrip() + "..."
        return content

    def extract_lines(doc, keywords):
        content = (doc.get("content") or "").splitlines()
        hits = []
        for line in content:
            lower_line = line.lower()
            if any(keyword in lower_line for keyword in keywords):
                cleaned = line.strip("- ").strip()
                if cleaned:
                    hits.append(cleaned)
        return "; ".join(hits)

    def extract_section(doc, marker, length=800):
        content = (doc.get("content") or "")
        lower_content = content.lower()
        idx = lower_content.find(marker.lower())
        if idx == -1:
            return ""
        snippet = content[idx:idx + length].strip()
        return snippet

    for doc in kb_results:

        if doc["source"] in [
            "onboarding_guide.md",
            "capacity_planning_q2_2026.md"
        ]:

            important = summarize_doc(doc)

            if doc["source"] == "onboarding_guide.md":
                extracted = extract_lines(
                    doc,
                    [
                        "vpn",
                        "github",
                        "aws",
                        "console",
                        "pci",
                        "on-call",
                        "on call",
                        "shadow"
                    ]
                )
                if extracted:
                    important = extracted

                    results[
                        "tool_outputs"
                    ].append({

                        "tool":
                        "onboarding_summary",

                        "summary":
                        "Onboarding access and training steps",

                        "important_result":
                        extracted,
                    })

            if doc["source"] == "capacity_planning_q2_2026.md":
                extracted = extract_lines(
                    doc,
                    [
                        "sqs",
                        "consumer",
                        "auto",
                        "scal",
                        "queue"
                    ]
                )
                section = extract_section(
                    doc,
                    "NotificationSvc",
                    length=900
                )
                if extracted:
                    important = extracted
                if section:
                    important = section

                    results[
                        "tool_outputs"
                    ].append({

                        "tool":
                        "capacity_plan_summary",

                        "summary":
                        "Capacity planning proposal for NotificationSvc",

                        "important_result":
                        extracted,
                    })

            results[
                "tool_outputs"
            ].append({

                "tool":
                "kb_highlight",

                "summary":
                f"Key excerpt from {doc['source']}",

                "important_result":
                important,
            })

    #
    # Incident Tool
    #

    if any(
        word in lower_query

        for word in [
            "incident",
            "incidents",
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

        if any(
            phrase in lower_query

            for phrase in [
                "how many incidents",
                "incident count",
                "most incidents",
                "q1"
            ]
        ):

            incident_sql = """
            SELECT
                service,
                COUNT(*) AS incident_count
            FROM incidents
            WHERE date BETWEEN '2026-01-01' AND '2026-03-31'
            GROUP BY service
            ORDER BY incident_count DESC
            """

            incident_rows = execute_sql(
                incident_sql
            )

            trace["tools_called"].append({
                "tool": "incident_counts"
            })

            trace["sql_queries"].append(
                incident_sql
            )

            total_incidents = sum(
                row["incident_count"]
                for row in incident_rows
            )

            top_service = (
                incident_rows[0]["service"]
                if incident_rows
                else "N/A"
            )

            results[
                "tool_outputs"
            ].append({

                "tool":
                "incident_counts",

                "summary":
                "Incident counts for Q1 2026",

                "important_result":
                (
                    f"Total incidents in Q1 2026 = {total_incidents}. "
                    f"Top service = {top_service}."
                ),

                "data":
                incident_rows,
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
            "sla",
            "error rate",
            "error",
            "requests per minute",
            "rpm",
            "cpu",
            "utilization",
            "current",
            "currently",
            "right now",
            "running",
            "healthy",
            "normal",
            "request volume"
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
            metrics,

            "important_result":
            (
                f"p99={metrics.get('latency_ms', {}).get('p99')}ms, "
                f"error_rate={round(metrics.get('error_rate_percent', 0), 4)}%, "
                f"rpm={round(metrics.get('requests_per_minute', 0))}, "
                f"cpu={round(metrics.get('cpu_utilization_percent', 0), 2)}%"
            )
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

        if any(
            phrase in lower_query

            for phrase in [
                "requests per minute",
                "rpm",
                "cpu",
                "utilization",
                "most requests",
                "highest",
                "compare"
            ]
        ):

            all_services = get_services()
            all_metrics = []

            for svc in all_services:
                all_metrics.append(
                    get_service_metrics(svc)
                )

            max_rpm = max(
                all_metrics,
                key=lambda item: item.get("requests_per_minute", 0)
            )

            max_cpu = max(
                all_metrics,
                key=lambda item: item.get("cpu_utilization_percent", 0)
            )

            trace["tools_called"].append({
                "tool": "multi_service_metrics"
            })

            results[
                "tool_outputs"
            ].append({

                "tool":
                "multi_service_metrics",

                "summary":
                "Current metrics across services",

                "data":
                all_metrics,

                "important_result":
                (
                    f"Top RPM: {max_rpm.get('service')} ~"
                    f"{round(max_rpm.get('requests_per_minute', 0), -2)} rpm. "
                    f"Top CPU: {max_cpu.get('service')} ~"
                    f"{round(max_cpu.get('cpu_utilization_percent', 0), 1)}%"
                )
            })

        if any(
            phrase in lower_query

            for phrase in [
                "sla",
                "target",
                "error rate",
                "latency"
            ]
        ):

            sla_sql = f"""
            SELECT metric, target, measurement_window
            FROM sla_targets
            WHERE service = '{service}'
            """

            sla_rows = execute_sql(
                sla_sql
            )

            trace["tools_called"].append({
                "tool": "sla_targets"
            })

            trace["sql_queries"].append(
                sla_sql
            )

            results[
                "tool_outputs"
            ].append({

                "tool":
                "sla_targets",

                "summary":
                f"SLA targets for {service}",

                "data":
                sla_rows,
            })

        if any(
            phrase in lower_query

            for phrase in [
                "daily average",
                "q1 average",
                "q1 2026 daily"
            ]
        ):

            avg_sql = f"""
            SELECT AVG(latency_p99_ms) AS avg_p99
            FROM daily_metrics
            WHERE service = '{service}'
            AND date BETWEEN '2026-01-01' AND '2026-03-31'
            """

            avg_rows = execute_sql(
                avg_sql
            )

            trace["tools_called"].append({
                "tool": "daily_metrics_avg"
            })

            trace["sql_queries"].append(
                avg_sql
            )

            results[
                "tool_outputs"
            ].append({

                "tool":
                "daily_metrics_avg",

                "summary":
                f"Q1 2026 daily average p99 for {service}",

                "data":
                avg_rows,
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
            "spend",
            "total infrastructure"
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

        if any(
            phrase in lower_query

            for phrase in [
                "total infrastructure cost",
                "across all services",
                "all services"
            ]
        ):

            total_sql = """
            SELECT SUM(total_cost) AS total_cost
            FROM monthly_costs
            WHERE month IN (
                '2026-01',
                '2026-02',
                '2026-03'
            )
            """

            total_rows = execute_sql(
                total_sql
            )

            trace["tools_called"].append({
                "tool": "total_infra_cost"
            })

            trace["sql_queries"].append(
                total_sql
            )

            results[
                "tool_outputs"
            ].append({

                "tool":
                "total_infra_cost",

                "summary":
                "Total infrastructure cost across all services (Q1 2026)",

                "important_result":
                (
                    f"Total cost across all services in Q1 2026 = "
                    f"${total_rows[0]['total_cost']:,.0f}"
                ),

                "data":
                total_rows,
            })

        if "march" in lower_query and any(
            phrase in lower_query

            for phrase in [
                "highest total cost",
                "highest cost",
                "most expensive"
            ]
        ):

            highest_sql = """
            SELECT service, total_cost
            FROM monthly_costs
            WHERE month = '2026-03'
            ORDER BY total_cost DESC
            LIMIT 1
            """

            highest_rows = execute_sql(
                highest_sql
            )

            trace["tools_called"].append({
                "tool": "highest_month_cost"
            })

            trace["sql_queries"].append(
                highest_sql
            )

            results[
                "tool_outputs"
            ].append({

                "tool":
                "highest_month_cost",

                "summary":
                "Highest total cost in March 2026",

                "important_result":
                (
                    f"Top service in March 2026 = {highest_rows[0]['service']} "
                    f"(${highest_rows[0]['total_cost']:,.0f})"
                ),

                "data":
                highest_rows,
            })

        if "q4" in lower_query and "q1" in lower_query and "increase" in lower_query:

            q4_sql = f"""
            SELECT SUM(total_cost) AS total_cost
            FROM monthly_costs
            WHERE service = '{service}'
            AND month IN ('2025-10','2025-11','2025-12')
            """

            q1_sql = f"""
            SELECT SUM(total_cost) AS total_cost
            FROM monthly_costs
            WHERE service = '{service}'
            AND month IN ('2026-01','2026-02','2026-03')
            """

            q4_rows = execute_sql(q4_sql)
            q1_rows = execute_sql(q1_sql)

            trace["tools_called"].append({
                "tool": "q4_q1_costs"
            })

            trace["sql_queries"].extend([
                q4_sql,
                q1_sql,
            ])

            q4_total = q4_rows[0]["total_cost"] or 0
            q1_total = q1_rows[0]["total_cost"] or 0
            diff = q1_total - q4_total
            pct = (diff / q4_total * 100) if q4_total else 0

            results[
                "tool_outputs"
            ].append({

                "tool":
                "q4_q1_costs",

                "summary":
                f"Q4 2025 vs Q1 2026 cost delta for {service}",

                "important_result":
                (
                    f"Q4 2025 = ${q4_total:,.0f}, Q1 2026 = ${q1_total:,.0f}, "
                    f"increase = ${diff:,.0f} (~{pct:.0f}%)"
                ),

                "data":
                {
                    "q4_2025": q4_total,
                    "q1_2026": q1_total,
                    "increase": diff,
                    "percent": pct,
                },
            })

    trace["latency_ms"] = int(
        (time.time() - start_time) * 1000
    )

    results["trace"] = trace
    results["reasoning_steps"] = reasoning_steps
    return results
