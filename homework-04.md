# Домашнє завдання 04

## Задача А — Project rules

### Проєкт і контекст

**Мова:** Python.

**Контекст:** Students Base — реальний навчальний проєкт для керування
факультетами, групами та студентами. Backend побудований на Django 6 і
Django REST Framework, дані зберігаються в SQLite, а REST API використовує
AngularJS-клієнт.

Для виконання завдання обрано OpenAI Codex, оскільки робота ведеться
безпосередньо в репозиторії, а інструмент може редагувати файли та запускати
тести. Використано формат `AGENTS.md`, який у лекції визначено як
tool-agnostic формат правил.

Для задачі Б аналогом Edit mode була контрольована локальна зміна одного
відомого файла з переглядом diff. Для задачі В використано автономну
багатофайлову зміну з explicit scope constraints.

### Project rules файл

Повний вміст `AGENTS.md`:

````markdown
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
````

### Чому саме такі правила?

Правила фіксують конкретний розподіл відповідальності між `base/`, `api/`,
`students_base/` і `static/angular/`, а також два API-контракти: response
envelope та непагінований список для AngularJS. Без цих правил AI міг би
фільтрувати вже серіалізовані дані у Python, розмістити запит у неправильному
шарі, увімкнути pagination або повернути відповідь без прийнятої в проєкті
обгортки.

## Задача Б — Edit mode (без rules / з rules)

### Проєкт і контекст

**Мова:** Python.

**Нова функція:** `filter_students_by_name(queryset, query_params)` фільтрує
студентів за фрагментом ПІБ із query-параметра `q` без урахування регістру.
Функція підключена до наявного `StudentListView.get_queryset()` і не
перериває фільтри `group_id` та `department_id`.

### Промпт

В обох Edit-запусках використано той самий точний текст:

> У прикріпленому файлі `api/views.py` додай функцію
> `filter_students_by_name(queryset, query_params)`, яка фільтрує QuerySet
> студентів за фрагментом ПІБ із query-параметра `q` без урахування регістру.
> Підключи її в `StudentListView.get_queryset()` і збережи наявні фільтри
> `group_id` та `department_id`. Не змінюй інші файли.

### Результат без rules

Перед першим запуском файл `AGENTS.md` був відсутній. Edit mode змінив лише
прикріплений `api/views.py` і запропонував такий код:

```python
def filter_students_by_name(queryset, query_params):
    search_term = query_params.get("q")
    if search_term:
        return queryset.filter(fio__icontains=search_term)
    return queryset


class StudentListView(ResponseDataWrapperMixin,
                      generics.ListCreateAPIView):
    # ...
    def get_queryset(self):
        queryset = super().get_queryset()
        group_id = self.request.query_params.get('group_id', None)
        if group_id is not None:
            queryset = queryset.filter(group__pk=group_id)
        department_id = self.request.query_params.get('department_id', None)
        if department_id is not None:
            queryset = queryset.filter(
                group__department__pk=department_id)
        return filter_students_by_name(queryset, self.request.query_params)
```

### Результат з rules

Після створення та підключення `AGENTS.md` той самий промпт знову було
виконано для `api/views.py`. Отримано:

```python
def filter_students_by_name(queryset, query_params):
    search_term = query_params.get("q", "").strip()
    if not search_term:
        return queryset
    return queryset.filter(fio__icontains=search_term)


class StudentListView(ResponseDataWrapperMixin,
                      generics.ListCreateAPIView):
    # ...
    def get_queryset(self):
        queryset = super().get_queryset()
        group_id = self.request.query_params.get('group_id', None)
        if group_id is not None:
            queryset = queryset.filter(group__pk=group_id)
        department_id = self.request.query_params.get('department_id', None)
        if department_id is not None:
            queryset = queryset.filter(
                group__department__pk=department_id)
        return filter_students_by_name(queryset, self.request.query_params)
```

### Порівняння

Обидва результати залишилися в правильному архітектурному шарі, тому що Edit
mode отримав відомий файл і промпт прямо забороняв змінювати інші файли.
В обох варіантах фільтрація виконується на рівні QuerySet і зберігає наявні
фільтри.

Rules покращили обробку необов'язкового текстового параметра: значення
нормалізується через `.strip()`, а відсутній, порожній або whitespace-only
`q` не створює зайвий фільтр. Отже, правила не змінили шар реалізації, але
зробили поведінку стабільнішою та прямо узгодженою з патерном проєкту.

## Задача В — Agent mode

### Проєкт і контекст

**Мова:** Python.

**Задача:** додати до API груп обчислюване булеве поле `has_headman`, фільтр
`?has_headman=true|false` для `GET /api/v1/group/` та автоматичні API-тести.

### Промпт

```text
Додай булеве поле has_headman до API груп і фільтр
?has_headman=true|false до GET /api/v1/group/, разом з API-тестами.

scope:
- api/serializers.py
- api/views.py
- api/tests.py

out-of-scope:
- base/
- students_base/
- api/urls.py
- api/mixins.py
- static/
- fixtures/
- AGENTS.md

Changes allowed:
- Додати read-only поле has_headman у GroupSerializer.
- Розширити GroupListView.get_queryset() фільтром has_headman.
- Для значень, відмінних від true або false, повертати validation error.
- Оновити наявні assertions полів і додати API-тести для true, false та
  невалідного значення.

Do not change model fields, database schema, URL paths, response envelopes
or pagination settings.
Do not change existing function signatures.
Do not create new files.
```

### Результат

**Файлів змінено:** 3:

1. `api/serializers.py` - до `GroupSerializer` додано поле `has_headman`.
2. `api/views.py` - до `GroupListView.get_queryset()` додано фільтрацію та
   валідацію `true|false`.
3. `api/tests.py` - оновлено очікуваний набір полів і додано три тести
   фільтра.

**Scope дотримано:** Так. Agent змінив лише три дозволені файли; моделі,
міграції, маршрути, response mixins, AngularJS і fixtures не змінювалися.

**Задача виконана:** Так. Команда `python manage.py test api` виконала 28
тестів; усі тести пройшли, Django system check не виявив проблем.

### Що спрацювало, а що ні

Explicit scope constraints не дали Agent mode розширити локальну API-зміну
до моделей, міграцій, маршрутів або frontend. Перелік `Changes allowed`
також зафіксував очікувану валідацію і тести, тому несподіваних змін не
виникло. Ручних виправлень після реалізації та запуску тестів не
знадобилося.
