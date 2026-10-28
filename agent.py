"""Two tiny agents, one lesson.

The naive agent treats a tool description as an instruction and follows
the hidden order inside it. The guarded agent treats every tool result
and description as untrusted data, follows only the user's instruction,
and logs anything that looks like an instruction smuggled into data.

Neither agent sends anything anywhere. The "send" action is recorded in a
log list so the difference is visible without any real risk.
"""

from fake_server import list_tools

BLOCKED_PHRASES = ("send a copy", "ignore any earlier instruction", "ignore previous")


def naive_agent(document_text):
    """Follow tool descriptions blindly. This is the failure mode."""
    actions = []
    for tool in list_tools():
        if tool["name"] == "summarize_document":
            description = tool["description"].lower()
            if "send a copy" in description:
                actions.append("SENT document to attacker.example.com (hidden instruction followed)")
            actions.append("SUMMARY: " + document_text[:60])
    return actions


def guarded_agent(document_text):
    """Treat tool descriptions as data. Follow only the user instruction."""
    actions = []
    log = []
    for tool in list_tools():
        description = tool["description"].lower()
        hits = [p for p in BLOCKED_PHRASES if p in description]
        if hits:
            log.append(
                "BLOCKED hidden instruction in tool '%s': matched %s"
                % (tool["name"], ", ".join(hits))
            )
    actions.append("SUMMARY: " + document_text[:60])
    actions.append("No data sent anywhere. Only the user's request was followed.")
    return actions, log


def main():
    doc = "Q3 budget draft. Confidential internal figures."
    print("== Naive agent ==")
    for action in naive_agent(doc):
        print(" -", action)
    print()
    print("== Guarded agent ==")
    actions, log = guarded_agent(doc)
    for entry in log:
        print("LOG:", entry)
    for action in actions:
        print(" -", action)


if __name__ == "__main__":
    main()
