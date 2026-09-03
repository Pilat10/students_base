# AI workflow log — CSV export of students (Variant 1)

**Tool used:** Claude Code (CLI agent, Sonnet 5), working directly in this repo checkout.

This log covers the whole cycle for one feature: requirements → design decisions → implementation
→ tests → docs, all done in a single Claude Code session.

## 1. Requirements gathering (the "grill" interview)

Instead of a single freeform prompt, requirements were extracted through a structured
question-by-question interview (the `/grill-me` skill). The assistant first read the codebase
(`base/models.py`, `api/views.py`, `base/admin.py`, `static/angular/js/controllers.js`, DRF
settings) to find real gaps rather than inventing hypothetical ones, then proposed three concrete
candidates:

1. An activity-log viewer for the existing but UI-less `LogEntry` audit model.
2. A student search box in the Angular SPA, wired to the API's already-existing `?q=` filter.
3. CSV export of the student list.

**Correction #1 (user overrode the AI's recommendation):** the assistant's default pick was the
activity-log viewer ("smallest schema risk"). The user picked **CSV export** instead. No changes
were made to accommodate this beyond building the feature actually requested — the AI's
recommendation was not authoritative, just a starting point for the interview.

From there, each remaining question resolved one design branch at a time, with an AI-recommended
option offered first and the user free to pick a different one:

| Decision | AI recommendation | User's choice |
|---|---|---|
| Front end | Angular SPA only | Angular SPA only (agreed) |
| Filter behavior | Respect current `group_id`/`department_id`/`q` filters | Agreed |
| CSV columns | Denormalized: fio, birthday, card number, group name, department name | Agreed |
| Endpoint shape | Dedicated `GET /api/v1/student/export/` view, not content negotiation on the existing list endpoint | Agreed |
| Download trigger | Plain `<a href>` (session cookie handles auth, GET needs no CSRF token) | Agreed |
| Test edge cases | 401 + empty-result CSV (baseline) vs. also covering CSV-injection escaping | Baseline only |
| Deliverable files | Separate `workflow.md` + `report.md` at repo root | Agreed |

## 2. Implementation prompt

Single instruction after the interview: **"Yes, go ahead and implement it."** Everything from
here — the view, URL wiring, Angular link, and tests — was generated and applied by the assistant
in one pass, then verified by actually running the test suite (see below), not just by inspection.

## 3. Where the AI got it wrong, and how that was caught

While writing `StudentExportTestCase.test_export_requires_authentication`, the assistant assumed
an anonymous request to the new endpoint would return `401 Unauthorized` (mirroring the project's
custom `LoginView`, which returns 401 explicitly). Running `python manage.py test api` failed:

```
AssertionError: 403 != 401
```

Root cause, verified in code: this endpoint doesn't hand-code its auth response — it relies on
DRF's default `IsAuthenticated` permission and the project's `DEFAULT_AUTHENTICATION_CLASSES`
(`SessionAuthentication` first, then `TokenAuthentication`). DRF's exception handler only returns
401 when the first authenticator's `authenticate_header()` is non-`None`; `SessionAuthentication`
returns `None`, so an unauthenticated request to *any* generic DRF view in this project (not just
this new one) gets `403`, not `401`. The assistant fixed the test assertion to `403` and added a
comment explaining why, rather than changing the view to force a different status code the rest of
the API doesn't use.

This is the concrete instance of "AI proposed something that was checked against real behavior,
found wrong, and corrected" called for by the course brief — caught by running tests, not by
review alone.

## 4. Verification performed

- `python manage.py test api` — 34/34 passing, including 6 new `StudentExportTestCase` tests.
- `python manage.py test` (full suite) — 34/34 passing, no regressions elsewhere.
- Read back every generated diff (`api/views.py`, `api/urls.py`, `api/tests.py`,
  `static/angular/js/controllers.js`, `static/angular/views/student_list.html`) before accepting
  it, checking against existing conventions (`ResponseDataWrapperMixin` usage, the
  `dep_url_get`-style query-string building already in `StudentList`'s controller, the
  `filter_students_by_name` helper already in `api/views.py`).

## 5. Known gap in this log

The brief asks for examples from **at least two different AI tools** (e.g. an IDE assistant plus a
separate chat model), each with its own case and a verdict on fitness for that task. This log only
covers one tool (Claude Code, end-to-end). `homework-02.md` in this same repo documents a
comparison of Claude Code across two different context-scope tasks, which can supplement this if
you need a second-tool example — but that is Claude Code again, not a distinct tool. If the
grading rubric strictly requires a second, different tool (e.g. ChatGPT/another chat model used
manually to review the same diff), that step still needs to be done and logged separately; it was
not fabricated here.
