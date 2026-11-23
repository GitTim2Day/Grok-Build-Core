# OPENAI SUPPORT FOLLOW-UPS — GOSUB/RETURN MITIGATION STRATEGY

Stamp: Sunday, November 22, 2026 11:44:45 PM America/New_York

Context note: These were sent after learning OpenAI had already caught one of the GOSUB/RETURN patterns. They are the mitigation strategy (review-card gate + append-only audit log) offered proactively.

---

## Message 1: Review-card gate

OpenAI Support,
Please route this follow-up to the team responsible for agent controls and model evaluation. It builds on my GOSUB and RETURN proposal by giving the operator a clear place to review and authorize an external action.
For email, the agent prepares the draft and returns control to a review card. The card shows the actual To, CC, and BCC recipients, subject, body, and attachments. The operator can edit, cancel, or select “Approve and send.” Until that button is pressed, the message stays pending.
The send service should enforce the approval. It sends only the exact version shown to the operator and accepts the approval once. If a recipient, the message, or an attachment changes, the revised version goes back for review. An append-only record can capture the approved version, the operator’s decision, and the send outcome.
Timothy H. Norman
Summary: Have the agent return a review card and require the operator to approve the exact message before the send service can send it.

---

## Message 2: Append-only audit log

OpenAI Support,
Please route this follow-up to the team responsible for agent controls and model evaluation. It extends my GOSUB and RETURN and approval-card proposals with an append-only audit record.
For each action, record the authenticated account that requested it, the agent or tool that handled it, the proposed action and its scope, any human approval or denial, and the outcome. Use one action ID to link those events. Include blocked attempts and actions taken through helper services so reviewers can reconstruct what happened and investigate patterns of possible misuse.
Use stable internal account identifiers and restrict access to the log. The record should establish which account initiated the request and whether the agent stayed within its authorization.
Timothy H. Norman
Summary: Link each request, approval decision, and outcome in an append-only audit log to make agent behavior traceable.

---

SHA-256: f643bd8379383eb782643723455c1e30c3f021f289f11df4b162673586f7b4ae
Ledger hop: 1a206b8bb4d8a06a
Pointer: session-map-2026-11-22-openai-gosub-mitigation
