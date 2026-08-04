# Homework 02 — chose AI-tools

## Task A — Filter students by department

| Field | Value |
|---|---|
| Technology | Python, Django, DRF |
| Context | API for storing students data |
| Instrument | Claude Code VSCode extension |

**Why this instrument?** In any case copilot use external models so I prefer to chose models by
myself. Also I like to work with Claude Code and use it daily

**Prompt**

> `@api/views.py#72-77` add possibility to filter students by `'department_id'` to see a list of
> students in specific department

**Result**

<details>
<summary>Before</summary>

```python
class StudentListView(ResponseDataWrapperMixin, generics.ListCreateAPIView):
    """

    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        group_id = self.request.query_params.get('group_id', None)
        if group_id is not None:
            return super().get_queryset().filter(
                group__pk=group_id)
        return super().get_queryset()
```

</details>

<details>
<summary>After</summary>

```python
class StudentListView(ResponseDataWrapperMixin, generics.ListCreateAPIView):
    """

    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        group_id = self.request.query_params.get('group_id', None)
        if group_id is not None:
            queryset = queryset.filter(group__pk=group_id)
        department_id = self.request.query_params.get('department_id', None)
        if department_id is not None:
            queryset = queryset.filter(group__department__pk=department_id)
        return queryset
```

</details>

---

## Task B — Onboarding walkthrough of `api/`

| Field | Value |
|---|---|
| Technology | Python, Django, DRF |
| Context | API for storing students data |
| Instrument | Claude Code VSCode extension |

**Why this instrument?** In any case copilot use external models so I prefer to chose models by
myself. Also I like to work with Claude Code and use it daily

**Prompt**

> `@api/` I'm Onbording new member. Explain: what it does, what dependancies, what main 2 issues have?

**Result**

### What it does

The DRF layer backing the AngularJS SPA at `/app/`. Mounted at `/api/v1/` from
`students_base/urls.py`; routes declared in `api/urls.py`.

| Endpoint | View | Notes |
|---|---|---|
| `department/`, `department/<pk>/` | `DepartmentListView` / `DepartmentDetailView` | plain CRUD |
| `group/`, `group/<pk>/` | `GroupListView` / `GroupDetailView` | list supports `?department_id=` |
| `student/`, `student/<pk>/` | `StudentListView` / `StudentDetailView` | list supports `?group_id=` and `?department_id=` (via `group__department`) |
| `auth/` | `LoginView` | POST login, GET whoami, DELETE logout — session cookie |
| `auth-token/` | `LoginTokenView` | POST returns a DRF authtoken |
| `schema/`, `docs/` | drf-spectacular | OpenAPI 3 + Swagger UI |

Three conventions a newcomer has to know:

1. **Every response is enveloped.** `api/mixins.py` hooks `finalize_response` and rewraps
   `response.data` as `{"status": "success"|"fail", "data": ...}`. `LoginTokenView` alone uses
   the subclass with `{"success": true|false, ...}`. Two shapes, not interchangeable.
2. **No pagination, deliberately.** `students_base/settings.py` carries a warning comment — the
   SPA iterates `data.data` as a bare array, so enabling `PAGE_SIZE` blanks every table.
3. **Derived fields live in the serializers**, not on the models: `count_group` / `count_student`
   / `avg_age` on `DepartmentSerializer`, `count_student` / `headman_name` on `GroupSerializer`.
   `EmptyStringAsNullPKField` exists purely because the SPA posts `"headman": ""` to mean "none".

Auth: session + token both enabled, `IsAuthenticated` by default. Email login works here too
because `base/auth.py::MyAuth` is in `AUTHENTICATION_BACKENDS` and both login views go through
`django.contrib.auth.authenticate`.

### Dependencies

Runtime (`requirements.txt`): `Django 6.0.7`, `djangorestframework 3.17.1`,
`drf-spectacular 0.30.0`, `Markdown` (renders the `<pre>` docstrings in the browsable API),
`gunicorn`. Plus `rest_framework.authtoken` for the token model.

Internal: `api/` depends on `base.models` (`Department`/`Group`/`Student`) and
`django.contrib.auth.models.User`. Nothing depends on `api/` except the SPA over HTTP — so the
API contract *is* the coupling, and `api/tests.py` (~28 cases) is what pins it.

### Two main issues

**1. N+1 query explosion in `DepartmentSerializer`.** Per department, `get_count_group` is a
query, `get_count_student` is a query, and `get_avg_age` calls `get_count_student` *again* (third
query) then loads every student row in the department to sum ages in Python. Four queries plus a
full student fetch per department, on an unpaginated list endpoint. `GroupSerializer.get_count_student`
has the same shape. Fix: annotate in `get_queryset()` — `Count('group')`, `Count('group__student')`,
and an age aggregate.

**2. `LoginTokenView` is partly broken and duplicates `LoginView`.** It sets
`authentication_classes = ()`, correct for POST but it means `request.user` is always anonymous on
the other verbs — `GET /auth-token/` always 401s even with a valid token, and `DELETE` calls
`logout()` on a request with no session. Both verbs are dead code that looks live. On top of that
`credentials()`, `get()` and `delete()` are copy-pasted verbatim from `LoginView`, so the two auth
endpoints will drift. Fix: extract a shared base class, drop or repair the unauthenticated verbs.

Smaller things noted but not raised as main issues: most view docstrings are empty (they are the
Swagger descriptions), and `LoginView.permission_classes = ()` leaves the logout `DELETE` open to
anonymous callers.

---

## Task C

| Field | Value |
|---|---|
| Technology | Python, Django, DRF |
| Context | API for storing students data |
| Instrument | Claude Code VSCode extension |

**Why this instrument?** In any case copilot use external models so I prefer to chose models by
myself. Also I like to work with Claude Code and use it daily

**Prompt**

> @api/views.py LoginView and LoginTokenView duplicate credentials(), get(), and delete() almost verbatim. Extract a shared base class so only post() differs between them, and flag whether LoginTokenView's inherited get()/delete() are actually reachable given authentication_classes = ().

**Result**

<details>
<summary>Before</summary>

```python
class LoginView(ResponseDataWrapperMixin, APIView):
    """
    <pre>
        {
         "username": "admin",
         "password": "admin"
        }
    </pre>
    """
    permission_classes = ()

    def credentials(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            return user
        return None

    def post(self, request):
        user = self.credentials(request)
        if not user:
            return Response(
                {"error": "wrong username or password"}, HTTP_401_UNAUTHORIZED)
        login(request, user)
        return Response(
            {"user": UserSerializer(user, context={"request": request}).data})

    def get(self, request, format=None):
        content = {
            'user': str(request.user),
            'auth': str(request.auth),
        }
        if not request.user.is_authenticated:
            return Response(content, HTTP_401_UNAUTHORIZED)
        return Response(content)

    def delete(self, request):
        logout(request)
        return Response({})


class LoginTokenView(ResponseDataWrapperMixinSuccess, APIView):
    """
    <pre>
        {
         "username": "admin",
         "password": "admin"
        }
    </pre>
    """
    authentication_classes = ()
    permission_classes = ()

    def credentials(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            return user
        return None

    def post(self, request):
        user = self.credentials(request)
        if not user:
            return Response(
                {"error": "wrong username or password"}, HTTP_401_UNAUTHORIZED)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user": UserSerializer(user, context={"request": request}).data
            })

    def get(self, request, format=None):
        content = {
            'user': str(request.user),
            'auth': str(request.auth),
        }
        if not request.user.is_authenticated:
            return Response(content, HTTP_401_UNAUTHORIZED)
        return Response(content)

    def delete(self, request):
        logout(request)
        return Response({})
```

</details>

<details>
<summary>After</summary>

```python
class BaseLoginView(APIView):
    """
    <pre>
        {
         "username": "admin",
         "password": "admin"
        }
    </pre>
    """
    permission_classes = ()

    def credentials(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            return user
        return None

    def get(self, request, format=None):
        content = {
            'user': str(request.user),
            'auth': str(request.auth),
        }
        if not request.user.is_authenticated:
            return Response(content, HTTP_401_UNAUTHORIZED)
        return Response(content)

    def delete(self, request):
        logout(request)
        return Response({})


class LoginView(ResponseDataWrapperMixin, BaseLoginView):

    def post(self, request):
        user = self.credentials(request)
        if not user:
            return Response(
                {"error": "wrong username or password"}, HTTP_401_UNAUTHORIZED)
        login(request, user)
        return Response(
            {"user": UserSerializer(user, context={"request": request}).data})


class LoginTokenView(ResponseDataWrapperMixinSuccess, BaseLoginView):
    authentication_classes = ()

    def post(self, request):
        user = self.credentials(request)
        if not user:
            return Response(
                {"error": "wrong username or password"}, HTTP_401_UNAUTHORIZED)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user": UserSerializer(user, context={"request": request}).data
            })
```

</details>

---
