from operator import ifloordiv

import psycopg2
import logging

# Настраиваем логгер
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Подключение к базе данных
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="lab_18",
            user="admin",
            password="0000",
            host="localhost"
        )
        logging.info("Подключение к базе данных выполнено успешно")
        return conn

    except Exception as e:
        logging.error(f"Ошибка подключения к базе данных: {e}")
        return None

# checked
def add_customer(company_name, phone, first_name, last_name, city, street, building):
    try:
        conn = connect_db()
        if conn is None:
            return "Ошибка подключения к базе данных"

        cursor = conn.cursor()
        # 1. Вставляем данные в таблицу Address и получаем address_id
        address_query = """
               INSERT INTO Address (city, street, building)
               VALUES (%s, %s, %s)
               RETURNING id;
               """
        cursor.execute( address_query,(city, street, building) )
        address_id = cursor.fetchone()[0]

        # 2. Вставляем данные в таблицу Customers с полученным address_id
        customer_query = """
        INSERT INTO Customers (company_name, address_id, phone, first_name, last_name)
        VALUES (%s, %s, %s, %s, %s);
        """
        cursor.execute(customer_query, (company_name, address_id, phone, first_name, last_name))
        conn.commit()
        logging.info(f"Клиент '{company_name}' добавлен успешно")
        return "Клиент добавлен!"

    except Exception as e:
        logging.error(f"Ошибка при добавлении клиента: {e}")
        return str(e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# checked
def search_customers(search_query):
    try:
        conn = connect_db()
        if conn is None:
            return None, "Ошибка подключения к базе данных"

        cursor = conn.cursor()
        query = "SELECT id, company_name, phone FROM Customers WHERE company_name ILIKE %s"
        cursor.execute(query, ('%' + search_query + '%',))
        customers = cursor.fetchall()

        logging.info(f"Найдено {len(customers)} клиентов по запросу: {search_query}")
        return customers, None

    except Exception as e:
        logging.error(f"Ошибка при поиске клиентов: {e}")
        return None, str(e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# checked
def delete_customer(customer_id):
    try:
        conn = connect_db()
        if conn is None:
            return "Ошибка подключения к базе данных"

        cursor = conn.cursor()
        cursor.execute("DELETE FROM Customers WHERE id = %s", (customer_id,))

        if cursor.rowcount == 0:
            return f"Клиент с id {customer_id} не найден!"

        conn.commit()
        logging.info(f"Клиент с ID {customer_id} удалён успешно")
        return "Клиент успешно удален!"

    except Exception as e:
        logging.error(f"Ошибка при удалении клиента с ID {customer_id}: {e}")
        return str(e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# checked
def get_all_customers():
    try:
        conn = connect_db()
        if conn is None:
            return None, "Ошибка подключения к базе данных"

        cursor = conn.cursor()
        query = "SELECT * FROM Customers;"
        cursor.execute(query)
        customers = cursor.fetchall()
        logging.info(f"Получено {len(customers)} покупателей")
        return customers, None

    except Exception as e:
        logging.error(f"Ошибка при получении списка покупателей: {e}")
        return None, str(e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# checked
def get_all_orders():
    try:
        conn = connect_db()
        if conn is None:
            return None, "Ошибка подключения к базе данных"

        cursor = conn.cursor()
        query = """
            SELECT Orders.id, Customers.company_name, Orders.order_date, Orders.total_amount, Orders.status
            FROM Orders
            JOIN Customers ON Orders.customer_id = Customers.id
            ORDER BY Orders.order_date 
        """
        cursor.execute(query)
        orders = cursor.fetchall()

        logging.info(f"Получено {len(orders)} заказов")
        return orders, None

    except Exception as e:
        logging.error(f"Ошибка при получении заказов: {e}")
        return None, str(e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


#
def get_order_details(order_id):
    try:
        conn = connect_db()
        if conn is None:
            return None, "Ошибка подключения к базе данных"
        cursor = conn.cursor()
        query = """
            SELECT Order_items.id, Products.description, Order_items.quantity, Order_items.price
            FROM Order_items
            JOIN Products ON Order_items.product_id = Products.id
            WHERE Order_items.order_id = %s
        """
        cursor.execute(query, (order_id,))
        order_items = cursor.fetchall()

        logging.info(f"Получено {len(order_items)} позиций для заказа ID {order_id}")
        return order_items, None
    except Exception as e:
        logging.error(f"Ошибка при получении деталей заказа ID {order_id}: {e}")
        return None, str(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Функция для добавления товара
def add_product(price, description, delivery):
    try:
        conn = connect_db()
        if conn is None:
            return "Ошибка подключения к базе данных"
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Products (price, description, delivery) VALUES (%s, %s, %s)",
            (price, description, delivery)
        )
        conn.commit()

        logging.info(f"Товар '{description}' добавлен успешно")
        return "Товар добавлен!"
    except Exception as e:
        logging.error(f"Ошибка при добавлении товара: {e}")
        return str(e)
    finally:
        if cursor:
            cursor.close()  # Закрываем курсор
        if conn:
            conn.close()  # Закрываем соединение


# Функция для поиска заказов по номеру или названию товара
def search_orders(search_query):
    try:
        conn = connect_db()
        if conn is None:
            return None, "Ошибка подключения к базе данных"

        cursor = conn.cursor()
        query = """
            SELECT Orders.id, Customers.company_name, Orders.order_date, Orders.total_amount, Orders.status
            FROM Orders
            JOIN Customers ON Orders.customer_id = Customers.id
            LEFT JOIN Order_items ON Orders.id = Order_items.order_id
            LEFT JOIN Products ON Order_items.product_id = Products.id
            WHERE Orders.id::text LIKE %s OR Products.description ILIKE %s
            ORDER BY Orders.order_date DESC
        """
        search_query = f"%{search_query}%"
        cursor.execute(query, (search_query, search_query))
        orders = cursor.fetchall()


        logging.info(f"Найдено {len(orders)} заказов по запросу: {search_query}")
        return orders, None
    except Exception as e:
        logging.error(f"Ошибка при поиске заказов: {e}")
        return None, str(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Функция для получения контактного лица клиента
def get_contact_person(customer_id):
    try:
        conn = connect_db()
        if conn is None:
            return None, "Ошибка подключения к базе данных"

        cursor = conn.cursor()
        query = """
            SELECT Contact.first_name, Contact.last_name 
            FROM Contact 
            JOIN Customers ON Customers.contact_person_id = Contact.id 
            WHERE Customers.id = %s
        """
        cursor.execute(query, (customer_id,))
        contact_person = cursor.fetchone()

        return contact_person, None
    except Exception as e:
        logging.error(f"Ошибка при получении контактного лица для клиента {customer_id}: {e}")
        return None, str(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Функция для получения адреса клиента
def get_address(customer_id):
    try:
        conn = connect_db()
        if conn is None:
            return None, "Ошибка подключения к базе данных"

        cursor = conn.cursor()
        query = """
            SELECT Cities.name, Streets.name, Address.building, Address.zip_code 
            FROM Address
            JOIN Customers ON Customers.address_id = Address.id
            JOIN Cities ON Address.city = Cities.id
            JOIN Streets ON Address.street = Streets.id
            WHERE Customers.id = %s
        """
        cursor.execute(query, (customer_id,))
        address = cursor.fetchone()

        return address, None
    except Exception as e:
        logging.error(f"Ошибка при получении адреса для клиента {customer_id}: {e}")
        return None, str(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Функция для чтения логов из файла
def read_logs():
    try:
        conn = connect_db()
        if conn is None:
            return None, "Ошибка подключения к базе данных"

        cursor = conn.cursor()

        # Обновляем запрос для извлечения нового поля details
        query = """
        SELECT log_id, customer_id, log_date, details
        FROM Customer_Activity_Log
        ORDER BY log_date DESC;
        """
        cursor.execute(query)
        logs = cursor.fetchall()

        return logs

    except Exception as e:
        return str(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()