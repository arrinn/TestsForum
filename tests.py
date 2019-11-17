import database_connector

database_connector.add_question(123, 'how do you feel?')
database_connector.add_question(123, 'where are you?')
list = database_connector.get_questions_list()
print(list)

print(list[0].text)


