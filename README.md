# 👷 Test-task-projement

Репозиторий для выполнения тестового задания в котором требуется модифицировать
существующий legacy-проект.

**_ВАЖНО_** - это **legacy-проект**, работающий корректно с интерпретаторами 
Python от 3.0 до 3.6 включительно. 

## Installing

Перед **первым** запуском приложения необходимо:

1. Установить зависимости из `requirements.txt`

2. Провести миграции БД
    ```console
    python manage.py migrate
    ```
3. Создать суперпользователя
   ```console
   python manage.py createsuperuser
   ```

Для корректной работы приложения необходимо запустить несколько служб:

1. Продюсер приложения (сервер Redis)
   ```console
   docker run -p 6379:6379 --name projement-redis -d redis
   ```

2. Брокер (celery)
   ```console
   source runcelery.sh
   ```
   **_или_**
   ```console
   celery -A projement  worker --loglevel=INFO
   ```

3. Потребитель (django приложение)
   ```console
   python manage.py runserver
   ```

_Примечание_ - все команды приведены с учётом того, что рабочей
директорией является `projement`.

## ToDo

1. Перевести проект на более строгую БД (например postgresql).
2. Произвести обновление django.
3. Улучшить информативность в шаблоне обновление времён проекта.
4. Заменить работу с модулем `os` на работу с `pathlib`.
5. Написать единый скрипт запуска проекта с пробросом констант через окружение.
6. Добавить в CI/CD при работе с master-веткой.
7. Упорядочить проекты при выгрузке в файл.

## Task text

<details>
<summary>
   <strong>
      <a>Формулировка задания</a>
   </strong>
</summary>

## Project overview

Projement is a simplified tool for project managers. Project managers can have
an overview of all the projects in a company.
This includes estimated and actual hours spent on *design*, *development* and *testing*.

**Make sure to read through the whole assignment before you start writing your solutions.**
**The last tasks might be more complicated than the first ones and depending on the implementation they might be related
to each other.**

Please use the best practices known to you to make the commits and manage branches in the repository.

### Setup

Use `Python 3` for back-end

All the requirements have been described in `requirements.txt`.
Make sure you add all your back-end requirements there as well!
Initial requirements include:

- [Django](https://docs.djangoproject.com/en/1.11/) as the base framework
- [django-crispy-forms](http://django-crispy-forms.readthedocs.io/en/latest/) for easier form layouts
- [markdown](http://pythonhosted.org/Markdown/siteindex.html) for rendering markdown in HTML

The application uses SQLite for the database by default.
You can override it in the settings - make sure to document it somehow if needed!

Migrate the database before the first run

    python manage.py migrate

Create a superuser

    python manage.py createsuperuser

Loading initial data for projects

    python manage.py loaddata projects/fixtures/initial.json

### Running the application

    python manage.py runserver

The application should be visible at `127.0.0.1:8000` after that

## Tasks

If you have any issues or questions about the task then mark them as TODOs
in comments and figure out the best solution yourself.

### 1. Fix project ordering on dashboard | ☑

Currently the projects on the dashboard are ordered by start date.

**Make the projects ordered by end date (descending) so that the projects that have not ended yet are shown first.**

### 2. Improve the admin for project detail view | ☑

Currently in the admin interface it is possible to filter the projects by company
name not the company instance in the database.
Because of that it is impossible to filter out the projects of one specific
company if there are multiple companies with the same name.

Please fix it - **make it possible to filter projects by actual companies in the database (company name should still be
visible in the filter options)**

### 3. Actual hours need to be decimals | ☑

Currently all the actual hours (design, development, testing) for the *Project*
model are in integers, but they need to be decimals.

**Change the actual hours to `DecimalField`s and make all the other necessary changes (e.g. migrations) to keep the
application running.**

All the actual hours should be in the range of `0 <= x < 10000` and have 2 decimal places.

### 4. Incremental changes | ☑

When two people are editing the same project at the same time and want
to increase the actual development hours by 10, then it results in faulty data.
For example, if the actual hours of development is currently 25 in a project
and two users are starting to edit the form then the initial value in the form is 25.
They both increase it by 10 and insert 35 as the development hours.
After submitting the form the actual development hours are 35, even though both
developers wanted to increase it by 10 and the resulting value should have been 45 (25+10+10).

**Please change the logic so that instead of entering the total amount of actual hours, the designers, developers and
testers have to enter the hours incrementally.**

### 5. Design and implement the history of the changes | ☑

Currently all the users can edit the actual hours of a project and no history
of the changes is left behind.
We should be able to see which user and when did the change. The information
about the initial value, change delta and resulting value should also be easily accessible.
If more than one of the actual hours (e.g. design and development hours for a project)
are changed at the same time, then they should be recognizable as one change.

**Please change the project structure so that the required history is stored in the database.**

It should be possible to view and filter the changes in a simple way in the future.
No changes nor logs should be created if none of the actual hours changed.
You don't have to implement any new views, just make sure that they are easy
to create when needed and the initially implemented logic (including the form) works.

There are no requirements of how you should represent the data that was entered
before the architectural changes, just make sure that the previously entered data is not lost!

### 6. Add tags to the projects | ☑

Tags are model instances that are **shared between projects** and have only
the title field (max 16 characters). They should be easily editable in the admin.

Each project can have `0..*` tags attached to it. We also need to know
**when was each tag attached to the project**.
Tags for one specific project should be easily editable in the admin.

You don't currently have to show the tags on dashboard nor the edit
form (of course you could do it ;)

### 7. Excel | ☑

**Make it possible to download a simple summary of projects in `.xls` format.**

It can be just a simple button on dashboard and have the same content as the table there.

### 8. Fix and write tests| ☑

You have probably broken some of the tests while implementing the previous changes.

**Please fix the tests and write some new ones to prove that everything works.**

### 9. Improve the code (optional)| ☑

You might have had some good ideas how to improve the project - either on the
architectural side or just the basic back-end implementation and code.
Feel free to document the improvements that you would make (e.g. in README.md as TODO-s)
and implement the changes if you still have some free time.
</details>
