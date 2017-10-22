from vokabeltrainer import VokabelTrainer

d = {'squirrel': 'Eichhörnchen', 'crocodile': 'Krokodile'}
vocabletrainer = VokabelTrainer(d)
vocabletrainer.add('squirrel', 'Eichhörnchen')
print("Inhalt des Dictonary vorm Init")
print(vocabletrainer.vocables, "\n")

vocabletrainer.init()
print("Inhalt des Dictonary nach Init")
print(vocabletrainer.vocables, "\n")

vocabletrainer.add('clock', 'Uhr')
print("Inhalt des Dictonary nach Add")
print(vocabletrainer.vocables, "\n")

a = input("Geben Sie die Anzahl der Dürchläufe an: ")
vocabletrainer.train(int(a))
vocabletrainer.result()

a = input("Geben Sie erneut die Anzahl der Dürchläufe an: ")
vocabletrainer.reset(int(2))
vocabletrainer.result()
