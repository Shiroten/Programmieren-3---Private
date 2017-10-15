"""
Modul vokabeltrainer.
"""
import random


class Vokabeltrainer(object):
    """
    Grundklasse für Vokabeltrainer
    """

    def __init__(self, dictionary):
        # dictionary = {'cat':'Katze'}
        self.vocables = dictionary
        self.answerRight = 0
        self.answerWrong = 0

    def init(self):
        """
            Fügt zum Testen Werte zu vocables
        """
        self.vocables['cat'] = 'Katze'
        self.vocables['dog'] = 'Hund'
        self.vocables['fish'] = 'Fisch'
        self.vocables['tree'] = 'Baum'

    def add(self, keyToAdd, valueToAdd):
        """
            Fügt dem dictonary vokabeln weitere Einträge hinzu

            Args:
                keyToAdd: neuer Schlüssel
                valueToAdd: neuer Wert
            """
        self.vocables[keyToAdd] = valueToAdd

    def train(self, number):
        """
            Erzeugt die Abfragen in abhängigkeit der Anzahl

        :type number: int
        :param number: Anzahl der gestellten Fragen
        :return:
        """
        for x in range(0, number):
            randomKey = random.choice(list(self.vocables.keys()))
            print("English: ", randomKey)
            answer = input('Bitte das deutsche Wort eintippen: ')
            if self.vocables.get(randomKey).lower() == answer.lower():
                self.answerRight = self.answerRight + 1
                print("Die Antwort war korrekt\n")
            else:
                self.answerWrong = self.answerWrong + 1
                print("Die Antwort war falsch\n")

    def reset(self, runs):
        """
            Resetet die Anzahl der Versuche und startet eine neue Trainingsrunde
        :type runs: int
        :param runs: Anzahl der Fragen der neuen Runde
        """

        self.answerWrong = 0
        self.answerRight = 0
        self.train(runs)

    def result(self):
        """
            Gibt die Anzahl der richtigen und Falschen Antworten aus
        """

        print('Ergebnisse: -------------\n'
              'Richtige Antworten:{} \n'
              'Falsche  Antworten:{} \n'.format(self.answerRight, self.answerWrong))


if __name__ == "__main__":
    d = {'squirrel': 'Eichhörnchen', 'crocodile': 'Krokodile'}
    vocabletrainer = Vokabeltrainer(d)
    vocabletrainer.add('squirrel', 'Eichhörnchen')
    print("Inhalt des Dictonary vorm Init")
    print(vocabletrainer.vocables,"\n")

    vocabletrainer.init()
    print("Inhalt des Dictonary nach Init")
    print(vocabletrainer.vocables,"\n")

    a = input("Geben Sie die Anzahl der Dürchläufe an: ")
    vocabletrainer.train(int(a))
    vocabletrainer.result()

    a = input("Geben Sie erneut die Anzahl der Dürchläufe an: ")
    vocabletrainer.reset(int(2))
    vocabletrainer.result()
