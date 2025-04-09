from random import randint, choice
import faker
import psycopg2

NUMBER_USERS = 30
NUMBER_TASKS = 50

def generate_fake_data(number_users, number_tasks):
    fake_data = faker.Faker()

    fake_users = []
    for _ in range(number_users):
        fullname = fake_data.name()
        email = fake_data.email()
        fake_users.append((fullname, email))

    statuses = ['new', 'in progress', 'completed']
    fake_tasks = []
    for _ in range(number_tasks):
        title = fake_data.sentence(nb_words=5)
        description = fake_data.text(max_nb_chars=200)
        status = choice(statuses)
        fake_tasks.append((title, description, status))

    return fake_users, fake_tasks

def insert_data_to_db(fake_users, fake_tasks):
    try:
        # Підключення до нової бази даних
        connection = psycopg2.connect(
            dbname="my1_new_db",  # Тепер ми підключаємось до нової бази даних
            user="jurek", 
            password="password", 
            host="localhost", 
            port="5432"
        )
        cursor = connection.cursor()

        # Вставка користувачів
        user_insert_query = """INSERT INTO users (fullname, email) VALUES (%s, %s)"""
        cursor.executemany(user_insert_query, fake_users)
        connection.commit()

        # Вставка статусів
        status_insert_query = """INSERT INTO status (name) VALUES (%s)"""
        cursor.executemany(status_insert_query, [('new',), ('in progress',), ('completed',)])
        connection.commit()

        # Вставка завдань
        task_insert_query = """INSERT INTO tasks (title, description, status_id, user_id) 
                               VALUES (%s, %s, (SELECT id FROM status WHERE name = %s LIMIT 1), 
                                       (SELECT id FROM users WHERE email = %s LIMIT 1))"""
        for task in fake_tasks:
            title, description, status = task
            user_email = choice(fake_users)[1]  # Вибір випадкового користувача
            cursor.execute(task_insert_query, (title, description, status, user_email))

        connection.commit()
        print("Дані успішно вставлено в базу даних!")
    except Exception as e:
        print("Помилка при вставці даних в базу:", e)
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    fake_users, fake_tasks = generate_fake_data(NUMBER_USERS, NUMBER_TASKS)
    insert_data_to_db(fake_users, fake_tasks)

