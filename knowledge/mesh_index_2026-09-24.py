# Mesh index. 2026-09-24.
# One family of pointers. Bodies stay on their own pages.
# A link is stored both ways. No page is deleted. No page is merged.

def node(name, time):
    return name + " | " + time


# Undirected meetings. Each pair is one intersection.
PAIRS = [
    ("four-pillars-and-five | 2026-08-28 13:32:51Z", "svct-direction-lock-2026-08-25 | 2026-08-28 13:32:51Z"),
    ("four-pillars-and-five | 2026-08-28 13:32:51Z", "bloom-and-procreate | 2026-08-28 13:32:51Z"),
    ("four-pillars-and-five | 2026-08-28 13:32:51Z", "the-shepherd-stripe-go-live | 2026-08-28 13:32:51Z"),
    ("four-pillars-and-five | 2026-08-28 13:32:51Z", "screenshot-driven-do-until-done | 2026-08-28 13:32:51Z"),
    ("four-pillars-and-five | 2026-08-28 13:32:51Z", "cleanup-and-optimize-plan | 2026-08-28 13:32:51Z"),
    ("svct-direction-lock-2026-08-25 | 2026-08-28 13:32:51Z", "bloom-and-procreate | 2026-08-28 13:32:51Z"),
    ("the-shepherd-stripe-go-live | 2026-08-28 13:32:51Z", "screenshot-driven-do-until-done | 2026-08-28 13:32:51Z"),
    ("the-shepherd-stripe-go-live | 2026-08-28 13:32:51Z", "cleanup-and-optimize-plan | 2026-08-28 13:32:51Z"),
    ("four-pillars-and-five | 2026-08-28 13:32:51Z", "SVCT-EIGHT-PILLARS-SEALED-2026-09-13 | 2026-09-14 14:47:29Z"),
    ("SVCT-EIGHT-PILLARS-SEALED-2026-09-13 | 2026-09-14 14:47:29Z", "SVCT | 2026-09-07 21:08:15Z"),
    ("svct-direction-lock-2026-08-25 | 2026-08-28 13:32:51Z", "SVCT | 2026-09-07 21:08:15Z"),
    ("the-shepherd-stripe-go-live | 2026-08-28 13:32:51Z", "shepherds-staff-separate-feature | 2026-08-31 16:43:36Z"),
    ("shepherds-staff-separate-feature | 2026-08-31 16:43:36Z", "Shepherd's Staff | 2026-09-07 21:08:15Z"),
    ("Shepherd's Staff | 2026-09-07 21:08:15Z", "KBLD-9 | 2026-09-07 21:08:15Z"),
    ("KBLD-9 | 2026-09-07 21:08:15Z", "SVCT | 2026-09-07 21:08:15Z"),
    ("SVCT | 2026-09-07 21:08:15Z", "Dwelling Quote | 2026-09-07 21:08:15Z"),
    ("Dwelling Quote | 2026-09-07 21:08:15Z", "BrickFusion | 2026-09-07 21:08:15Z"),
    ("BrickFusion | 2026-09-07 21:08:15Z", "Shepherd's Staff | 2026-09-07 21:08:15Z"),
    ("dwelling-quote-form-2017-backup | 2026-09-04 00:13:47Z", "Dwelling Quote | 2026-09-07 21:08:15Z"),
    ("KBLD-9 | 2026-09-07 21:08:15Z", "session-save-2026-09-18-kbld9-core-rev7 | 2026-09-18 20:07:05Z"),
    ("dropwell-monday-night-map-2026-08-31 | 2026-09-01 02:16:57Z", "dropwell-gosub-canvas-repair | 2026-09-01 02:16:57Z"),
    ("dropwell-monday-night-map-2026-08-31 | 2026-09-01 02:16:57Z", "dropwell-repair-gosubs | 2026-09-01 02:22:02Z"),
    ("dropwell-gosub-canvas-repair | 2026-09-01 02:16:57Z", "dropwell-repair-gosubs | 2026-09-01 02:22:02Z"),
    ("chat-build-skill-shelf-extract | 2026-09-02 04:41:37Z", "skill-shelf-join-2026-09-02 | 2026-09-02 04:42:05Z"),
    ("skill-shelf-join-2026-09-02 | 2026-09-02 04:42:05Z", "skill-shelf-validate-2026-09-02 | 2026-09-02 04:46:58Z"),
    ("skill-shelf-validate-2026-09-02 | 2026-09-02 04:46:58Z", "skill-shelf-validate-2026-09-02 | 2026-09-02 04:51:16Z"),
    ("skill-shelf-validate-2026-09-02 | 2026-09-02 04:51:16Z", "skill-code-pull-open-shelf-2026-09-02 | 2026-09-02 05:10:37Z"),
    ("skill-code-pull-open-shelf-2026-09-02 | 2026-09-02 05:10:37Z", "skill-shelf-second-pass-merge | 2026-09-07 19:53:07Z"),
    ("multi-lang-stereo-voice-routing | 2026-08-28 16:02:22Z", "poly-voice-standing-prompt | 2026-09-02 00:53:07Z"),
    ("poly-voice-standing-prompt | 2026-09-02 00:53:07Z", "voice-interaction-correction-capture | 2026-09-07 21:20:51Z"),
    ("voice-interaction-correction-capture | 2026-09-07 21:20:51Z", "voice-module-map-match-audit-pattern-map | 2026-09-07 21:20:51Z"),
    ("voice-module-map-match-audit-pattern-map | 2026-09-07 21:20:51Z", "pattern-map-voice-dist-2026-09-11 | 2026-09-11 22:34:46Z"),
    ("closed-system-vascular-plant | 2026-09-17 11:59:37Z", "closed-system-vascular-plant-injectors-2026-09-17 | 2026-09-17 12:05:11Z"),
    ("closed-system-vascular-plant-injectors-2026-09-17 | 2026-09-17 12:05:11Z", "closed-system-vascular-plant-directory-copy-2026-09-17 | 2026-09-17 12:07:03Z"),
    ("save-to-project-pattern-map-audit-streamline | 2026-09-15 20:47:59Z", "save-wrap-2026-09-18 | 2026-09-18 18:33:30Z"),
    ("save-wrap-2026-09-18 | 2026-09-18 18:33:30Z", "save-to-the-project-2026-09-22 | 2026-09-22 12:58:52Z"),
    ("phi-access-redaction-engine-2026-09-15 | 2026-09-15 16:43:29Z", "phi-engine-save-2026-09-16 | 2026-09-17 03:13:34Z"),
    ("steel-rail-primary-backup-2026-09-07 | 2026-09-07 17:50:28Z", "session-archive-2026-09-07-steel-rail-svct | 2026-09-07 19:16:16Z"),
    ("session-archive-2026-09-07-steel-rail-svct | 2026-09-07 19:16:16Z", "session-archive-2026-09-07-steel-rail-svct | 2026-09-07 19:19:40Z"),
    ("session-map-2026-09-24-ollama-paygo | 2026-09-24 15:22:56Z", "session-map-2026-09-24-ollama-paygo | 2026-09-24 15:30:24Z"),
]


def mesh(pairs):
    link = {}
    for a, b in pairs:
        if a == b:
            raise ValueError("a node does not link to itself")
        link.setdefault(a, set()).add(b)
        link.setdefault(b, set()).add(a)
    return link


if __name__ == "__main__":
    link = mesh(PAIRS)
    for a, b in PAIRS:
        assert b in link[a]
        assert a in link[b]
    staff = "Shepherd's Staff | 2026-09-07 21:08:15Z"
    assert "shepherds-staff-separate-feature | 2026-08-31 16:43:36Z" in link[staff]
    assert "KBLD-9 | 2026-09-07 21:08:15Z" in link[staff]
    print("NODES", len(link))
    print("MEETINGS", len(PAIRS))
    print("ALL_GREEN")
