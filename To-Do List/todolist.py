from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    # __repr__(self):
    #    return self.task

    def addTask(self, description, deadline, session):
        new_row = Table(task=description, deadline=deadline)
        session.add(new_row)
        session.commit()
        print("The task has been added!")

    def todaysTasks(self, session):
        today = datetime.today()
        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        if rows:
            print(f"Today {today.day} {today.strftime('%b')}:")
            for i, row in enumerate(rows):
                print(f"{i+1}. {row.task}")
        else:
            print("Nothing to do!")

    def all_tasks(self, session):
        rows = session.query(Table).order_by(Table.deadline).all()
        if rows:
            print('All tasks')
            for i, row in enumerate(rows):
                print(f"{i+1}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
        else:
            print("Nothing to do!")

    def weeks_task(self, session):
        today = datetime.today()
        j = 0
        while j < 7:
            taskdate = today + timedelta(days=j)
            rows = session.query(Table).filter(Table.deadline == taskdate.date()).all()
            weekdayno = taskdate.weekday()
            weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            weekday = weekdays[weekdayno]
            print(f"{weekday} {taskdate.day} {taskdate.strftime('%b')}:")
            if rows:
                for i, row in enumerate(rows):
                    print(f"{i+1}. {row.task}")
            else:
                print("Nothing to do!")
            print("\n")
            j += 1

    def missed_task(self, session):
        today = datetime.today()
        rows = session.query(Table).filter(Table.deadline < today).order_by(Table.deadline).all()
        if rows:
            print('Missed tasks:')
            for i, row in enumerate(rows):
                print(f"{i+1}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
        else:
            print("Nothing is missed!")

    def delete_task(self, session):
        rows = session.query(Table).order_by(Table.deadline).all()
        if rows:
            print('Choose the number of the task you want to delete:')
            for i, row in enumerate(rows):
                print(f"{i+1}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
            delrow = rows[int(input())-1]
            session.delete(delrow)
            session.commit()
            print('The task has been deleted!')
        else:
            print('Nothing to delete')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

table = Table()

exitloop = False
while not exitloop:
    print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
    selection = int(input())
    if selection == 1:
        table.todaysTasks(session)
    elif selection == 2:
        table.weeks_task(session)
    elif selection == 3:
        table.all_tasks(session)
    elif selection == 4:
        table.missed_task(session)
    elif selection == 5:
        task = input("Enter task")
        deadline = datetime.strptime(input("Enter deadline"), '%Y-%m-%d')
        table.addTask(task, deadline, session)
    elif selection == 6:
        table.delete_task(session)
    elif selection == 0:
        exitloop = True
        print("Bye!")
    print()
