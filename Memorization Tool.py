from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class MyClass(Base):
    __tablename__ = 'flashcard'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    box = Column(Integer)

engine = create_engine('sqlite:///flashcard.db? check_same_thread=False')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class FlashCards():
    def __init__(self):
        self.dict = {}

    def add_flashcard(self):
        while True:
            box = 0
            question = input('Question:\n')
            if question:
                while True:
                    answer = input('Answer:\n')
                    if answer:
                        new_data = MyClass(question=question, answer=answer, box=box)
                        session.add(new_data)
                        session.commit()
                        self.dict[question] = answer
                        self.add_flashcard_submenu()

    def add_flashcard_submenu(self):
        choose = input("""
1. Add a new flashcard
2. Exit
""")
        if choose == '1':
            print('')
            self.add_flashcard()
        elif choose == '2':
            print('')
            self.main_menu()
        else:
            print(f'\n{choose} is not an option')
            self.add_flashcard_submenu()

    def practice_flashcard(self, result_list):
        for el in result_list:
            print('\nQuestion:', el.question)
            if not self.sub_menu_practice(el):
                continue
        print('')
        self.main_menu()

    def sub_menu_practice(self, el):
        choose = input("""press "y" to see the answer:
press "n" to skip:
press "u" to update:
""")
        if choose == 'y':
            print('Answer:', el.answer)
            choice = input("""press "y" if your answer is correct:
press "n" if your answer is wrong:
""")
            if choice == 'y':
                el.box += 1
                session.commit()
                if el.box == 3:
                    session.delete(el)
                    session.commit()
            else:
                return None
        elif choose == 'n':
            input("""press "y" if your answer is correct:
press "n" if your answer is wrong:
""")
            el.box += 1
            session.commit()
            if el.box == 3:
                session.delete(el)
                session.commit()
            return None
        elif choose == 'u':
            self.update_flashcard(el)
            return None
        else:
            print(f'{choose} is not an option')
            self.sub_menu_practice(el)

    def update_flashcard(self, el):
        choose = input("""press "d" to delete the flashcard:
press "e" to edit the flashcard:
""")
        if choose == 'd':
            session.delete(el)
            session.commit()
            return None
        elif choose == 'e':
            print(f"""
current question: {el.question}
please write a new question:""")
            el.question = input()
            session.commit()
            print(f"""
current answer: {el.answer}
please write a new answer:""")
            el.answer = input()
            session.commit()
        else:
            print(f'{choose} is not an option')
            self.update_flashcard(el)

    def main_menu(self):
        self.result_list = session.query(MyClass).all()
        choose = input(("""1. Add flashcards
2. Practice flashcards
3. Exit\n"""))
        if choose == '1':
            self.add_flashcard_submenu()
        elif choose == '2':
            if not self.result_list:
                print("\nThere is no flashcard to practice!\n")
                self.main_menu()
            else:
                self.practice_flashcard(self.result_list)
        elif choose == '3':
            print('\nBye!')
            quit()
        else:
            print(f'\n{choose} is not an option\n')
            self.main_menu()

def main():
    flash_cards = FlashCards()
    flash_cards.main_menu()

main()
