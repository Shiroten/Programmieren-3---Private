import Vokabeltrainer

d = {'squirrel': 'Eichhörnchen', 'crocodile': 'Krokodile'}
vocabletrainer = Vokabeltrainer()
vocabletrainer.add('squirrel', 'Eichhörnchen')
# print(vocabletrainer.vocables)

vocabletrainer.init()
# print(vocabletrainer.vocables)

vocabletrainer.train(5)
vocabletrainer.result()

vocabletrainer.result(2)
vocabletrainer.result()
