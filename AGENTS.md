# Students Base project rules

## Technology stack

- Python 3.14, Django 6.0, Django REST Framework 3.17, SQLite.
- AngularJS 1.3 consumes the REST API directly; there is no frontend build step.
- Run backend tests with `python manage.py test` or API tests with
  `python manage.py test api`.

## Architecture and directory responsibilities

- `base/models.py` contains the `Department`, `Group`, `Student`, and
  `LogEntry` domain models.
- `base/views.py`, `base/forms.py`, and `base/templates/` implement the
  server-rendered Django interface.
- `api/views.py` owns HTTP endpoint behavior and QuerySet filtering.
- `api/serializers.py` owns REST input/output fields and validation.
- `api/mixins.py` owns the API response envelopes.
- `api/urls.py` only maps URL paths to API views.
- `api/tests.py` contains DRF API tests.
- `static/angular/` contains the AngularJS client.

## Concrete implementation rules

1. Every new DRF API view must use `ResponseDataWrapperMixin`, except token
   login, which uses `ResponseDataWrapperMixinSuccess`.
2. Implement API collection filters in `api/views.py` by extending the
   relevant view's `get_queryset()`. Query only through Django QuerySets;
   do not load a collection and filter it in Python.
3. Put reusable QuerySet filter helpers at module level in `api/views.py`.
   Keep them pure: accept a QuerySet and request parameters, return a
   QuerySet, and do not call `.get()`, `.first()`, or `list(queryset)`.
4. Normalize optional text query parameters with `.strip()`. A missing,
   empty, or whitespace-only parameter must leave the QuerySet unchanged.
   Use `__icontains` for case-insensitive name matching.
5. Preserve the existing `{"status": "success|fail", "data": ...}` response
   envelope and the `{"success": true|false, "data": ...}` token-login
   envelope.
6. Update `api/tests.py` whenever an endpoint, query parameter, serializer
   field, or response shape changes. Assert both the HTTP status and the
   wrapped response data.
7. Model changes belong in `base/models.py` and require a migration. Do not
   place domain fields in serializers or views.
8. Keep API route declarations in `api/urls.py`; project-level routing stays
   in `students_base/urls.py`.

## Explicit prohibitions

- DO NOT enable DRF pagination. AngularJS templates iterate the bare array
  stored under `response.data.data`.
- Forbidden: returning unwrapped API responses from new or changed DRF
  views.
- DO NOT put database queries or API filtering logic in `api/urls.py`,
  `students_base/urls.py`, templates, or AngularJS controllers.
- Forbidden: renaming `static/angular/js/derectives.js` unless every
  reference is updated in the same scoped task.
- DO NOT change existing function signatures or create files outside the
  prompt's explicit scope.

## Correct filtering pattern

```python
# api/views.py
def filter_students_by_name(queryset, query_params):
    search_term = query_params.get("q", "").strip()
    if not search_term:
        return queryset
    return queryset.filter(fio__icontains=search_term)


class StudentListView(ResponseDataWrapperMixin,
                      generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = super().get_queryset()
        # Preserve the existing ID filters before applying the text filter.
        return filter_students_by_name(queryset, self.request.query_params)
```

Do not filter a serialized list inside the view:

```python
# Forbidden
students = StudentSerializer(queryset, many=True).data
return [student for student in students if query in student["fio"]]
```
