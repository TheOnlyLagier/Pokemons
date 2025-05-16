import random
from colorama import Fore, Style, init

init(autoreset=True)

class Cichnamoni:
    def __init__(self, jmeno, typ,trener=None):
        self.jmeno = jmeno
        self.typ = typ
        self.zdravi = 100
        self.stit = 50
        self.xp = 0
        self.level = 1
        self.unikatni_utok_info = {"Název": "", "Popis": ""}
        self.zablokovany_utoky = 0
        self.slabsi_utoky = 0
        self.firestorm_next_turn = False 
        self.trener = trener
        self.max_zdravi = 100
        self.max_stit = 50

    def utok(self):
        if self.typ == "Oheň":
            return random.randint(10, 30)
        elif self.typ == "Voda":
            return random.randint(5, 35)
        elif self.typ == "Země":
            return random.randint(15, 25)
        elif self.typ == "Elektro":
            return random.randint(2, 40)
        elif self.typ == "Tráva":
            return random.randint(12, 29)

    def prijmi_utok(self, sila):
        if self.stit > 0:
            if sila <= self.stit:
                self.stit -= sila
            else:
                zbyva = sila - self.stit
                self.stit = 0
                self.zdravi -= zbyva
        else:
            self.zdravi -= sila

    def level_up(self, xp):
        self.xp +=xp
        while self.xp >= 100:
            self.level += 1
            self.xp -= 100

            #lepsi staty  16.5.2025  01:12 hodin
            self.max_zdravi += 10
            self.max_stit += 5
            self.zdravi = self.max_zdravi
            self.stit = self.max_stit

            print(Fore.GREEN + f"{self.jmeno} právě postoupil na level {self.level}!")
            print(Fore.LIGHTGREEN_EX + f"Nové staty: HP: {self.zdravi}, Štít: {self.stit}")

    def info(self):
        return (f"{Style.BRIGHT}Jméno: {self.jmeno} | Typ: {self.typ} | HP: {self.zdravi} | Štít: {self.stit} | Level: {self.level}")

    def efektivita(self, typ_nepritele):
        if self.typ == "Oheň" and typ_nepritele == "Tráva":
            return 1.5
        elif self.typ == "Voda" and typ_nepritele == "Oheň":
            return 1.5
        elif self.typ == "Země" and typ_nepritele == "Elektro":
            return 1.5
        elif self.typ == "Elektro" and typ_nepritele == "Voda":
            return 1.5
        elif self.typ == "Tráva" and typ_nepritele == "Země":
            return 1.5
        elif self.typ == typ_nepritele:
            return 1
        else:
            return 0.75

    def proved_unikatni_utok(self, nepritel):
        if self.typ == "Oheň":
            print(Fore.RED + f"{self.jmeno} použil svůj unikátní útok: Firestorm! 30 DMG")
            nepritel.prijmi_utok(30)
            nepritel.firestorm_next_turn = True 
            print(Fore.RED + "Další kolo způsobí 20 DMG.")
        elif self.typ == "Voda":
            print(Fore.BLUE + f"{self.jmeno} použil svůj unikátní útok: Tsunami! 35 DMG")
            nepritel.prijmi_utok(35)
            nepritel.zablokovany_utoky = 2
            print(Fore.BLUE + "Nepřítel nemůže útočit 2 kola.")
        elif self.typ == "Elektro":
            print(Fore.YELLOW + f"{self.jmeno} použil svůj unikátní útok: Thunderstrike! 45 DMG")
            nepritel.prijmi_utok(45)
            if random.random() < 0.5:
                nepritel.zablokovany_utoky = 1
                print(Fore.YELLOW + "50% šance: Nepřítel nemůže útočit v dalším kole.")
        elif self.typ == "Země":
            print(Fore.GREEN + f"{self.jmeno} použil svůj unikátní útok: Earthquake! 22 DMG")
            nepritel.prijmi_utok(22)
        elif self.typ == "Tráva":
            print(Fore.LIGHTGREEN_EX + f"{self.jmeno} použil svůj unikátní útok: Leaf Storm! 35 DMG")
            nepritel.prijmi_utok(35)
            nepritel.slabsi_utoky = 1
            print(Fore.LIGHTGREEN_EX + "Nepřítel má snížený DMG o 30% na další kolo.")

    def boj(self, nepritel, interaktivni=False):
        print(Fore.YELLOW + f"\n⚔️ Souboj mezi {self.jmeno} a {nepritel.jmeno} začíná! ⚔️\n")
        while self.zdravi > 0 and nepritel.zdravi > 0:
            if nepritel.firestorm_next_turn:
                nepritel.prijmi_utok(20)
                nepritel.firestorm_next_turn = False
                print(Fore.RED + f"{nepritel.jmeno} dostává 20 DMG z Firestormu!")

            if interaktivni:
                akce = input(Fore.CYAN + "Vyber akci (útok/obrana/útěk/unikátní útok) 1/2/3/4: ").lower()
                if akce == "3":
                    print(Fore.MAGENTA + f"{self.jmeno} utekl z boje!")
                    return
                elif akce == "2":
                    self.stit += 10
                    print(Fore.BLUE + f"{self.jmeno} se brání a získává 10 štítu navíc (nyní {self.stit})")
                elif akce == "1":
                    utok1 = int(self.utok() * self.efektivita(nepritel.typ))
                    print(Fore.RED + f"{self.jmeno} útočí a dává {utok1} damage!")
                    nepritel.prijmi_utok(utok1)
                elif akce == "4":
                    self.proved_unikatni_utok(nepritel)
                else:
                    print(Fore.LIGHTBLACK_EX + "❌ Neplatná akce!")
            else:
                if random.random() < 0.15: #muj unikatni utok 15% sance
                    self.proved_unikatni_utok(nepritel)
                else:
                    utok1 = int(self.utok() * self.efektivita(nepritel.typ))
                    print(Fore.RED + f"{self.jmeno} útočí a dává {utok1} damage!")
                    nepritel.prijmi_utok(utok1)

            if nepritel.zdravi > 0:
                if nepritel.zablokovany_utoky > 0:
                    nepritel.zablokovany_utoky -= 1
                    print(Fore.MAGENTA + f"{nepritel.jmeno} nemůže útočit tento kolo!")
                else:
                    if random.random() < 0.15:  #Unikatni utoky nepritele 15% sance
                        nepritel.proved_unikatni_utok(self)
                    else:
                        utok2 = int(nepritel.utok() * nepritel.efektivita(self.typ))
                        if nepritel.slabsi_utoky > 0:
                            utok2 = int(utok2 * 0.7)
                            nepritel.slabsi_utoky -= 1
                        print(Fore.MAGENTA + f"{nepritel.jmeno} útočí a dává {utok2} damage!")
                        self.prijmi_utok(utok2)



            print(
                Style.BRIGHT + f"\n{self.jmeno}: {self.zdravi} HP, {self.stit} štít | {nepritel.jmeno}: {nepritel.zdravi} HP, {nepritel.stit} štít\n")

        if self.zdravi > 0:
            print(Fore.GREEN + f"🎉 {self.jmeno} vyhrál!")
            self.level_up(50)
            self.trener.vyhra +=1
            self.trener.zapasy +=1
            nepritel.trener.prohra +=1
            nepritel.trener.zapasy +=1

        else:
            print(Fore.GREEN + f"🎉 {nepritel.jmeno} vyhrál!")
            nepritel.level_up(50)
            nepritel.trener.vyhra += 1
            nepritel.trener.zapasy += 1
            self.trener.prohra +=1
            self.trener.zapasy +=1

    def obnov_stav(self):
        self.zdravi = self.max_zdravi
        self.stit = self.max_stit
        self.firestorm_next_turn = False
        self.zablokovany_utoky = 0
        self.slabsi_utoky = 0

class Trener:
    def __init__(self, jmeno):
        self.jmeno = jmeno
        self.vyhra = 0
        self.zapasy = 0
        self.prohra = 0
        self.tym = []

    def statistiky(self):
        print(Fore.LIGHTCYAN_EX + f"\n📊 Statistika trenéra {self.jmeno}:")
        print(f"Výhry: {self.vyhra}")
        print(f"Prohry: {self.prohra}")
        print(f"Odehrané zápasy: {self.zapasy}")

    def pridej_tym(self, pokemon):
        self.tym.append(pokemon)
        pokemon.trener = self

    def dostupni_pokemoni(self):
        print(Fore.LIGHTBLUE_EX + f"{self.jmeno}ův tým:")
        for pokemon in self.tym:
            print(pokemon.info())

    def vyber_pokemona(self, jmeno):
        for pokemon in self.tym:
            if pokemon.jmeno.lower() == jmeno.lower():
                return pokemon
        print(Fore.RED + f"{self.jmeno} nemá pokémona jménem {jmeno}")
        return None

def spust_hru():
    pok1 = Cichnamoni("Flareon", "Oheň")
    pok2 = Cichnamoni("Vaporeon", "Voda")
    pok3 = Cichnamoni("Volteon", "Elektro")
    pok4 = Cichnamoni("Digtrio", "Země")
    pok5 = Cichnamoni("Leafeon", "Tráva")

    Trener1 = Trener("Ash")
    Trener2 = Trener("Brock")

    Trener1.pridej_tym(pok1)
    Trener1.pridej_tym(pok3)
    Trener2.pridej_tym(pok2)
    Trener2.pridej_tym(pok5)

    Trener1.dostupni_pokemoni()
    Trener2.dostupni_pokemoni()

    while True:
        interaktivni_rezim = input(Fore.CYAN + "Chceš hrát v interaktivním režimu? (ano/ne): ").lower()
        if interaktivni_rezim != "ano" and interaktivni_rezim != "ne":
            print("Neumis psat")
            continue
        interaktivni_rezim = interaktivni_rezim == "ano"
        bojovnik1 = None
        while not bojovnik1:
            Trener1.dostupni_pokemoni()
            Trener2.dostupni_pokemoni()
            jmeno1 = input(Fore.CYAN + "\nAsh, vyber svého Pokémona: ")
            bojovnik1 = Trener1.vyber_pokemona(jmeno1)

        bojovnik2 = None
        while not bojovnik2:
            jmeno2 = input(Fore.CYAN + "Brock, vyber svého Pokémona: ")
            bojovnik2 = Trener2.vyber_pokemona(jmeno2)

        bojovnik1.boj(bojovnik2, interaktivni=interaktivni_rezim)

        odpoved = input(Fore.MAGENTA + "\nChcete hrát další zápas? (ano/ne): ").lower()
        if odpoved != "ano":
            print(Fore.GREEN + "Díky za hraní! 👋")
            break

        Trener1.statistiky()
        Trener2.statistiky()

        bojovnik1.obnov_stav()
        bojovnik2.obnov_stav()

spust_hru()
