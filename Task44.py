import random, os
import pandas as pd
import sqlite3 as sql
def Create_Table(table_name:str='Human_Language'):#создает таблицу с указанным именем
    with sql.connect("one_hot.db") as con:
        cur = con.cursor()
        try:
            cur.execute(f"""CREATE TABLE {table_name} (
                        {table_name}_ID INTEGER PRIMARY KEY AUTOINCREMENT
                        )""")
            print (f'Таблица {table_name} успешно создана')
        except:
            print (f'Таблица {table_name} уже существует')
    
def Add_Column_In_Table(table_name:str='Human_Language',
                        columns_Name_Type:dict={"Word":'TEXT'}):#добавляет столбцы в таблицу
                                                                    # с указанным именем
    with sql.connect("one_hot.db") as con:
        cur = con.cursor()
        for key,value in columns_Name_Type.items():
            try:
                cur.execute(f"""ALTER TABLE {table_name} ADD COLUMN {key} '{value}'""")
                con.commit()
                print (f'Добавлен столбец {key} в таблицу {table_name}')
            except:
                cur.execute(f"""PRAGMA table_info('{table_name}')""")
                print (f'Столбец {key} уже есть в таблице {table_name}')
def Add_Info_Into_Table(table_name:str='Human_Language', #добавляет информацию в таблицу если она пустая
                        info:dict={'Word':('("ROBOT")','("HUMAN")')}):
    with sql.connect("one_hot.db") as con:
        cur = con.cursor() 
        cur.execute(f"""SELECT * FROM {table_name}""")
        if not cur.fetchall():
            for column_name,add_in_column in info.items():
                for i in range(len(add_in_column)):
                    cur.execute(f"""INSERT INTO {table_name}({column_name}) 
                                VALUES {add_in_column[i]}""")
                    con.commit()
                print(f'Данные добавлены в столбец {column_name} таблицы {table_name}')
        else:
            print(f'Данные в таблице {table_name} уже имеются')

def Delete_Info(table_name:str='whoAmI'): #очистка данных таблицы
    with sql.connect("one_hot.db") as con:
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM {table_name}""")
        if cur.fetchall():
            cur.execute(f"""DELETE FROM {table_name}""")
            con.commit()
            print(f'Таблица {table_name} очищена')
        else:
            print(f'Таблица {table_name} пуста. Очистка не требуется')
    



os.system('cls')
lst = ['robot'] * 10
lst += ['human'] * 10
random.shuffle(lst)
data1 = pd.DataFrame({'whoAmI':lst})
data2 = pd.get_dummies(data1)
print(data1.head())
print(data2.head())
list_human_robot:list=lst
tables:dict={'Human_Language':{'Word':'TEXT'},
             'Robot_Language':{'Human_Language':'TEXT','ROBOT':'INTEGER','HUMAN':'INTEGER'},
             'Who_Am_I':{'Who_Am_I':'TEXT','ROBOT':'INTEGER','HUMAN':'INTEGER'}}

for table_name, columns in tables.items(): #создаем таблицы
    Create_Table(table_name)
    Add_Column_In_Table(table_name,columns)
Delete_Info('Who_Am_I') #очищаем таблицу Who_Am_I
robot_list:list=[]
for who in list_human_robot:
    if who == 'robot':
        robot_list.append("('robot',1,0)")
    else:
        robot_list.append("('human',0,1)")
robot_tuple:tuple=tuple(robot_list)
whoAmI_dict:dict={}
whoAmI_dict["Who_Am_I, ROBOT, HUMAN"] = robot_tuple
Add_Info_Into_Table('Who_Am_I',whoAmI_dict)        
robot_lang_dict:dict={}
robot_lang_dict["Human_Language, ROBOT, HUMAN"]=('("ROBOT", 1, 0)','("HUMAN", 0, 1)')
Add_Info_Into_Table('Robot_Language',robot_lang_dict)
Add_Info_Into_Table('Human_Language',{'Word':('("ROBOT")','("HUMAN")')})

with sql.connect('one_hot.db') as con:
    cur=con.cursor()
    for_pd = cur.execute("""SELECT Who_Am_I, ROBOT, HUMAN FROM Who_Am_I""")
print(cur.fetchall())


