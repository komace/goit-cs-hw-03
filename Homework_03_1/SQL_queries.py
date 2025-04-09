import psycopg2

def create_connection():
    return psycopg2.connect(
        dbname="my1_new_db",  # Ваша база даних
        user="jurek",  # Ваше ім'я користувача
        password="password",  # Ваш пароль
        host="localhost",
        port="5432"
    )

# Функція для запису результатів у файл
def write_to_file(content):
    with open("results.txt", "a") as f:  # Відкриваємо файл для додавання
        f.write(content + "\n")
        
# 1. Отримати всі завдання певного користувача
def get_user_tasks(user_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks WHERE user_id = %s;", (user_id,))
    tasks = cursor.fetchall()
    write_to_file("Завдання користувача:")
    for task in tasks:
        write_to_file(str(task))
    cursor.close()
    connection.close()

# 2. Вибрати завдання за певним статусом
def get_tasks_by_status(status_name):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * 
        FROM tasks 
        WHERE status_id = (SELECT id FROM status WHERE name = %s);
    """, (status_name,))
    tasks = cursor.fetchall()
    write_to_file(f"Завдання зі статусом '{status_name}':")
    for task in tasks:
        write_to_file(str(task))
    cursor.close()
    connection.close()

# 3. Оновити статус конкретного завдання
def update_task_status(task_id, new_status):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE tasks 
        SET status_id = (SELECT id FROM status WHERE name = %s)
        WHERE id = %s;
    """, (new_status, task_id))
    connection.commit()
    write_to_file(f"Статус завдання з ID {task_id} оновлено на '{new_status}'.")
    cursor.close()
    connection.close()

# 4. Отримати список користувачів, які не мають жодного завдання
def get_users_without_tasks():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * 
        FROM users 
        WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks);
    """)
    users = cursor.fetchall()
    write_to_file("Користувачі без завдань:")
    for user in users:
        write_to_file(str(user))
    cursor.close()
    connection.close()

# 5. Додати нове завдання для конкретного користувача
def add_task(user_id, title, description, status_name):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO tasks (title, description, status_id, user_id)
        VALUES (%s, %s, (SELECT id FROM status WHERE name = %s), %s);
    """, (title, description, status_name, user_id))
    connection.commit()
    write_to_file(f"Завдання '{title}' додано для користувача з ID {user_id}.")
    cursor.close()
    connection.close()

# 6. Отримати всі завдання, які ще не завершено
def get_incomplete_tasks():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * 
        FROM tasks 
        WHERE status_id != (SELECT id FROM status WHERE name = 'completed');
    """)
    tasks = cursor.fetchall()
    write_to_file("Незавершені завдання:")
    for task in tasks:
        write_to_file(str(task))
    cursor.close()
    connection.close()

# 7. Видалити конкретне завдання
def delete_task(task_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
    connection.commit()
    write_to_file(f"Завдання з ID {task_id} видалено.")
    cursor.close()
    connection.close()

# 8. Знайти користувачів з певною електронною поштою
def get_users_by_email(email_pattern):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * 
        FROM users 
        WHERE email LIKE %s;
    """, (email_pattern,))
    users = cursor.fetchall()
    write_to_file(f"Користувачі з електронною поштою, що містить '{email_pattern}':")
    for user in users:
        write_to_file(str(user))
    cursor.close()
    connection.close()

# 9. Оновити ім'я користувача
def update_user_name(user_id, new_name):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE users 
        SET fullname = %s 
        WHERE id = %s;
    """, (new_name, user_id))
    connection.commit()
    write_to_file(f"Ім'я користувача з ID {user_id} оновлено на '{new_name}'.")
    cursor.close()
    connection.close()

# 10. Отримати кількість завдань для кожного статусу
def get_task_count_by_status():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT status_id, COUNT(*) 
        FROM tasks 
        GROUP BY status_id;
    """)
    counts = cursor.fetchall()
    write_to_file("Кількість завдань за статусами:")
    for count in counts:
        write_to_file(f"Статус ID {count[0]}: {count[1]} завдань")
    cursor.close()
    connection.close()

# 11. Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
def get_tasks_by_email_domain(domain):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT tasks.* 
        FROM tasks 
        JOIN users ON tasks.user_id = users.id
        WHERE users.email LIKE %s;
    """, (f"%{domain}%",))
    tasks = cursor.fetchall()
    write_to_file(f"Завдання, призначені користувачам з електронною поштою, що містить '{domain}':")
    for task in tasks:
        write_to_file(str(task))
    cursor.close()
    connection.close()

# 12. Отримати список завдань, що не мають опису
def get_tasks_without_description():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks WHERE description IS NULL OR description = '';")
    tasks = cursor.fetchall()
    write_to_file("Завдання без опису:")
    for task in tasks:
        write_to_file(str(task))
    cursor.close()
    connection.close()

# 13. Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
def get_users_in_progress_tasks():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT users.*, tasks.* 
        FROM users 
        INNER JOIN tasks ON users.id = tasks.user_id
        WHERE tasks.status_id = (SELECT id FROM status WHERE name = 'in progress');
    """)
    result = cursor.fetchall()
    write_to_file("Користувачі та їхні завдання у статусі 'in progress':")
    for row in result:
        write_to_file(str(row))
    cursor.close()
    connection.close()

# 14. Отримати користувачів та кількість їхніх завдань
def get_users_task_count():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT users.id, users.fullname, COUNT(tasks.id) 
        FROM users 
        LEFT JOIN tasks ON users.id = tasks.user_id 
        GROUP BY users.id;
    """)
    result = cursor.fetchall()
    write_to_file("Користувачі та кількість їхніх завдань:")
    for row in result:
        write_to_file(f"Користувач: {row[1]}, Завдань: {row[2]}")
    cursor.close()
    connection.close()

# Виконання всіх запитів
if __name__ == "__main__":
    write_to_file("Результати виконання запитів:\n")
    get_user_tasks(18)  # Завдання користувача з ID = 18
    get_tasks_by_status('new')  # Завдання зі статусом 'new'
    update_task_status(1, 'in progress')  # Оновити статус завдання з ID = 1 на 'in progress'
    get_users_without_tasks()  # Користувачі без завдань
    add_task(1, 'New Task', 'Task description', 'new')  # Додати нове завдання
    get_incomplete_tasks()  # Незавершені завдання
    delete_task(1)  # Видалити завдання з ID = 1
    get_users_by_email('%example.com')  # Користувачі з email, що містять 'example.com'
    update_user_name(1, 'New Name')  # Оновити ім'я користувача з ID = 1
    get_task_count_by_status()  # Кількість завдань за статусами
    get_tasks_by_email_domain('example.com')  # Завдання користувачів з email доменом 'example.com'
    get_tasks_without_description()  # Завдання без опису
    get_users_in_progress_tasks()  # Користувачі та їхні завдання у статусі 'in progress'
    get_users_task_count()  # Користувачі та кількість їхніх завдань
