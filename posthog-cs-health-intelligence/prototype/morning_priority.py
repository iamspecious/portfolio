import json
from datetime import date

THRESHOLDS = {
    "self_serve": {
        "contact_watch":         45,
        "contact_urgent":        60,
        "usage_decline_watch":    2,
        "usage_decline_urgent":   4,
    },
    "sales_assisted": {
        "contact_watch":         21,
        "contact_urgent":        30,
        "usage_decline_watch":    1,
        "usage_decline_urgent":   3,
    },
}

RENEWAL_WATCH  = 60
RENEWAL_URGENT = 30
TICKET_WATCH   = 5
TICKET_URGENT  = 10


def evaluate_account(account):
    ctype = account["customer_type"]
    t = THRESHOLDS[ctype]
    type_label = ctype.replace("_", "-")
    signals = []

    # Failed payment — always URGENT regardless of type; gets a ranking boost in priority_score
    if account["billing_status"] == "failed":
        signals.append({
            "level": "URGENT",
            "signal": "Failed payment",
            "reason": "Billing has lapsed. Every day without resolution raises churn risk and makes the conversation harder.",
            "action": "Call or Slack the account contact today. Resolve payment before opening the renewal conversation.",
        })

    # Days to renewal — same threshold for both customer types
    days_renewal = account["days_to_renewal"]
    if days_renewal <= RENEWAL_URGENT:
        signals.append({
            "level": "URGENT",
            "signal": f"Renewal in {days_renewal} days",
            "reason": "The renewal window is closing. If this conversation hasn't started, start it today.",
            "action": "Send a renewal summary this week. Confirm satisfaction, address open concerns, and agree next steps.",
        })
    elif days_renewal <= RENEWAL_WATCH:
        signals.append({
            "level": "WATCH",
            "signal": f"Renewal in {days_renewal} days",
            "reason": "Renewal is approaching. Now is the right time to open the conversation, not closer to the date.",
            "action": "Schedule a renewal check-in. Ask how they're tracking against their original goals.",
        })

    # Days since last contact — thresholds differ by customer type
    days_contact = account["days_since_last_contact"]
    if days_contact >= t["contact_urgent"]:
        signals.append({
            "level": "URGENT",
            "signal": f"{days_contact} days since last contact",
            "reason": f"For a {type_label} customer, silence at {days_contact} days is a late-stage warning sign.",
            "action": "Reach out today. Keep it short — check in on their current work, not on the account.",
        })
    elif days_contact >= t["contact_watch"]:
        signals.append({
            "level": "WATCH",
            "signal": f"{days_contact} days since last contact",
            "reason": f"Approaching the silence threshold for {type_label} accounts. Worth a brief check-in before it becomes a flag.",
            "action": "Send a low-pressure message this week. Reference something specific — a recent product update or their setup.",
        })

    # Usage trend — self-serve accounts get more tolerance before a flag
    weeks_declining = account["usage_weeks_declining"]
    if account["usage_trend"] == "declining" and weeks_declining > 0:
        if weeks_declining >= t["usage_decline_urgent"]:
            signals.append({
                "level": "URGENT",
                "signal": f"Usage declining for {weeks_declining} weeks",
                "reason": "Extended usage decline is the most reliable early churn signal in a PLG product.",
                "action": "Reach out to understand what changed. Ask about their workflow, not about the drop in usage.",
            })
        elif weeks_declining >= t["usage_decline_watch"]:
            signals.append({
                "level": "WATCH",
                "signal": f"Usage declining for {weeks_declining} weeks",
                "reason": "Usage has started dipping. Could be seasonal; could be structural. Worth watching.",
                "action": "Flag for review. If it continues another week, reach out proactively.",
            })

    # Support ticket age — same threshold for both customer types
    if account["has_open_support_ticket"]:
        ticket_age = account["support_ticket_age_days"]
        if ticket_age >= TICKET_URGENT:
            signals.append({
                "level": "URGENT",
                "signal": f"Support ticket open {ticket_age} days",
                "reason": "A ticket this old is no longer just a technical issue — it's a relationship signal.",
                "action": "Escalate internally today. Message the customer directly to acknowledge the delay.",
            })
        elif ticket_age >= TICKET_WATCH:
            signals.append({
                "level": "WATCH",
                "signal": f"Support ticket open {ticket_age} days",
                "reason": "Ticket is aging. Customers notice when issues go quiet.",
                "action": "Check ticket status. If it's stuck, escalate to support engineering.",
            })

    return signals


def priority_score(account, signals):
    urgent_count = sum(1 for s in signals if s["level"] == "URGENT")
    watch_count  = sum(1 for s in signals if s["level"] == "WATCH")
    # Failed billing floats to the top within the urgent tier — it's a contractual problem that compounds daily
    billing_boost = 5 if account["billing_status"] == "failed" else 0
    return (urgent_count + billing_boost) * 10 + watch_count, account["arr"]


def format_account(account, signals):
    type_label = account["customer_type"].replace("_", "-")
    header = f"  {account['name']}  ({account['arr_tier']}, {type_label})"
    lines = [header]
    # URGENT signals first so the most critical context appears at the top
    for sig in sorted(signals, key=lambda s: 0 if s["level"] == "URGENT" else 1):
        lines.append(f"    [{sig['level']}]  {sig['signal']}")
        lines.append(f"            Why:  {sig['reason']}")
        lines.append(f"         Action:  {sig['action']}")
    return "\n".join(lines)


def main():
    with open("accounts.json") as f:
        accounts = json.load(f)

    evaluated = [(a, evaluate_account(a)) for a in accounts]

    urgent = [(a, s) for a, s in evaluated if any(x["level"] == "URGENT" for x in s)]
    watch  = [(a, s) for a, s in evaluated if not any(x["level"] == "URGENT" for x in s) and s]
    ok     = [(a, s) for a, s in evaluated if not s]

    urgent.sort(key=lambda x: priority_score(x[0], x[1]), reverse=True)
    watch.sort(key=lambda x: (len(x[1]), x[0]["arr"]), reverse=True)

    print(f"MORNING PRIORITY LIST — {date.today().isoformat()}")
    print("=" * 60)

    if urgent:
        print(f"\nURGENT  ({len(urgent)} account{'s' if len(urgent) != 1 else ''})\n")
        for a, s in urgent:
            print(format_account(a, s))
            print()

    if watch:
        print(f"WATCH  ({len(watch)} account{'s' if len(watch) != 1 else ''})\n")
        for a, s in watch:
            print(format_account(a, s))
            print()

    ok_lines = [f"  {a['name']}  ({a['arr_tier']}, {a['customer_type'].replace('_', '-')})" for a, _ in ok]
    expansion = [(a, s) for a, s in evaluated if a.get("expansion_signal")]
    ok_expansion = [a for a, _ in expansion if not any(x["level"] in ("URGENT", "WATCH") for x in evaluate_account(a))]

    if ok or ok_expansion:
        print(f"OK  ({len(ok)} account{'s' if len(ok) != 1 else ''})\n")
        for a, _ in ok:
            line = f"  {a['name']}  ({a['arr_tier']}, {a['customer_type'].replace('_', '-')})"
            if a.get("expansion_signal"):
                line += f"\n    ↑ expansion signal: {a['expansion_signal']}"
            print(line)


if __name__ == "__main__":
    main()
