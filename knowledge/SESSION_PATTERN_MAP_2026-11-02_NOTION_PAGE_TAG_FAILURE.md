# SESSION_PATTERN_MAP_2026-11-02_NOTION_PAGE_TAG_FAILURE

## Attempt
Used `<page url="...">` tags inside `notion-update-page` `insert_content` to add three page references to hop ledger `40ac9bfe-3aff-817c-975a-eca59d3280fe`. Intent: link x-recovery, cos-sweep, and dyneema-streamline pages inline.

## Failure
Notion API returned **400 validation_error**. Message: "Cannot add a page by using the corresponding tag with a URL. URL-bearing block tags preserve existing blocks; they are not inline references." Request ID: `1344c4c3-f929-4e0d-98c7-c6df51fb9cf1`.

## Correction
Switched to standard markdown links in the same `insert_content` call. Three links appended successfully at end of ledger page.

## Dominance (locked)
- **Markdown links** `[- title](url)` are the standing method for **inline page references** in Notion content updates.
- `<page url>` tags are reserved for **block-level page placement** only — moving or positioning an existing page, never for inline citation.
- Any future inline reference uses markdown links. Page tags only when the intent is explicitly a block.

## Outcome
Hop ledger chain continuous. Three November 2 maps linked:
- x-recovery: 40cc9bfe3aff81ee88c1f94380e83845
- cos-sweep: 40cc9bfe3aff8171aa48c5396e7e25c8
- dyneema-streamline: 40cc9bfe3aff81e99717d3ca06c2c88b

Close stamp 16:08 Eastern. Append-only. No edit to prior rows.
