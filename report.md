# Report — CSV export of students

**Variant:** 1 — AI-assisted feature delivery.
**Companion log:** see `workflow.md` for the AI prompts, decisions, and the one case where AI
output was wrong and had to be corrected against real test output.

## User story

As a user browsing the student list (optionally filtered to one group), I want to export the
students I'm currently looking at as a CSV file, so I can open it in a spreadsheet or hand it to
someone who doesn't have access to this app.

## Acceptance criteria

- `GET /api/v1/student/export/` returns `Content-Type: text/csv` with a header row
  (`fio, birthday, number_student_cart, group, department`) followed by one row per matching
  student.
- The endpoint accepts the same `group_id`, `department_id`, and `q` query parameters as
  `GET /api/v1/student/`, and applies them identically (same `filter_students` helper is shared by
  both views).
- A request that matches zero students still returns `200 OK` with just the header row — not an
  error.
- An unauthenticated request is rejected (`403`, matching this project's existing behavior for
  every other DRF view under `IsAuthenticated` + `SessionAuthentication`/`TokenAuthentication`).
- In the Angular SPA, the student list page (`static/angular/views/student_list.html`) has an
  "Export to CSV" link whose URL includes the `group_id` filter currently applied to that page.

## Explicit scope boundaries — what this feature does NOT do

- No export for `Group` or `Department` lists — students only.
- No background/async job — the response is generated and streamed synchronously in one request.
- No format other than CSV (no XLSX, no PDF).
- No pagination of the exported rows — the export always contains every row matching the filter,
  consistent with this project's project-wide "never paginate list data" rule
  (`students_base/settings.py`).
- No export trigger added to the server-rendered Django views (`base/views.py`) — Angular SPA only,
  per the resolved design decision.
- Column set is fixed (fio, birthday, card number, group, department); no user-configurable column
  selection.

## Implementation summary

- `api/views.py`: extracted the group/department/name filtering that `StudentListView` already did
  into a shared `filter_students()` function, and added `StudentExportView` (`APIView`, not wrapped
  in `ResponseDataWrapperMixin` since CSV isn't JSON) that reuses it and streams a CSV via
  `csv.writer` into an `HttpResponse`.
- `api/urls.py`: new route `student/export/`, name `api:student-export`.
- `static/angular/js/controllers.js`: `StudentList` controller now builds `$scope.exportUrl` from
  the same `dep_url_get` query string it already uses for the JSON fetch.
- `static/angular/views/student_list.html`: new `<a ng-href="{{ exportUrl }}">Export to CSV</a>`.
- `api/tests.py`: new `StudentExportTestCase` (6 tests) — auth rejection, unfiltered export, filter
  by `group_id`, filter by `department_id`, filter by `q`, and the empty-result/header-only case.

## PR / review checklist

- [x] `filter_students()` is the single source of truth for student filtering — `StudentListView`
      and `StudentExportView` cannot drift apart on what `?group_id=`/`?department_id=`/`?q=` mean.
- [x] New endpoint relies on the project's existing `DEFAULT_PERMISSION_CLASSES` /
      `DEFAULT_AUTHENTICATION_CLASSES` rather than hand-rolling auth — no new security surface.
- [x] `select_related('group__department')` used in the export queryset to avoid N+1 queries per
      row (each row needs `student.group.name` and `student.group.department.name_department`).
- [x] CSV response does not go through `ResponseDataWrapperMixin` — verified this is intentional
      (mixin is JSON-only) and documented with a docstring on `StudentExportView`.
- [x] No pagination added anywhere — checked against the project's explicit "do not paginate"
      settings comment.
- [x] Tests cover the happy path, all three filters, the empty-result edge case, and the
      unauthenticated-request case.
- [x] Full test suite (`python manage.py test`) passes: 34/34, no regressions.
- [ ] Not covered: CSV-escaping of `fio` values containing commas/quotes/newlines. Python's `csv`
      module handles this correctly by construction (any value with a comma, quote, or newline is
      automatically quoted), so this is believed safe, but no test exercises it — flagged here
      rather than silently assumed.

## Risks, limitations, and what AI actually saved/cost

**Where AI helped:** the interview-driven requirements pass surfaced three real gaps in the
codebase (audit log with no UI, dead `?q=` filter with no UI consumer, and no export at all) by
actually reading the code rather than guessing — this took a few file reads instead of the user
having to audit the codebase manually. Once the design was pinned down, generating the view, URL,
Angular wiring, and 6 tests in one pass was faster than writing each by hand, and the code follows
the existing conventions (the `filter_students_by_name` pattern, the `dep_url_get`-string-building
pattern in the Angular controller) because the assistant matched what was already there instead of
introducing a new style.

**Where AI got it wrong:** the first version of the auth-rejection test assumed a `401` response;
the real status is `403`, because of how this project's `DEFAULT_AUTHENTICATION_CLASSES` ordering
interacts with DRF's exception handling. This was only caught because the test was actually run
(`python manage.py test`), not because it was reviewed by eye — a reminder that AI-generated
assertions about framework behavior need to be checked against a real run, not trusted from
pattern-matching against a superficially similar case (the project's *custom* `LoginView`, which
does hard-code 401).

**Known limitations of this feature, not just this delivery process:**
- Synchronous CSV generation means very large student tables (this project has none currently, but
  hypothetically) would hold the request open for the full query + serialization time — there's no
  streaming/chunked response, just a single `HttpResponse` built in memory.
- No column customization or localized headers — headers are the raw field names.
- The "download trigger" being a plain link means there's no client-side loading indicator or error
  handling if the request fails (e.g. session expired) — the browser just navigates and DRF returns
  a JSON 403/500 body as if it were a file, which is a poor user experience if it happens, though
  functionally correct for the primary path.

**Outstanding item from the course brief:** the brief calls for evidence from **two different AI
tools**, each with a documented case and verdict. This delivery only used one (Claude Code,
end-to-end). See `workflow.md` §5 for the honest note on that gap.
