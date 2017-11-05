"""
Modul vokabeltrainer.
"""
import random


class VokabelTrainer:
    """
    Grundklasse für Vokabeltrainer
    """

    def __init__(self, dictionary={'cat': 'Katze'}):
        self.vocables = dictionary
        self.answer_right = 0
        self.answer_wrong = 0

    def init(self):
        """
            Fügt zum Testen Werte zu vocables
        """
        self.vocables['cat'] = 'Katze'
        self.vocables['dog'] = 'Hund'
        self.vocables['fish'] = 'Fisch'
        self.vocables['tree'] = 'Baum'

    def add(self, key_to_add, value_to_add):
        """
            Fügt dem dictonary vokabeln weitere Einträge hinzu

            Args:
                key_to_add: neuer Schlüssel
                value_to_add: neuer Wert
            """
        self.vocables[key_to_add] = value_to_add

    def random_key_gen(self, number):
        """
            Zufaellige Auswahl von n Schluesseln aus dem dict d
        """
        if (number > len(self.vocables)):
            raise IndexError('Liste enthaelt nicht genuegend Elemente')
        else:
            k_list = list(self.vocables.keys())
            random.shuffle(k_list)
            for k in k_list[:number]:
                yield k

    def train(self, number):
        """
            Erzeugt die Abfragen in abhängigkeit der Anzahl

        :type number: int
        :param number: Anzahl der gestellten Fragen
        :return:
        """
        for i in range(0, number):
            random_key = random.choice(list(self.vocables.keys()))
            print("English: ", random_key)
            answer = input('Bitte das deutsche Wort eintippen: ')
            if self.vocables.get(random_key).lower() == answer.lower():
                self.answer_right = self.answer_right + 1
                print("Die Antwort war korrekt\n")
            else:
                self.answer_wrong = self.answer_wrong + 1
                print("Die Antwort war falsch\n")

    def train_new(self, number):
        for random_key in self.random_key_gen(number):
            print("English: ", random_key)
            answer = input('Bitte das deutsche Wort eintippen: ')
            if self.vocables.get(random_key).lower() == answer.lower():
                self.answer_right = self.answer_right + 1
                print("Die Antwort war korrekt\n")
            else:
                self.answer_wrong = self.answer_wrong + 1
                print("Die Antwort war falsch\n")

    def reset(self, runs):
        """
            Resetet die Anzahl der Versuche und startet eine neue Trainingsrunde
        :type runs: int
        :param runs: Anzahl der Fragen der neuen Runde
        """

        self.answer_wrong = 0
        self.answer_right = 0
        self.train_new(runs)

    def result(self):
        """
            Gibt die Anzahl der richtigen und Falschen Antworten aus
        """

        print('Ergebnisse: -------------\n'
              'Richtige Antworten:{} \n'
              'Falsche  Antworten:{} \n'.format(self.answer_right, self.answer_wrong))


def main():
    """
    main function
    """
    dictionary = {'squirrel': 'Eichhörnchen', 'crocodile': 'Krokodile'}
    vocable_trainer = VokabelTrainer(dictionary)
    vocable_trainer.add('squirrel', 'Eichhörnchen')
    print("Inhalt des Dictonary vorm Init")
    print(vocable_trainer.vocables, "\n")

    vocable_trainer.init()
    print("Inhalt des Dictonary nach Init")
    print(vocable_trainer.vocables, "\n")

    vocable_trainer.add('clock', 'Uhr')
    print("Inhalt des Dictonary nach Add")
    print(vocable_trainer.vocables, "\n")

    answer = input("Geben Sie die Anzahl der Dürchläufe an: ")
    vocable_trainer.train_new(int(answer))
    vocable_trainer.result()

    answer = input("Geben Sie erneut die Anzahl der Dürchläufe an: ")
    vocable_trainer.reset(int(2))
    vocable_trainer.result()


if __name__ == "__main__":
    main()
