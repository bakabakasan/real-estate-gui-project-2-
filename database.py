import sqlite3 

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

#cursor.execute("""CREATE TABLE IF NOT EXISTS estate (
#      id integer primary key autoincrement, 
#      type text, 
#      location text, 
#     cost real, 
#      currency text, 
#      bedroom text, 
#     description text, 
#      additional_information text, 
#      area text, 
#      floor text)""")

all_estates = [
  ('Квартира', 'Минск, Беларусь', 90000, 'USD', 2, 'Квартира с отличной планировкой, с мебелью и бытовой техникой, полностью готова к проживанию. Есть телефон, охранная сигнализация. Три окна с видом на парк.', 'Возможно оформить в кредит.', '53 кв.м.', '3 этаж'),
  ('Квартира', 'Гродно, Беларусь', 30000, 'USD', 1, 'Уютная квартира в Гродно, в районе с развитой структурой. Рядом Вокзал и торговые центры, и остановки общественного транспорта.', '-', '32 кв.м.', '2 этаж'),
  ('Дом', 'Витебск, Беларусь', '', 'USD', 3, 'Двухэтажный коттедж с гаражом на две машины. Участок 18 соток. Подведены все коммуникации к дому. Сделана разводка всех коммуникаций по дому.', 'Возможна оплата в кредит.', '125 кв.м.', '2 этажа'),
  ('Дом', 'Полоцк, Беларусь', 100000, 'USD', 4, 'Дом расположен в живописном районе с развитой инфраструктурой. В районе имеется школа, сад, конный клуб, почта и продуктовые магазины.', '-', '96 кв.м.', '1 этаж')]

cursor.executemany("INSERT INTO estate VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", all_estates)

#cursor.execute("""CREATE TABLE IF NOT EXISTS messages (
#      id integer primary key autoincrement, 
#      full_name text, 
#      phone_number text, 
#      email text, 
#      message text, 
#      page_url text)""")

#cursor.execute("""CREATE TABLE IF NOT EXISTS users (
#      id integer primary key autoincrement, 
#      name text, 
#      email text, 
#      password)""")

#cursor.execute("SELECT * FROM estate")
#print(cursor.fetchall())

conn.commit()

conn.close()