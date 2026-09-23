# Copyright (c) 2026, libracore AG and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from operator import itemgetter

def execute(filters: dict | None = None):
    """Return columns and data for the report.

    This is the main entry point for the report. It accepts the filters as a
    dictionary and should return columns and data. It is called by the framework
    every time the report is refreshed or a filter is updated.
    """
    columns = get_columns()
    data = get_data()
    chart = get_chart(data)

    return columns, data, None, chart

def execute_snapshot_report(filters: dict | None = None):
    """Return columns and data for the report.

    This is the main entry point for snapshot report. When 'Synced
    Report' is enabled in report, framework will call this method
    every time the report is refreshed or a filter is updated. It
    accepts the same filters as normal execute. But a utility method -
    get_latest_sync, is also imported.

    """
    from frappe.database.duckdb.database import get_latest_sync

    columns = get_columns()
    data = get_data()
    chart = get_chart(data)
    
    return columns, data, None, chart

def get_columns() -> list[dict]:
    """Return columns for the report.

    One field definition per column, just like a DocType field definition.
    """
    return [
        {
            "label": _("Airline"),
            "fieldname": "airline",
            "fieldtype": "Link",
            "options": "Airline",
            "width": "200px"
        },
        {
            "label": _("Revenue"),
            "fieldname": "revenue",
            "fieldtype": "Int",
            "width": "150px"
        },
    ]


def get_data() -> list[list]:
    """Return data for the report.

    The report data is a list of rows, with each row being a list of cell values.
    """
    airlines = frappe.get_all("Airline", fields=['name'])
    
    data = []
    for a in airlines:
        # this would be much easier and perform better as SQL, 
        # but the task asks for an implementation with get_all
        tickets = frappe.get_all("Airplane Ticket",
            filters=[
                ['flight', 'LIKE', f"{a['name']}-%"], 
                ['docstatus', '=', 1]
            ],
            fields=['name', 'total_amount']
        )
        revenue = 0
        for t in tickets:
            revenue += t['total_amount']
            
        data.append({
            'airline': a['name'],
            'revenue': revenue
        })
        
    output = sorted(data, key=itemgetter('revenue'), reverse=True)
    
    return output

def get_chart(data):
    labels = [d['airline'] for d in data]
    values = [d['revenue'] for d in data]

    return {
        "data": {
            "labels": labels,
            "datasets": [{"name": _("Revenue"), "values": values}]
        },
        "type": "donut",
        "height": 300
    }
