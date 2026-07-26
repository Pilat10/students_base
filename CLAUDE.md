# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Students Base is a Django 6 app for managing departments, groups, and students, with two parallel front ends:
- Server-rendered Django views/templates (`base/views.py`, `base/templates/`) using Django's generic class-based views.
- An AngularJS 1.3 SPA (`static/angular/`, served at `/app/`) that talks to a REST API.

Both front ends operate on the same underlying models and can be used interchangeably; the Angular app is the more actively developed one.

## Commands

Python 3 with Django 6.0.

```bash
uv venv --python 3.14 .venv && source .venv/bin/activate
pip install -r requirements.txt

python manage.py runserver
python manage.py migrate
python manage.py test                 # run all tests (Django + DRF APITestCase)
python manage.py test api             # run just the API tests (api/tests.py)
python manage.py test api.tests.AuthenticationTastCase   # single test case
python manage.py loaddata <fixture>   # fixtures live in fixtures/
python manage.py get_groups           # custom management command listing groups/students
```

Angular app (in `static/angular/`):
```bash
cd static/angular
bower install          # installs angular, angular-route, bootstrap, angular-mocks
npm install
npm test                # runs `karma start test/karma.conf.js` — note the pinned karma
                        # ~0.12 / karma-chrome-launcher ~0.1 toolchain predates modern
                        # Node and may not install; treat the specs as documentation
                        # of the API contract if so.
```

## Architecture

### Django apps
- `students_base/` — project settings/urls/wsgi. `students_base/urls.py` wires up `/admin/`, `/api/v1/` (delegated to `api/urls.py`), the server-rendered `/groups`, `/student` CRUD routes, login/logout, and the Angular SPA shell at `/app/`.
- `base/` — core domain models, server-rendered views, forms, auth backend, and a signal-based audit log.
- `api/` — Django REST Framework API layer (serializers, views, mixins) consumed by the Angular SPA.

### Domain model (`base/models.py`)
`Department` → has many `Group` → has many `Student`. A `Group` has an optional `headman` (a `OneToOneField` to `Student`, `on_delete=SET_NULL`). Deleting a `Department`/`Group` cascades to its children (`on_delete=CASCADE` on the `Group.department`/`Student.group` FKs). `LogEntry` (the audit log model) also lives here.

### Audit logging via signals
`base/signals.py` connects `post_save`/`post_delete` on `Group` and `Student` to write a `LogEntry` recording add/change/delete actions. The receivers are registered in `base/apps.py::BaseConfig.ready()` (not at import time in `models.py`) via `@receiver(..., sender='base.Group', dispatch_uid=...)`. When adding a new model that should be audited, connect its signals the same way in `ready()`; when changing `Group`/`Student` save behavior, be aware the signal handler fires on every save.

### Custom authentication
`base/auth.py` defines `MyAuth`, a custom auth backend (subclassing `django.contrib.auth.backends.ModelBackend`) that authenticates by **email** instead of username (looks up `User` by `email` field). It's listed in `AUTHENTICATION_BACKENDS` in `students_base/settings.py` ahead of Django's default `ModelBackend`, so both email-based and username-based login work. `/login_email/` in `students_base/urls.py` is the email-based login route.

### REST API (`api/`)
- Endpoints: `/api/v1/department/`, `/api/v1/group/`, `/api/v1/student/` (list/detail, DRF generics), plus `/api/v1/auth/` (session login/logout) and `/api/v1/auth-token/` (token-based login, returns a DRF authtoken). Schema/docs live at `/api/v1/schema/` and `/api/v1/docs/` (drf-spectacular).
- `GroupListView` supports `?department_id=`. `StudentListView` supports both `?group_id=` and `?department_id=` (the latter filters through `group__department`, since `Student` has no direct FK to `Department`); both can be combined.
- `REST_FRAMEWORK` in settings enables both `SessionAuthentication` and `TokenAuthentication`. The Angular SPA authenticates via session cookie + CSRF (never calls `/auth-token/`); the token endpoint exists for non-browser clients. Session-based `LoginView`/`LoginTokenView` in `api/views.py` both call `django.contrib.auth.authenticate`/`login`, so email-based login works through the API too via `MyAuth`.
- **Response envelope**: all API responses are wrapped by mixins in `api/mixins.py`. `ResponseDataWrapperMixin` wraps success responses as `{"status": "success", "data": ...}` and failures as `{"status": "fail", "data": ...}`; `ResponseDataWrapperMixinSuccess` (used only by `LoginTokenView`) uses `{"success": true/false, "data": ...}` instead. Keep this distinction in mind — the two envelope shapes are not interchangeable, and any new API view should pick one of these mixins deliberately rather than skip wrapping.
- **Do not enable DRF pagination** (`DEFAULT_PAGINATION_CLASS`/`PAGE_SIZE`). List endpoints return a bare JSON array under `data`; the Angular SPA iterates that array directly, and paginating it would silently blank every table.
- `DepartmentSerializer` computes `count_group`, `count_student`, and `avg_age` (average student age in the department) via `SerializerMethodField`s rather than model properties — these are computed per-request with extra queries, not cached.
- `GroupSerializer.headman` uses a custom `EmptyStringAsNullPKField` so a JSON `"headman": ""` from the SPA (meaning "no headman") is coerced to `None` instead of raising a validation error.

### Angular SPA (`static/angular/js/`)
- Served via `students_base/urls.py`'s `/app/` route (`TemplateView` rendering `templates/index_angular.html`, wrapped in `ensure_csrf_cookie` so the SPA can obtain a CSRF cookie for its session-authenticated API calls). `index_angular.html` sets `<base href="/app/" />` so Angular's html5Mode routing doesn't collide with the server-rendered `/groups` routes.
- `app.js` defines routes via `ngRoute` (`$routeProvider`), mapping URLs like `/departments`, `/departments/:departmentId`, `/groups`, `/groups/:groupId` to templates in `static/angular/views/` and controllers in `controllers.js`.
- `services.js` holds API service wrappers; `derectives.js` (note: misspelled, matches existing filename — don't "fix" the spelling without updating all references) holds custom directives.
- CSRF is wired via `$httpProvider.defaults.xsrfCookieName/xsrfHeaderName` matching Django's `csrftoken`/`X-CSRFToken`.
- Dependency management is bower (`bower.json`) for browser libs and npm (`package.json`) only for the karma test runner — there's no build/bundle step; files are served directly as static assets.

### Templates
Server-rendered templates live under `templates/` (base site templates, e.g. `registration/login.html`) and `base/templates/base/` (group/student CRUD templates used by the Django CBVs in `base/views.py`).
