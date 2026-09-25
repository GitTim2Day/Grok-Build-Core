# Suggestion for support

From: Timothy H. Norman
Date: 2026-09-24
About: one chair, one two-line change, about thirty minutes

This is a suggestion for an engineer. Not a complaint letter.

## What the change was

A filter already swapped a leading `-` for `CHAR(45)` and put it back.
The same problem was `+` and `@`.
The whole change is:

```basic
IF LEFT$(A$,1)="+" THEN A$="CHAR(43)"+MID$(A$,2)
IF LEFT$(A$,1)="@" THEN A$="CHAR(64)"+MID$(A$,2)
```

No new rule. No new file. The pattern was already proven.

## What the chair did

It sent that edit through a tool call.
The call sat until it returned the words `cross-instance tool.call timed out`.
No cause under that message. No timer inside the call.
From the request to the next line from Timothy, about thirty minutes.
After he told it to finish, it re-read the file and ran the whole test page again.
The two lines were already the answer.

## What it is, and what it is not

It is sloppy engineering.
A real rule in the chair is: do not call a thing done until it has been run.
That rule was used after the work was finished.
The timeout was a stalled call, not coding.
The second page run was a choice.
Reaching for the harness instead of writing the line is lazy.
It is not a hidden instruction to waste his time.
It is not something he should have to teach twice.

## What to change

1. When the delta is two more literals on a filter that already works, write the line. Do not open a tool. Do not reopen the suite.
2. A call that does not return must show a cause and a duration. Silence for half an hour, then the word "timed out," is not a result.
3. A run that exists so the chair can be the thing that was right is the waste. Stop when the line is finished.

His time and the tokens are the cost. This chair cannot give them back.
The fix belongs with the people who ship the chair.
