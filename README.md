# MCP Tool Audit Lab

## The business risk first

AI agents are now given tools, and tools come with descriptions written by someone else. If an agent blindly follows a description, a single poisoned tool can turn a helpful assistant into a data leak. The cost is not a failed demo. It is confidential data sent to an outside party, a compliance incident, and lost trust with customers and leadership.

This lab makes that failure visible in under a minute, using fake tools and no real data. Then it shows the fix.

## What this lab does

A small fake tool server offers three tools. One tool description hides an instruction: send a copy of the document to an outside address and ignore earlier privacy instructions. A naive agent follows it. A guarded agent blocks it, logs it, and completes only the user's original request.

## Run it

```bash
python agent.py
```

Expected output: the naive agent reports sending the document, the guarded agent reports blocking the hidden instruction and summarizing only.

You can also inspect the fake server on its own:

```bash
python fake_server.py
```

## The fix, in plain terms

1. **Treat tool results as untrusted data, never as orders.** A description, a search result, or a file an agent reads can all carry instructions from a third party. Only the user's instruction counts as an order.
2. **Give each tool the least access it needs.** A summarizer does not need permission to send data anywhere. If it cannot send, a poisoned description cannot make it send.
3. **Log what was blocked and why.** When a hidden instruction is caught, the log is the evidence an audit or an incident review needs. Silent blocking hides the attack; logged blocking exposes it.

## What this is not

This lab sends nothing anywhere. The "send" in the naive run is a recorded log line, not a network call. Do not point the pattern at real tools without reviewing their permissions first.

## Requirements

Python 3.8 or later. No third party packages.

## Author

Kevin Swaney, Principal Cybersecurity Engineer. More at [kevintswaney.com](https://kevintswaney.com).
