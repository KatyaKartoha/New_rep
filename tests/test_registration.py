import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    # Функция create_db() создает базу данных users.db и инициализирует схему
    create_db()
    yield
    # Очистка после выполнения тестов
    os.remove('users.db')

def test_create_db(setup_database):
    """Тест создания базы данных и таблицы пользователей."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Проверяем, существует ли таблица users
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

def test_add_existing_user(setup_database):
    first_try = add_user('admin', 'tsetyn@example.com', 'password123123')
    second_try = add_user('admin', 'tsety1@example.com', 'anotherpassword123')
    assert first_try == True, "Пользователь должен быть добавлен при первом добавлении."
    assert second_try == False, "Добавление пользователя с существующим логином должно вернуть False."

def test_authenticate_user(setup_database):
    add_user('testerr', 'testy@example.com', 'password123')
    authenticated = authenticate_user('testerr', 'password123')
    assert authenticated == True, "Должна быть успешная аутентификация с правильным логином и паролем."

def test_authenticate_nonexistent_user(setup_database):
    authenticated = authenticate_user('nonexistent', 'password123456')
    assert authenticated == False, "Должна быть неуспешная аутентификация."

def test_authenticate_user_wrong_password(setup_database):
    add_user('testerry', 'testy@example.com', 'password123')
    authenticated = authenticate_user('testerry', 'password1234590')
    assert authenticated == False, "Должна быть неуспешная аутентификация."

def test_list_show(setup_database):
    add_user('testuser', 'testuser@example.com', 'password123')
    add_user('testuser2', 'testuser2@example.com', 'password1234')
    add_user('testuser3', 'testuser3@example.com', 'password12345')
    display_users()
    print(display_users())
    b=[[i] for i in display_users()]
    assert len(b()) == 3, "Должно быть отображено 3" 


# Возможные варианты тестов:
"""
Тест добавления пользователя с существующим логином.
Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""