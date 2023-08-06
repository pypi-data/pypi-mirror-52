
# -*- coding: utf-8 -*-
"""
"""

from flasik.cli import (command, option, argument, click)
from flasik import db, models
import core
import nltk
import schedule
import time
import logging

logging.basicConfig(level=logging.INFO)

@command("news:setup")
def setup():
    """ Setup Newsroom """
    nltk.download('stopwords');


@command("news:worker:run-taskq")
def worker_run():
    """ Worker: Run Task Queues """
    logging.info("news:worker:run-taskq")
    models.NewsroomTaskQueue.run()


@command("news:worker:import-sources")
def worker_import_sources():
    """ Worker: Import sources """
    pause = 1  # in minutes
    while True:
        logging.info("Worker: importing sources...")
        core.import_sources()
        time.sleep(pause * 60)

# @command("news:fetch-sources")
def fetch_sources():
    core.import_sources()


@command("news:add-source")
def add_source():
    """ To add new source """
    print("Adding new source")
    type_ = click.prompt("Type (rss|youtube_channel|page_links)")
    name = click.prompt("Name")
    url = click.prompt("Url/Channel")
    page_links_selector = None
    if type_ == "page_links":
        page_links_selector = click.prompt("Page links selector")
    fetch_frequency = click.prompt(
        "Fetch frequency in minutes", type=int, default=60)
    limit = click.prompt("Fetch limit", type=int, default=10)
    if click.confirm('Do you want to continue?'):
        models.NewsroomSource.new(name=name,
                                  url=url,
                                  type=type_,
                                  page_links_selector=page_links_selector,
                                  fetch_frequency=fetch_frequency,
                                  limit=limit)
        print("New source added successfully!")


@command("news:admin:add-user")
def add_admin_user():
    """ Add new user """
    print("Add New User")
    name = click.prompt("Name")
    email = click.prompt("Login Email", confirmation_prompt=True)
    password = click.prompt("Login Password", confirmation_prompt=True, hide_input=True)

    email = email.strip()
    password = password.strip()
    try:
        user = models.NewsroomAuth.new(email=email, password=password, name=name)
        print("User created successfully!")
        print("ID: %s" % user.id)
        print("Login Email: %s" % email)
        print("Name: %s" % name)
    except Exception as e:
        print('ERROR: %s' % e)


@command("news:admin:list-users")
def add_admin_user():
    """ List Users """
    print("List Users")
    try:
        for user in models.NewsroomAuth.query():
            print("ID: %s | Email: %s  | Is Admin: %s | Is Active: %s" %
                  (user.id, user.email, user.is_admin, user.is_active))
    except Exception as e:
        print('ERROR: %s' % e)


@command("news:admin:change-admin-right")
def add_admin_user():
    """ Change User Admin Right """
    print("Change User Admin Right ")
    try:
        id = click.prompt("Enter User ID")
        is_val = click.prompt("IS Admin (1|0)", type=int, default=1)
        user = models.NewsroomAuth.get(id)
        if user:
            user.update(is_admin=is_val == 1)
            print("ID: %s | Email: %s  | Is Admin: %s | Is Active: %s" %
                  (user.id, user.email, user.is_admin, user.is_active))
        else:
            raise Exception("User '%s' not found" % id)
    except Exception as e:
        print('ERROR: %s' % e)


@command("news:admin:change-user-email")
def add_admin_user():
    """ Change User Email """
    print("Change User Email ")
    try:
        id = click.prompt("Enter User ID")
        email = click.prompt("Email")
        user = models.NewsroomAuth.get(id)
        if user:
            user.change_email(email)
            print("ID: %s | Email: %s  | Is Admin: %s | Is Active: %s" %
                  (user.id, user.email, user.is_admin, user.is_active))
        else:
            raise Exception("User '%s' not found" % id)
    except Exception as e:
        print('ERROR: %s' % e)


@command("news:admin:change-user-password")
def add_admin_user():
    """ Change User Password """
    print("Change User Password ")
    try:
        id = click.prompt("Enter User ID")
        password = click.prompt("Login Password", confirmation_prompt=True, hide_input=True)
        user = models.NewsroomAuth.get(id)
        if user:
            user.change_password(password)
            print("ID: %s | Email: %s  | Is Admin: %s | Is Active: %s" %
                  (user.id, user.email, user.is_admin, user.is_active))
        else:
            raise Exception("User '%s' not found" % id)
    except Exception as e:
        print('ERROR: %s' % e)


@command("news:admin:change-user-status")
def add_admin_user():
    """ Change User Active Status """
    print("Change User Active Status")
    try:
        id = click.prompt("Enter User ID")
        is_val = click.prompt("IS Active (1|0)", type=int, default=1)
        user = models.NewsroomAuth.get(id)
        if user:
            user.update(is_active=is_val == 1)
            print("ID: %s | Email: %s  | Is Admin: %s | Is Active: %s" %
                  (user.id, user.email, user.is_admin, user.is_active))
        else:
            raise Exception("User '%s' not found" % id)
    except Exception as e:
        print('ERROR: %s' % e)


@command("news:admin:delete-user")
def add_admin_user():
    """ Delete User """
    print("Delete User")
    try:
        id = click.prompt("Enter User ID")
        user = models.NewsroomAuth.get(id)
        if user and click.confirm("Do you really want to DELETE '%s'" % user.email):
            print("ID: %s | Email: %s  | Is Admin: %s | Is Active: %s" %
                  (user.id, user.email, user.is_admin, user.is_active))
            if click.confirm("LAST CHANCE: Do you really want to DELETE '%s'" % user.email):
                user.delete()
        else:
            raise Exception("User '%s' not found" % id)
    except Exception as e:
        print('ERROR: %s' % e)
