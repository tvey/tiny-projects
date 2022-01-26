# These are tiny

## Contents

* [Full Text Search](#full-text-search)

* [Google Books Explorer](#google-books-explorer)

* [Hey FastAPI](#hey-fastapi)

* [Hey Sanic](#hey-sanic)

* [Simply Todo List](#simply-todo-list)

* [STL-Flask](#stl-flask)

* [Tiny Flask](#tiny-flask)

## Full Text Search

Thanks to [`django.contrib.postgres.search`](https://docs.djangoproject.com/en/4.0/ref/contrib/postgres/search/) module we can easily use PostgreSQL’s full text search functionality.

Classes such as `SearchVector` and `SearchRank` allow to narrow down fields and pick the most relevant results from a queryset.

[django-full-text-search.herokuapp.com/](https://django-full-text-search.herokuapp.com/)

## Google Books Explorer

There is Django calling Google Books API on the backend and returning its json responses.
And there is Vue from cdn accepting queries and displaying fetched results.

## Hey FastAPI

A FastAPI CRUD example with [SQLModel](https://github.com/tiangolo/sqlmodel).

## Hey Sanic

Basic Sanic CRUD with MongoDB using a sanic-motor wrapper.

## Simply Todo List

Rethinking [a small app on Django](https://github.com/tvey/simply-todo-list) using pure Javascript and LocalStorage.

The app allows to add, edit, delete, copy and sort (on desktop) items.

Works on Netlify: [https://simply-todo-list.netlify.app/](https://simply-todo-list.netlify.app/)

## STL-Flask

The same old to-do list with a backend switched from Django to Flask just for the sake of trying.
Authentication and CRUD are in place, other features omitted.

Works on Heroku: [https://stlf.herokuapp.com/](https://stlf.herokuapp.com/)

## Tiny Flask

Dockerized web app with Nginx. Build images locally with Nginx listening on port 8000

```bash
bash run-compose.sh
```

or compose with premade images and with Nginx on port 80

```bash
bash run-prod-compose.sh
```
