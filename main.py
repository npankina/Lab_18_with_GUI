import tkinter as tk
from tkinter import ttk, messagebox

from db_operations import get_all_customers, add_customer, delete_customer, get_all_orders, get_order_details, \
    add_product, search_orders, search_customers, get_all_products, read_logs


# Функция для загрузки и отображения клиентов из БД
def load_customers():
    customers, error = get_all_customers()
    if error:
        messagebox.showerror("Ошибка", error)
    else:
        # Очищаем таблицу перед добавлением новых данных
        for row in tree_customers.get_children():
            tree_customers.delete(row)

        # Добавляем клиентов в таблицу
        for customer in customers:
            tree_customers.insert('', 'end', values=customer)


# Функция для добавления клиента через интерфейс
def add_customer_interface():
    company_name = entry_company_name.get()
    phone = entry_phone.get()
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    city = entry_city.get()
    street = entry_street.get()
    building = entry_building.get()

    if company_name and phone and first_name and last_name and city and street and building:
        # Здесь необходимо передать данные для создания клиента в базу данных (например, в db_operations.py)
        result = add_customer(company_name, phone, first_name, last_name, city, street, building)
        if "Ошибка" in result:
            messagebox.showerror("Ошибка", result)
        else:
            messagebox.showinfo("Успех", result)
            entry_company_name.delete(0, tk.END)
            entry_phone.delete(0, tk.END)
            entry_first_name.delete(0, tk.END)
            entry_last_name.delete(0, tk.END)
            entry_city.delete(0, tk.END)
            entry_street.delete(0, tk.END)
            entry_building.delete(0, tk.END)
    else:
        messagebox.showerror("Ошибка", "Заполните все поля")


# Создаем функцию, которая будет вызываться при нажатии кнопки
def fetch_products():
    products, error = get_all_products()
    if error:
        messagebox.showerror("Ошибка", error)
    else:
        # Очищаем таблицу перед добавлением новых товаров
        for row in tree_products.get_children():
            tree_products.delete(row)

        # Добавляем полученные товары в таблицу
        for product in products:
            tree_products.insert('', 'end', values=product)


# Функция для чтения и отображения логов в интерфейсе
def load_logs_interface():
    logs = read_logs()

    # Очищаем старые записи
    for row in tree_logs.get_children():
        tree_logs.delete(row)

    # Добавляем новые логи в таблицу, включая детали
    for log in logs:
        # log = (log_id, customer_id, operation, log_date, details)
        tree_logs.insert('', 'end', values=log)


# Функция для поиска клиентов через интерфейс
def search_customers_interface():
    search_query = entry_search.get()
    if search_query:
        customers, error = search_customers(search_query)
        if error:
            messagebox.showerror("Ошибка", error)
        else:
            # Очищаем таблицу перед добавлением результатов поиска
            for row in tree_customers.get_children():
                tree_customers.delete(row)
            # Добавляем результаты поиска в таблицу
            for customer in customers:
                tree_customers.insert('', 'end', values=customer)
    else:
        messagebox.showerror("Ошибка", "Введите поисковый запрос")


# Функция для удаления клиента через интерфейс
def delete_customer_interface():
    customer_id = entry_customer_id.get()
    if customer_id:
        result = delete_customer(customer_id)
        if "Ошибка" in result:
            messagebox.showerror("Ошибка", result)
        else:
            messagebox.showinfo("Успех", result)
            entry_customer_id.delete(0, tk.END)
            show_all_orders_interface()  # Обновляем список заказов после удаления клиента
    else:
        messagebox.showerror("Ошибка", "Введите ID клиента для удаления")


# Функция для загрузки и отображения заказов из БД
def load_orders():
    orders, error = get_all_orders()
    if error:
        messagebox.showerror("Ошибка", error)
    else:
        # Очищаем таблицу перед добавлением новых данных
        for row in tree_orders.get_children():
            tree_orders.delete(row)

        # Добавляем заказы в таблицу
        for order in orders:
            tree_orders.insert('', 'end', values=order)


# Функция для отображения всех заказов
def show_all_orders_interface():
    orders, error = get_all_orders()
    if error:
        messagebox.showerror("Ошибка", error)
    else:
        # Очищаем таблицу заказов перед добавлением новых данных
        for row in tree_orders.get_children():
            tree_orders.delete(row)
        # Добавляем заказы в таблицу
        for order in orders:
            tree_orders.insert('', 'end', values=order)


# Функция для отображения деталей выбранного заказа
def show_order_details(event):
    selected_item = tree_orders.focus()
    if selected_item:
        order_id = tree_orders.item(selected_item)['values'][0]
        order_details, error = get_order_details(order_id)
        if error:
            messagebox.showerror("Ошибка", error)
        else:
            # Очищаем таблицу деталей заказа
            for row in tree_order_details.get_children():
                tree_order_details.delete(row)
            # Добавляем детали заказа
            for item in order_details:
                tree_order_details.insert('', 'end', values=item)


# Функция для добавления товара через интерфейс
def add_product_interface():
    author = entry_author.get()
    title = entry_title.get()
    year_of_publication = entry_year_of_publication.get()
    price = entry_price.get()
    description = entry_description.get()
    delivery = delivery_var.get()  # Переменная для состояния доставки

    # Проверяем обязательные поля
    if not author or not title or not price:
        messagebox.showerror("Ошибка", "Заполните обязательные поля: автор, наименование, цена")
        return

    try:
        # Преобразование цены в число
        price = float(price)
    except ValueError:
        messagebox.showerror("Ошибка", "Цена должна быть числом")
        return

    try:
        # Преобразование года в целое число
        if year_of_publication:
            year_of_publication = int(year_of_publication)
        else:
            year_of_publication = None  # Если год не указан
    except ValueError:
        messagebox.showerror("Ошибка", "Год издания должен быть числом")
        return

    # Вызов функции для добавления товара в базу данных
    result = add_product(author, title, year_of_publication, price, description, delivery)
    if "Ошибка" in result:
        messagebox.showerror("Ошибка", result)
    else:
        messagebox.showinfo("Успех", "Товар успешно добавлен")
        # Очистка полей после добавления
        entry_author.delete(0, tk.END)
        entry_title.delete(0, tk.END)
        entry_year_of_publication.delete(0, tk.END)
        entry_price.delete(0, tk.END)
        entry_description.delete(0, tk.END)

# Функция для поиска заказов через интерфейс
def search_orders_interface():
    search_query = entry_search_orders.get()
    if search_query:
        orders, error = search_orders(search_query)
        if error:
            messagebox.showerror("Ошибка", error)
        else:
            # Очищаем таблицу перед добавлением результатов поиска
            for row in tree_orders.get_children():
                tree_orders.delete(row)
            # Добавляем результаты поиска в таблицу
            for order in orders:
                tree_orders.insert('', 'end', values=order)
    else:
        messagebox.showerror("Ошибка", "Введите поисковый запрос")


### Создание основного окна приложения ###
root = tk.Tk()
root.title("Управление клиентами, заказами и товарами")
root.geometry("1100x800")

# Создание вкладок для разделения функционала
tab_control = ttk.Notebook(root)

# Вкладка для управления клиентами
tab_customers = ttk.Frame(tab_control)
tab_control.add(tab_customers, text='Клиенты')

# Вкладка для управления заказами
tab_orders = ttk.Frame(tab_control)
tab_control.add(tab_orders, text='Заказы')

# Вкладка для управления товарами
tab_products = ttk.Frame(tab_control)
tab_control.add(tab_products, text='Товары')

# Вкладка для просмотра логов
tab_logs = ttk.Frame(tab_control)
tab_control.add(tab_logs, text='Логи')

tab_control.pack(expand=1, fill='both')

### Разделение вкладки Клиенты ###

# Поля ввода для добавления клиента
frame_add_customer = ttk.LabelFrame(tab_customers, text="Добавить клиента")
frame_add_customer.pack(fill="x", padx=10, pady=5)

# Поля для названия компании и телефона (эти уже есть)
label_company_name = ttk.Label(frame_add_customer, text="Название компании:")
label_company_name.grid(row=0, column=0, padx=5, pady=5, sticky='e')

entry_company_name = ttk.Entry(frame_add_customer, width=30)
entry_company_name.grid(row=0, column=1, padx=5, pady=5)

label_phone = ttk.Label(frame_add_customer, text="Телефон:")
label_phone.grid(row=1, column=0, padx=5, pady=5, sticky='e')

entry_phone = ttk.Entry(frame_add_customer, width=30)
entry_phone.grid(row=1, column=1, padx=5, pady=5)

# Поля для контактного лица (Имя и Фамилия)
label_first_name = ttk.Label(frame_add_customer, text="Имя контактного лица:")
label_first_name.grid(row=2, column=0, padx=5, pady=5, sticky='e')

entry_first_name = ttk.Entry(frame_add_customer, width=30)
entry_first_name.grid(row=2, column=1, padx=5, pady=5)

label_last_name = ttk.Label(frame_add_customer, text="Фамилия контактного лица:")
label_last_name.grid(row=3, column=0, padx=5, pady=5, sticky='e')

entry_last_name = ttk.Entry(frame_add_customer, width=30)
entry_last_name.grid(row=3, column=1, padx=5, pady=5)


# Поля для контактного лица
label_first_name = ttk.Label(frame_add_customer, text="Имя контактного лица:")
label_first_name.grid(row=2, column=0, padx=5, pady=5, sticky='e')

entry_first_name = ttk.Entry(frame_add_customer, width=30)
entry_first_name.grid(row=2, column=1, padx=5, pady=5)

label_last_name = ttk.Label(frame_add_customer, text="Фамилия контактного лица:")
label_last_name.grid(row=3, column=0, padx=5, pady=5, sticky='e')

entry_last_name = ttk.Entry(frame_add_customer, width=30)
entry_last_name.grid(row=3, column=1, padx=5, pady=5)

# Поля для адреса
label_city = ttk.Label(frame_add_customer, text="Город:")
label_city.grid(row=4, column=0, padx=5, pady=5, sticky='e')

entry_city = ttk.Entry(frame_add_customer, width=30)
entry_city.grid(row=4, column=1, padx=5, pady=5)

label_street = ttk.Label(frame_add_customer, text="Улица:")
label_street.grid(row=5, column=0, padx=5, pady=5, sticky='e')

entry_street = ttk.Entry(frame_add_customer, width=30)
entry_street.grid(row=5, column=1, padx=5, pady=5)

label_building = ttk.Label(frame_add_customer, text="Здание:")
label_building.grid(row=6, column=0, padx=5, pady=5, sticky='e')

entry_building = ttk.Entry(frame_add_customer, width=30)
entry_building.grid(row=6, column=1, padx=5, pady=5)

button_add_customer = ttk.Button(frame_add_customer, text="Добавить клиента", command=add_customer_interface)
button_add_customer.grid(row=7, column=0, columnspan=2, pady=10)


# Поле для поиска клиентов
frame_search_customer = ttk.LabelFrame(tab_customers, text="Поиск клиентов")
frame_search_customer.pack(fill="x", padx=10, pady=5)

entry_search = ttk.Entry(frame_search_customer, width=50)
entry_search.grid(row=0, column=0, padx=5, pady=5)

button_search = ttk.Button(frame_search_customer, text="Поиск клиентов", command=search_customers_interface)
button_search.grid(row=0, column=1, padx=5, pady=5)

# Добавляем кнопку для получения клиентов
button_load_customers = ttk.Button(tab_customers, text="Выгрузить клиентов", command=load_customers)
button_load_customers.pack(padx=10, pady=5)

# Таблица для отображения клиентов
frame_table_customers = ttk.Frame(tab_customers)
frame_table_customers.pack(fill="both", expand=True, padx=10, pady=5)

# Добавляем колонки для отображения имени и фамилии контактного лица
columns_customers = ("ID", "Название компании", "Телефон", "Имя контактного лица", "Фамилия контактного лица")
tree_customers = ttk.Treeview(frame_table_customers, columns=columns_customers, show="headings")
for col in columns_customers:
    tree_customers.heading(col, text=col)
    tree_customers.column(col, width=150, anchor='center')

tree_customers.pack(fill="both", expand=True)

# # Привязываем действие к выбору клиента в таблице
# tree_customers.bind("<<TreeviewSelect>>", lambda event: show_customer_details())

# Поле для удаления клиента
frame_delete_customer = ttk.LabelFrame(tab_customers, text="Удалить клиента")
frame_delete_customer.pack(fill="x", padx=10, pady=5)

label_customer_id = ttk.Label(frame_delete_customer, text="ID клиента для удаления:")
label_customer_id.grid(row=0, column=0, padx=5, pady=5, sticky='e')

entry_customer_id = ttk.Entry(frame_delete_customer, width=30)
entry_customer_id.grid(row=0, column=1, padx=5, pady=5)

button_delete_customer = ttk.Button(frame_delete_customer, text="Удалить клиента", command=delete_customer_interface)
button_delete_customer.grid(row=1, column=0, columnspan=2, pady=10)


### Добавление элементов во вкладку "Заказы" ###

# Поле для поиска заказов
frame_search_orders = ttk.LabelFrame(tab_orders, text="Поиск заказов")
frame_search_orders.pack(fill="x", padx=10, pady=5)

entry_search_orders = ttk.Entry(frame_search_orders, width=50)
entry_search_orders.grid(row=0, column=0, padx=5, pady=5)

button_search_orders = ttk.Button(frame_search_orders, text="Поиск заказов", command=search_orders_interface)
button_search_orders.grid(row=0, column=1, padx=5, pady=5)

# Добавляем кнопку для получения заказов
button_load_orders = ttk.Button(tab_orders, text="Выгрузить заказы", command=load_orders)
button_load_orders.pack(padx=10, pady=5)

# Таблица для отображения заказов
frame_orders = ttk.LabelFrame(tab_orders, text="Список заказов")
frame_orders.pack(fill="both", expand=True, padx=10, pady=5)

columns_orders = ("ID", "Клиент", "Дата заказа", "Сумма заказа", "Статус")
tree_orders = ttk.Treeview(frame_orders, columns=columns_orders, show="headings")
for col in columns_orders:
    tree_orders.heading(col, text=col)
    tree_orders.column(col, width=150, anchor='center')

tree_orders.pack(fill="both", expand=True)
tree_orders.bind("<<TreeviewSelect>>", show_order_details)

# Таблица для отображения деталей заказа
frame_order_details = ttk.LabelFrame(tab_orders, text="Детали заказа")
frame_order_details.pack(fill="both", expand=True, padx=10, pady=5)

columns_order_details = ("ID", "Автор", "Название", "Год издания", "Количество", "Цена")
tree_order_details = ttk.Treeview(frame_order_details, columns=columns_order_details, show="headings")

for col in columns_order_details:
    tree_order_details.heading(col, text=col)
    tree_order_details.column(col, width=150, anchor='center')

tree_order_details.pack(fill="both", expand=True)

### Добавление элементов во вкладку "Товары" ###

# Поля ввода для добавления товара
frame_add_product = ttk.LabelFrame(tab_products, text="Добавить товар")
frame_add_product.pack(fill="x", padx=10, pady=5)

btn_fetch_products = ttk.Button(tab_products, text="Выгрузить товары", command=fetch_products)
btn_fetch_products.pack()

label_author = ttk.Label(frame_add_product, text="Автор:")
label_author.grid(row=0, column=0, padx=5, pady=5, sticky='e')

entry_author = ttk.Entry(frame_add_product, width=30)
entry_author.grid(row=0, column=1, padx=5, pady=5)

label_title = ttk.Label(frame_add_product, text="Наименование:")
label_title.grid(row=1, column=0, padx=5, pady=5, sticky='e')

entry_title = ttk.Entry(frame_add_product, width=30)
entry_title.grid(row=1, column=1, padx=5, pady=5)

label_year_of_publication = ttk.Label(frame_add_product, text="Год издания:")
label_year_of_publication.grid(row=2, column=0, padx=5, pady=5, sticky='e')

entry_year_of_publication = ttk.Entry(frame_add_product, width=30)
entry_year_of_publication.grid(row=2, column=1, padx=5, pady=5)

label_price = ttk.Label(frame_add_product, text="Цена:")
label_price.grid(row=3, column=0, padx=5, pady=5, sticky='e')

entry_price = ttk.Entry(frame_add_product, width=30)
entry_price.grid(row=3, column=1, padx=5, pady=5)

label_description = ttk.Label(frame_add_product, text="Описание:")
label_description.grid(row=4, column=0, padx=5, pady=5, sticky='e')

entry_description = ttk.Entry(frame_add_product, width=30)
entry_description.grid(row=4, column=1, padx=5, pady=5)

# # Поле для выбора доставки
# label_delivery = ttk.Label(frame_add_product, text="Доставка:")
# label_delivery.grid(row=5, column=0, padx=5, pady=5, sticky='e')
#
# delivery_var = tk.BooleanVar(value=False)  # Переменная для хранения состояния доставки (по умолчанию False)
# check_delivery = ttk.Checkbutton(frame_add_product, variable=delivery_var, text="Доступна доставка")
# check_delivery.grid(row=5, column=1, padx=5, pady=5)

# Кнопка для добавления товара
button_add_product = ttk.Button(frame_add_product, text="Добавить товар", command=add_product_interface)
button_add_product.grid(row=6, column=0, columnspan=2, pady=10)

# Таблица для отображения товаров
frame_table_products = ttk.Frame(tab_products)
frame_table_products.pack(fill="both", expand=True, padx=10, pady=5)

columns_products = ("ID", "Автор", "Наименование", "Год", "Цена", "Описание", "Доставка")
tree_products = ttk.Treeview(frame_table_products, columns=columns_products, show="headings")
for col in columns_products:
    tree_products.heading(col, text=col)
    tree_products.column(col, width=150, anchor='center')

tree_products.pack(fill="both", expand=True)

### Разделение вкладки Логи ###

# Таблица для отображения логов
frame_logs = ttk.LabelFrame(tab_logs, text="Логи приложения")
frame_logs.pack(fill="both", expand=True, padx=10, pady=5)

# Обновляем колонки для включения нового поля details
columns_logs = ("ID", "Клиент", "Операция", "Дата и время", "Детали")
tree_logs = ttk.Treeview(frame_logs, columns=columns_logs, show="headings")
for col in columns_logs:
    tree_logs.heading(col, text=col)
    tree_logs.column(col, width=150, anchor='center')

tree_logs.pack(fill="both", expand=True)

# Кнопка для загрузки логов
button_load_logs = ttk.Button(tab_logs, text="Загрузить логи", command=load_logs_interface)
button_load_logs.pack(pady=5)

if __name__ == '__main__':
    root.mainloop()
