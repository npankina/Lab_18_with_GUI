from unittest import mock
from unittest.mock import mock_open

import pytest
from db_operations import add_customer, search_customers, delete_customer, get_all_customers, get_all_orders


@mock.patch('psycopg2.connect')
def test_add_customer(mock_connect):
    # Создаём мок-объекты для подключения и курсора
    mock_connection = mock.Mock()
    mock_cursor = mock.Mock()

    # Устанавливаем, что при вызове connect возвращается мок-соединение
    mock_connect.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor

    # id, возвращаемый из вставки в таблицу Address
    mock_cursor.fetchone.side_effect = [(1,)]

    # Вызываем тестируемую функцию
    result = add_customer(
        company_name="Test LLC",
        phone="+79991112233",
        first_name="Иван",
        last_name="Иванов",
        city="Санкт-Петербург",
        street="Серебристый бульвар",
        building="12"
    )

    # Проверка вызовов, не зависящая от форматирования SQL-запроса
    address_query_part = "INSERT INTO Address (city, street, building)"
    customer_query_part = "INSERT INTO Customers (company_name, address_id, phone, first_name, last_name)"

    # Проверяем, что запрос на добавление адреса содержит нужные части
    execute_calls = mock_cursor.execute.call_args_list
    address_query_found = any(address_query_part in call[0][0] for call in execute_calls)
    customer_query_found = any(customer_query_part in call[0][0] for call in execute_calls)

    assert address_query_found, "Запрос на вставку в таблицу Address не найден."
    assert customer_query_found, "Запрос на вставку в таблицу Customers не найден."

    # Проверяем, что вызов connection.commit() был произведён
    mock_connection.commit.assert_called_once()

    # Проверяем результат выполнения функции
    assert result == "Клиент добавлен!"

    # Проверяем, что курсор и соединение были закрыты
    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()



@mock.patch('psycopg2.connect')
def test_search_customers(mock_connect):
    mock_connection = mock.Mock()
    mock_cursor = mock.Mock()
    mock_connect.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, "ООО Пример", "+79991112233"),
        (2, "ИП Тест", "+79992223344")
    ]

    search_query = "Пример"
    customers, error = search_customers(search_query)

    mock_cursor.execute.assert_any_call(
        'SELECT id, company_name, phone FROM Customers WHERE company_name ILIKE %s',
        ('%' + search_query + '%',)
    )

    assert customers == [
        (1, "ООО Пример", "+79991112233"),
        (2, "ИП Тест", "+79992223344")
    ]
    assert error is None
    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()


@mock.patch('psycopg2.connect')
def test_search_customers_error(mock_connect):
    mock_connection = mock.Mock()
    mock_cursor = mock.Mock()
    mock_connect.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Ошибка запроса")

    search_query = "Ошибка"
    customers, error = search_customers(search_query)

    assert customers is None
    assert error == "Ошибка запроса"
    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()


@mock.patch('psycopg2.connect')
def test_delete_customer(mock_connect):
    mock_connection = mock.Mock()
    mock_cursor = mock.Mock()
    mock_connect.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 1
    result = delete_customer(customer_id=1)

    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM Customers WHERE id = %s", (1,)
    )

    mock_connection.commit.assert_called_once()
    assert result == "Клиент успешно удален!"

    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()



@mock.patch('psycopg2.connect')
def test_delete_customer_not_found(mock_connect):
    mock_connection = mock.Mock()
    mock_cursor = mock.Mock()
    mock_connect.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 0
    customer_id = 1
    result = delete_customer(customer_id)

    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM Customers WHERE id = %s", (1,)
    )

    mock_connection.commit.assert_not_called()
    assert result == f"Клиент с id {customer_id} не найден!"

    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()


@mock.patch('psycopg2.connect')
def test_delete_customer_error(mock_connect):
    mock_connection = mock.Mock()
    mock_cursor = mock.Mock()

    mock_connect.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor

    mock_cursor.execute.side_effect = Exception("Ошибка удаления")
    result = delete_customer(customer_id=1)
    assert "Ошибка удаления" in result

    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()


@mock.patch('psycopg2.connect')
def test_fetch_all_customers(mock_connect):
    mock_connection = mock.Mock()
    mock_cursor = mock.Mock()

    mock_connect.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, 'ООО Пример', 1, '+79991112233', 'Иван', 'Иванов'),
        (2, 'ИП Тест', 2, '+79992223344', 'Петр', 'Петров')
    ]
    customers, error = get_all_customers()
    mock_cursor.execute.assert_called_once_with("SELECT * FROM Customers;")

    assert customers == [
        (1, 'ООО Пример', 1, '+79991112233', 'Иван', 'Иванов'),
        (2, 'ИП Тест', 2, '+79992223344', 'Петр', 'Петров')
    ]
    assert error is None

    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()


@mock.patch('psycopg2.connect')
def test_fetch_all_customers_error(mock_connect):
    mock_connection = mock.Mock()
    mock_cursor = mock.Mock()

    mock_connect.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Ошибка выполнения запроса")

    customers, error = get_all_customers()

    assert customers is None
    assert error == "Ошибка выполнения запроса"

    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()


@mock.patch('psycopg2.connect')
def test_get_all_orders(mock_connect):
    mock_connection = mock.Mock()
    mock_cursor = mock.Mock()

    mock_connect.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, 'ООО Пример', '2024-09-24', 100.50, 'доставлен'),
        (2, 'ИП Тест', '2024-09-23', 50.00, 'отправлен')
    ]

    orders, error = get_all_orders()
    query_part = """
        SELECT Orders.id, Customers.company_name, Orders.order_date, Orders.total_amount, Orders.status
            FROM Orders
            JOIN Customers ON Orders.customer_id = Customers.id
            ORDER BY Orders.order_date DESC
    """.strip()

    execute_calls = mock_cursor.execute.call_args_list
    query_found = any(query_part in call[0][0] for call in execute_calls)
    assert query_found, "Запрос на выборку заказов не найден."

    assert orders == [
        (1, 'ООО Пример', '2024-09-24', 100.50, 'доставлен'),
        (2, 'ИП Тест', '2024-09-23', 50.00, 'отправлен')
    ]
    assert error is None

    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()


@mock.patch('psycopg2.connect')
def test_get_all_orders_connection_error(mock_connect):
    mock_connection = mock.Mock()
    mock_cursor = mock.Mock()

    mock_connect.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor

    mock_cursor.execute.side_effect = Exception("Ошибка подключения к базе данных")
    orders, error = get_all_orders()

    assert orders is None
    assert "Ошибка подключения к базе данных" in error

    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()


@mock.patch('psycopg2.connect')
def test_get_all_orders_query_error(mock_connect):
    mock_connection = mock.Mock()
    mock_cursor = mock.Mock()

    mock_connect.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor

    mock_cursor.execute.side_effect = Exception("Ошибка выполнения запроса")

    orders, error = get_all_orders()

    assert orders is None
    assert "Ошибка выполнения запроса" in error

    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()


@mock.patch('psycopg2.connect')
def test_get_order_details(mock_connect):
    mock_connection = mock.Mock()
    mock_cursor = mock.Mock()

    mock_connect.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor

