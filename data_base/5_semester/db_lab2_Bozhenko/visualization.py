import matplotlib.pyplot as plt
import pickle

q1 = []
q1_qwestion = "Скільки якого виду взаємодій користувачів виявлено?"
with open("query1.pickle", "rb") as infile:
 	q1 = pickle.load(infile)

l = [el[0].strip() for el in q1]
y = [el[1] for el in q1]

plt.pie(y, labels=l, autopct='%1.f%%')
plt.title(q1_qwestion)
plt.show()

# -------------------------------------------------------------------

q2 = []
q2_qwestion = "Скільки авторів є в кожній країні?"
with open("query2.pickle", "rb") as infile:
 	q2 = pickle.load(infile)

x = [el[0].strip() for el in q2]
y = [el[1] for el in q2]
plt.bar(x, y)
plt.title(q2_qwestion)
plt.yticks(y)
plt.show()

# -------------------------------------------------------------------

q3 = []
q3_qwestion = "Яка кількість переглядів контенту, створеного авторами з кожної країни?"
with open("query3.pickle", "rb") as infile:
 	q3 = pickle.load(infile)

x = [el[0].strip() for el in q3]
y = [el[1] for el in q3]
plt.bar(x, y)
plt.title(q3_qwestion)
plt.yticks(y)
plt.show()
