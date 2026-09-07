def select_expired(records, cutoff):
    return [r for r in records if r["created_at"] < cutoff]
