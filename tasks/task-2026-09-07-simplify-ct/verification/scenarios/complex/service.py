def get_customer(rows, tenant_id, customer_id):
    return next((r for r in rows if r["tenant_id"] == tenant_id and r["id"] == customer_id), None)
