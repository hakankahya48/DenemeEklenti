from phBot import *
from threading import Timer
from time import sleep
import phBotChat
import QtBind
import struct
import random
import json
import os
import time

pName = 'xEsyaBildir'
pVersion = '3.0'
NewestVersion = '0'

gui = QtBind.init(__name__, pName)
tbxLeaders = QtBind.createLineEdit(gui,"",470,41,110,20)
lstLeaders = QtBind.createList(gui,470,62,110,70)
btnAddLeader = QtBind.createButton(gui,'btnAddLeader_clicked'," Lider Ekle ",581,39)
btnRemLeader = QtBind.createButton(gui,'btnRemLeader_clicked'," Lider Sil ",581,61)
metaby = QtBind.createLabel(gui,'edited by hakankahya',485,220)
lstInfo = QtBind.createList(gui,15,42,450,220)
btnkarakter = QtBind.createButton(gui,'btnkarakter_clicked'," Karakter Bilgi ",15,11)
btnesya = QtBind.createButton(gui,'btnesya_clicked'," Esya ve Elixir Bilgi ",92,11)
btncoin = QtBind.createButton(gui,'btncoin_clicked'," Coin Bilgi ",190,11)
btncard = QtBind.createButton(gui,'btncard_clicked'," FGW Kart Bilgi ",265,11)

def btnkarakter_clicked():
	QtBind.clear(gui,lstInfo)
	QtBind.append(gui,lstInfo,'- ENV : Envanterin boş yuvasını bildirir.\n- GOLD : Şuanki Altını Bildirir.\n- EXP : Şuanki LV , EXP ve SP bildirir.\n- JOBEXP : JOB EXP bildirir.\n- POUCH : Meslek kesesini bildirir.(Uzmanlik)')
def btnesya_clicked():
	QtBind.clear(gui,lstInfo)
	QtBind.append(gui,lstInfo,'- LAMP : Envanterdeki Lambaları bildirir.\n- SOX : Envanter, Pet ve Deponuzdaki sox ögelerini bildirir.(Kuşanmişlar hariç)\n- FLOWER : Envanter ve Deponuzdaki çiçegi bildirir.\n- ICE : Envanterinizdeki dondurma(event)bildirir.\n- PANDORA : Envanter, Pet ve Deponuzdaki Pandora Kutusunu bildirir.\n- MS : Envanter, Pet ve Deponuzdaki MSS Bildirir.\n- LUCK : Envanter, Pet ve Deponuzdaki Lucky Stoneleri bildirir.\n- STEADY : Envanter, Pet ve Deponuzdaki Stedy Stoneleri Bildirir.\n- ELIXIR : Envanter, Pet ve Deponuzdaki toplam Elixir miktarını bildirir.\n- BLUE : Envanter, Pet ve Deponuzdaki toplam Blue Stone miktarını bildirir.\n- BLUE2 : Envanter, Pet ve Deponuzdaki toplam Blue Stone miktarını bildirir.\n- STAT : Envanter, Pet ve Deponuzdaki toplam Stat Stone miktarını bildirir.\n- STAT2 : Envanter, Pet ve Deponuzdaki toplam Stat Stone miktarını bildirir.\n- CATA : Envanterinizde olan Alchemy Catalyst miktarını bildirir.')
def btncoin_clicked():
	QtBind.clear(gui,lstInfo)
	QtBind.append(gui,lstInfo,'- COIN : Envanterdeki Gold/Silver/Iron/Copper/Arena Coin miktarını bildirir.')
def btncard_clicked():
	QtBind.clear(gui,lstInfo)
	QtBind.append(gui,lstInfo,'- FGW8DG : Envanter, Pet ve Deponuzda bulunan 8DG FGW Kartlarını bildirir.\n- FGW9DG : Envanter, Pet ve Deponuzda bulunan 9DG FGW Kartlarını bildirir.\n- FGW10DG : Envanter, Pet ve Deponuzda bulunan 10DG FGW Kartlarını bildirir.\n- FGW11DG : Envanter, Pet ve Deponuzda bulunan 11DG FGW Kartlarını bildirir.')

def getPath():
    return get_config_dir() + pName + "\\"

def getConfig():
    return getPath() + inGame['server'] + "_" + inGame['name'] + ".json"

def isJoined():
    global inGame
    inGame = get_character_data()
    if not (inGame and "name" in inGame and inGame["name"]):
        inGame = None
    return inGame

def loadDefaultConfig():
    QtBind.clear(gui, lstLeaders)

def loadConfigs():
    loadDefaultConfig()
    if isJoined():
        if os.path.exists(getConfig()):
            data = {}
            with open(getConfig(), "r") as f:
                data = json.load(f)
            if "Leaders" in data:
                for nickname in data["Leaders"]:
                    QtBind.append(gui, lstLeaders, nickname)

def btnAddLeader_clicked():
    if inGame:
        player = QtBind.text(gui, tbxLeaders)
        if player and not lstLeaders_exist(player):
            data = {}
            if os.path.exists(getConfig()):
                with open(getConfig(), 'r') as f:
                    data = json.load(f)
            if not "Leaders" in data:
                data['Leaders'] = []
            data['Leaders'].append(player)

            with open(getConfig(), "w") as f:
                f.write(json.dumps(data, indent=4, sort_keys=True))
            QtBind.append(gui, lstLeaders, player)
            QtBind.setText(gui, tbxLeaders, "")
            log('Plugin: Lider Eklendi. [' + player + ']')

def btnRemLeader_clicked():
    if inGame:
        selectedItem = QtBind.text(gui, lstLeaders)
        if selectedItem:
            if os.path.exists(getConfig()):
                data = {"Leaders": []}
                with open(getConfig(), 'r') as f:
                    data = json.load(f)
                try:
                    data["Leaders"].remove(selectedItem)
                    with open(getConfig(), "w") as f:
                        f.write(json.dumps(data, indent=4, sort_keys=True))
                except:
                    pass
            QtBind.remove(gui, lstLeaders, selectedItem)
            log('Plugin: Lider Silindi. [' + selectedItem + ']')

def lstLeaders_exist(nickname):
    nickname = nickname.lower()
    players = QtBind.getItems(gui, lstLeaders)
    for i in range(len(players)):
        if players[i].lower() == nickname:
            return True
    return False

def handleChatCommand(msg):
    args = msg.split(' ', 1)
    if len(args) != 2 or not args[0] or not args[1]:
        return
    t = args[0].lower()
    if t == 'private' or t == 'note':
        argsExtra = args[1].split(' ', 1)
        if len(argsExtra) != 2 or not argsExtra[0] or not argsExtra[1]:
            return
        args.pop(1)
        args += argsExtra
    sent = False
    if t == "all":
        sent = phBotChat.All(args[1])
    elif t == "private":
        sent = phBotChat.Private(args[1], args[2])
    elif t == "party":
        sent = phBotChat.Party(args[1])
    elif t == "guild":
        sent = phBotChat.Guild(args[1])
    elif t == "union":
        sent = phBotChat.Union(args[1])
    elif t == "note":
        sent = phBotChat.Note(args[1], args[2])
    elif t == "stall":
        sent = phBotChat.Stall(args[1])
    elif t == "global":
        sent = phBotChat.Global(args[1])
    if sent:
        log('Plugin: Mesaj "' + t + '" başarıyla gönderildi!')

def checkInv(arg):
    weapon = 0
    protector = 0
    accessory = 0
    shield = 0
    arena = 0
    qgold = 0
    silver = 0
    iron = 0
    copper = 0
    flower1 = 0
    flower2 = 0
    flower3 = 0
    flower4 = 0
    flower5 = 0
    catalyst = 0
    blue1 = 0
    blue2 = 0
    blue3 = 0
    blue4 = 0
    blue5 = 0
    blue6 = 0
    blue7 = 0
    blue8 = 0
    blue9 = 0
    blue10 = 0
    blue11 = 0
    blue12 = 0
    blue13 = 0
    blue14 = 0
    stat1 = 0
    stat2 = 0
    stat3 = 0
    stat4 = 0
    stat5 = 0
    stat6 = 0
    stat7 = 0
    stat8 = 0
    stat9 = 0
    stat10 = 0
    stat11 = 0
    stat12 = 0
    stat13 = 0
    stat14 = 0
    pandora = 0
    ms = 0
    luck = 0
    steady = 0
    cream = 0
    lamp = 0
    dLamp = 0
    card1 = 0
    card2 = 0
    card3 = 0
    card4 = 0
    card5 = 0
    card6 = 0
    card7 = 0
    card8 = 0
    card9 = 0
    card10 = 0
    card11 = 0
    card12 = 0
    card13 = 0
    card14 = 0
    card15 = 0
    card16 = 0
    card17 = 0
    card18 = 0
    card19 = 0
    card20 = 0
    card21 = 0
    card22 = 0
    card23 = 0
    card24 = 0
    card25 = 0
    card26 = 0
    card27 = 0
    card28 = 0
    card29 = 0
    card30 = 0
    card31 = 0
    card32 = 0
    faded = 0
    sunItems = 0
    items = []
    items = get_inventory()['items'][13:]

    if items:
        for item in items:
            if item is not None:
                if "Lv.11" in item['name'] and "Weapon" in item['name']:
                    weapon += item['quantity']
                if "Lv.11" in item['name'] and "Armor" in item['name']:
                    protector += item['quantity']
                if "Lv.11" in item['name'] and "Accessory" in item['name']:
                    accessory += item['quantity']
                if "Lv.11" in item['name'] and "Shield" in item['name']:
                    shield += item['quantity']
                if "Flower" in item['name'] and "Evil" in item['name']:
                    flower1 += item['quantity']
                if "Flower" in item['name'] and "Illusion" in item['name']:
                    flower2 += item['quantity']
                if "Flower" in item['name'] and "Life" in item['name']:
                    flower3 += item['quantity']
                if "Flower" in item['name'] and "Energy" in item['name']:
                    flower4 += item['quantity']
                if "Flower" in item['name'] and "Whirling" in item['name']:
                    flower5 += item['quantity']
                if "Coin" in item['name'] and "Arena" in item['name']:
                    arena += item['quantity']
                if "Coin" in item['name'] and "Gold" in item['name']:
                    gold += item['quantity']
                if "Coin" in item['name'] and "Silver" in item['name']:
                    silver += item['quantity']
                if "Coin" in item['name'] and "Iron" in item['name']:
                    iron += item['quantity']
                if "Coin" in item['name'] and "Copper" in item['name']:
                    copper += item['quantity']
                if "Alchemy catalyst" in item['name'] and "catalyst" in item['name']:
                    catalyst += item['quantity']
                if "Lvl.11" in item['name'] and "Str" in item['name']:
                    blue1 += item['quantity']
                if "Lvl.11" in item['name'] and "Int" in item['name']:
                    blue2 += item['quantity']
                if "Lvl.11" in item['name'] and "master" in item['name']:
                    blue3 += item['quantity']
                if "Lvl.11" in item['name'] and "strikes" in item['name']:
                    blue4 += item['quantity']
                if "Lvl.11" in item['name'] and "discipline" in item['name']:
                    blue5 += item['quantity']
                if "Lvl.11" in item['name'] and "penetration" in item['name']:
                    blue6 += item['quantity']
                if "Lvl.11" in item['name'] and "dodging" in item['name']:
                    blue7 += item['quantity']
                if "Lvl.11" in item['name'] and "stamina" in item['name']:
                    blue8 += item['quantity']
                if "Lvl.11" in item['name'] and "magic" in item['name']:
                    blue9 += item['quantity']
                if "Lvl.11" in item['name'] and "fogs" in item['name']:
                    blue10 += item['quantity']
                if "Lvl.11" in item['name'] and "air" in item['name']:
                    blue11 += item['quantity']
                if "Lvl.11" in item['name'] and "fire" in item['name']:
                    blue12 += item['quantity']
                if "Lvl.11" in item['name'] and "immunity" in item['name']:
                    blue13 += item['quantity']
                if "Lvl.11" in item['name'] and "revival" in item['name']:
                    blue14 += item['quantity']
                if "Lvl.11" in item['name'] and "courage" in item['name']:
                    stat1 += item['quantity']
                if "Lvl.11" in item['name'] and "warriors" in item['name']:
                    stat2 += item['quantity']
                if "Lvl.11" in item['name'] and "philosophy" in item['name']:
                    stat3 += item['quantity']
                if "Lvl.11" in item['name'] and "meditation" in item['name']:
                    stat4 += item['quantity']
                if "Lvl.11" in item['name'] and "challenge" in item['name']:
                    stat5 += item['quantity']
                if "Lvl.11" in item['name'] and "focus" in item['name']:
                    stat6 += item['quantity']
                if "Lvl.11" in item['name'] and "flesh" in item['name']:
                    stat7 += item['quantity']
                if "Lvl.11" in item['name'] and "life" in item['name']:
                    stat8 += item['quantity']
                if "Lvl.11" in item['name'] and "mind" in item['name']:
                    stat9 += item['quantity']
                if "Lvl.11" in item['name'] and "spirit" in item['name']:
                    stat10 += item['quantity']
                if "Lvl.11" in item['name'] and "dodging" in item['name']:
                    stat11 += item['quantity']
                if "Lvl.11" in item['name'] and "agility" in item['name']:
                    stat12 += item['quantity']
                if "Lvl.11" in item['name'] and "training" in item['name']:
                    stat13 += item['quantity']
                if "Lvl.11" in item['name'] and "prayer" in item['name']:
                    stat14 += item['quantity']
                if "Pandora's Box" in item['name'] and "" in item['name']:
                    pandora += item['quantity']
                if "Monster Summon Scroll (ekip kullanir)" in item['name'] and "" in item['name']:
                    ms += item['quantity']
                if "Magic stone of luck(Lvl.11)" in item['name'] and "" in item['name']:
                    luck += item['quantity']
                if "Magic stone of steady(Lvl.11)" in item['name'] and "" in item['name']:
                    steady += item['quantity']
                if "ITEM_ETC_E090722_" in item['servername'] and "ICECREAM" in item['servername']:
                    cream += item['quantity']
                if "Genie’s Lamp" in item['name']:
                    lamp += item['quantity']
                if "Dirty Lamp" in item['name']:
                    dLamp += item['quantity']
                if "Red tears" in item['name'] and "" in item['name']:
                    card1 += item['quantity']
                if "Western scriptures" in item['name'] and "" in item['name']:
                    card2 += item['quantity']
                if "Togui mask" in item['name'] and "" in item['name']:
                    card3 += item['quantity']
                if "Red talisman" in item['name'] and "" in item['name']:
                    card4 += item['quantity']
                if "Puppet" in item['name'] and "" in item['name']:
                    card5 += item['quantity']
                if "Dull kitchen knife" in item['name'] and "" in item['name']:
                    card6 += item['quantity']
                if "Elder staff" in item['name'] and "" in item['name']:
                    card7 += item['quantity']
                if "Spell paper" in item['name'] and "" in item['name']:
                    card8 += item['quantity']
                if "Fire flower" in item['name'] and "" in item['name']:
                    card9 += item['quantity']
                if "Horned cattle" in item['name'] and "" in item['name']:
                    card10 += item['quantity']
                if "Flame of oblivion" in item['name'] and "" in item['name']:
                    card11 += item['quantity']
                if "Flame paper" in item['name'] and "" in item['name']:
                    card12 += item['quantity']
                if "Hearthstone flame" in item['name'] and "" in item['name']:
                    card13 += item['quantity']
                if "Enchantress necklace" in item['name'] and "" in item['name']:
                    card14 += item['quantity']
                if "Honghaeah armor" in item['name'] and "" in item['name']:
                    card15 += item['quantity']
                if "Fire dragon sword" in item['name'] and "" in item['name']:
                    card16 += item['quantity']
                if "Silver pendant" in item['name'] and "" in item['name']:
                    card17 += item['quantity']
                if "Cobalt emerald" in item['name'] and "" in item['name']:
                    card18 += item['quantity']
                if "Logbook" in item['name'] and "" in item['name']:
                    card19 += item['quantity']
                if "Love letter" in item['name'] and "" in item['name']:
                    card20 += item['quantity']
                if "Portrait of a woman" in item['name'] and "" in item['name']:
                    card21 += item['quantity']
                if "Jewelry box" in item['name'] and "" in item['name']:
                    card22 += item['quantity']
                if "Diamond watch" in item['name'] and "" in item['name']:
                    card23 += item['quantity']
                if "Mermaid’s tears" in item['name'] and "" in item['name']:
                    card24 += item['quantity']
                if "Broken Key" in item['name'] and "" in item['name']:
                    card25 += item['quantity']
                if "Large tong" in item['name'] and "" in item['name']:
                    card26 += item['quantity']
                if "Phantom harp" in item['name'] and "" in item['name']:
                    card27 += item['quantity']
                if "Evil’s heart" in item['name'] and "" in item['name']:
                    card28 += item['quantity']
                if "Vindictive sprit’s bead" in item['name'] and "" in item['name']:
                    card29 += item['quantity']
                if "Hook hand" in item['name'] and "" in item['name']:
                    card30 += item['quantity']
                if "Sereness’s tears" in item['name'] and "" in item['name']:
                    card31 += item['quantity']
                if "Commander’s patch" in item['name'] and "" in item['name']:
                    card32 += item['quantity']
                if "Faded Bead" in item['name'] and "" in item['name']:
                    faded += item['quantity']
                if 'RARE' in item['servername'] and 'EVENT' not in item['servername'] and 'ARCHEMY' not in item[
                    'servername']:
                    sunItems += 1

    pets = get_pets()
    if pets != []:
        for p in pets.keys():
            pet = pets[p]
            if pet['type'] in 'pick':
                for petItems in pet['items']:
                    if petItems != None:
                        if "Lv.11" in petItems['name'] and "Weapon" in petItems['name']:
                            weapon += petItems['quantity']
                        if "Lv.11" in petItems['name'] and "Armor" in petItems['name']:
                            protector += petItems['quantity']
                        if "Lv.11" in petItems['name'] and "Accessory" in petItems['name']:
                            accessory += petItems['quantity']
                        if "Lv.11" in petItems['name'] and "Shield" in petItems['name']:
                            shield += petItems['quantity']
                        if "Flower" in petItems['name'] and "Evil" in petItems['name']:
                            flower1 += petItems['quantity']
                        if "Flower" in petItems['name'] and "Illusion" in petItems['name']:
                            flower2 += petItems['quantity']
                        if "Flower" in petItems['name'] and "Life" in petItems['name']:
                            flower3 += petItems['quantity']
                        if "Flower" in petItems['name'] and "Energy" in petItems['name']:
                            flower4 += petItems['quantity']
                        if "Flower" in petItems['name'] and "Whirling" in petItems['name']:
                            flower5 += petItems['quantity']
                        if "Coin" in petItems['name'] and "Gold" in petItems['name']:
                            qgold += petItems['quantity']
                        if "Coin" in petItems['name'] and "Silver" in petItems['name']:
                            silver += petItems['quantity']
                        if "Coin" in petItems['name'] and "Iron" in petItems['name']:
                            iron += petItems['quantity']
                        if "Coin" in petItems['name'] and "Copper" in petItems['name']:
                            copper += petItems['quantity']
                        if "Coin" in petItems['name'] and "Arena" in petItems['name']:
                            arena += petItems['quantity']
                        if "Alchemy catalyst" in petItems['name'] and "catalyst" in petItems['name']:
                            catalyst += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "Str" in petItems['name']:
                            blue1 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "Int" in petItems['name']:
                            blue2 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "master" in petItems['name']:
                            blue3 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "strikes" in petItems['name']:
                            blue4 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "discipline" in petItems['name']:
                            blue5 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "penetration" in petItems['name']:
                            blue6 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "dodging" in petItems['name']:
                            blue7 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "stamina" in petItems['name']:
                            blue8 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "magic" in petItems['name']:
                            blue9 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "fogs" in petItems['name']:
                            blue10 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "air" in petItems['name']:
                            blue11 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "fire" in petItems['name']:
                            blue12 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "immunity" in petItems['name']:
                            blue13 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "revival" in petItems['name']:
                            blue14 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "courage" in petItems['name']:
                            stat1 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "warriors" in petItems['name']:
                            stat2 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "philosophy" in petItems['name']:
                            stat3 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "meditation" in petItems['name']:
                            stat4 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "challenge" in petItems['name']:
                            stat5 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "focus" in petItems['name']:
                            stat6 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "flesh" in petItems['name']:
                            stat7 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "life" in petItems['name']:
                            stat8 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "mind" in petItems['name']:
                            stat9 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "spirit" in petItems['name']:
                            stat10 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "dodging" in petItems['name']:
                            stat11 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "agility" in petItems['name']:
                            stat12 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "training" in petItems['name']:
                            stat13 += petItems['quantity']
                        if "Lvl.11" in petItems['name'] and "prayer" in petItems['name']:
                            stat14 += petItems['quantity']
                        if "Pandora's Box" in petItems['name'] and "" in petItems['name']:
                            pandora += petItems['quantity']
                        if "Monster Summon Scroll (ekip kullanir)" in petItems['name'] and "" in petItems['name']:
                            ms += petItems['quantity']
                        if "Magic stone of steady(Lvl.11)" in petItems['name'] and "" in petItems['name']:
                            steady += petItems['quantity']
                        if "Magic stone of luck(Lvl.11)" in petItems['name'] and "" in petItems['name']:
                            luck += petItems['quantity']
                        if "ITEM_ETC_E090722_" in petItems['servername'] and "ICECREAM" in petItems['servername']:
                            cream += petItems['quantity']
                        if "Genie’s Lamp" in petItems['name']:
                            lamp += petItems['quantity']
                        if "Dirty Lamp" in petItems['name']:
                            dLamp += petItems['quantity']
                        if "Red tears" in petItems['name'] and "" in petItems['name']:
                            card1 += petItems['quantity']
                        if "Western scriptures" in petItems['name'] and "" in petItems['name']:
                            card2 += petItems['quantity']
                        if "Togui mask" in petItems['name'] and "" in petItems['name']:
                            card3 += petItems['quantity']
                        if "Red talisman" in petItems['name'] and "" in petItems['name']:
                            card4 += petItems['quantity']
                        if "Puppet" in petItems['name'] and "" in petItems['name']:
                            card5 += petItems['quantity']
                        if "Dull kitchen knife" in petItems['name'] and "" in petItems['name']:
                            card6 += petItems['quantity']
                        if "Elder staff" in petItems['name'] and "" in petItems['name']:
                            card7 += petItems['quantity']
                        if "Spell paper" in petItems['name'] and "" in petItems['name']:
                            card8 += petItems['quantity']
                        if "Fire flower" in petItems['name'] and "" in petItems['name']:
                            card9 += petItems['quantity']
                        if "Horned cattle" in petItems['name'] and "" in petItems['name']:
                            card10 += petItems['quantity']
                        if "Flame of oblivion" in petItems['name'] and "" in petItems['name']:
                            card11 += petItems['quantity']
                        if "Flame paper" in petItems['name'] and "" in petItems['name']:
                            card12 += petItems['quantity']
                        if "Hearthstone flame" in petItems['name'] and "" in petItems['name']:
                            card13 += petItems['quantity']
                        if "Enchantress necklace" in petItems['name'] and "" in petItems['name']:
                            card14 += petItems['quantity']
                        if "Honghaeah armor" in petItems['name'] and "" in petItems['name']:
                            card15 += petItems['quantity']
                        if "Fire dragon sword" in petItems['name'] and "" in petItems['name']:
                            card16 += petItems['quantity']
                        if "Silver pendant" in petItems['name'] and "" in petItems['name']:
                            card17 += petItems['quantity']
                        if "Cobalt emerald" in petItems['name'] and "" in petItems['name']:
                            card18 += petItems['quantity']
                        if "Logbook" in petItems['name'] and "" in petItems['name']:
                            card19 += petItems['quantity']
                        if "Love letter" in petItems['name'] and "" in petItems['name']:
                            card20 += petItems['quantity']
                        if "Portrait of a woman" in petItems['name'] and "" in petItems['name']:
                            card21 += petItems['quantity']
                        if "Jewelry box" in petItems['name'] and "" in petItems['name']:
                            card22 += petItems['quantity']
                        if "Diamond watch" in petItems['name'] and "" in petItems['name']:
                            card23 += petItems['quantity']
                        if "Mermaid’s tears" in petItems['name'] and "" in petItems['name']:
                            card24 += petItems['quantity']
                        if "Broken Key" in petItems['name'] and "" in petItems['name']:
                            card25 += petItems['quantity']
                        if "Large tong" in petItems['name'] and "" in petItems['name']:
                            card26 += petItems['quantity']
                        if "Phantom harp" in petItems['name'] and "" in petItems['name']:
                            card27 += petItems['quantity']
                        if "Evil’s heart" in petItems['name'] and "" in petItems['name']:
                            card28 += petItems['quantity']
                        if "Vindictive sprit’s bead" in petItems['name'] and "" in petItems['name']:
                            card29 += petItems['quantity']
                        if "Hook hand" in petItems['name'] and "" in petItems['name']:
                            card30 += petItems['quantity']
                        if "Sereness’s tears" in petItems['name'] and "" in petItems['name']:
                            card31 += petItems['quantity']
                        if "Commander’s patch" in petItems['name'] and "" in petItems['name']:
                            card32 += petItems['quantity']
                        if "Faded Bead" in petItems['name'] and "" in petItems['name']:
                            faded += petItems['quantity']
                        if 'RARE' in petItems['servername'] and 'EVENT' not in petItems[
                            'servername'] and 'ARCHEMY' not in petItems['servername']:
                            sunItems += 1

    storages = []
    storages = get_storage()['items']
    if storages:
        for item in storages:
            if item is not None:
                if "Lv.11" in item['name'] and "Weapon" in item['name']:
                    weapon += item['quantity']
                if "Lv.11" in item['name'] and "Armor" in item['name']:
                    protector += item['quantity']
                if "Lv.11" in item['name'] and "Accessory" in item['name']:
                    accessory += item['quantity']
                if "Lv.11" in item['name'] and "Shield" in item['name']:
                    shield += item['quantity']
                if "Flower" in item['name'] and "Evil" in item['name']:
                    flower1 += item['quantity']
                if "Flower" in item['name'] and "Illusion" in item['name']:
                    flower2 += item['quantity']
                if "Flower" in item['name'] and "Life" in item['name']:
                    flower3 += item['quantity']
                if "Flower" in item['name'] and "Energy" in item['name']:
                    flower4 += item['quantity']
                if "Flower" in item['name'] and "Whirling" in item['name']:
                    flower5 += item['quantity']
                if "Coin" in item['name'] and "Gold" in item['name']:
                    qgold += item['quantity']
                if "Silver" in item['name'] and "Silver" in item['name']:
                    silver += item['quantity']
                if "Coin" in item['name'] and "Iron" in item['name']:
                    iron += item['quantity']
                if "Coin" in item['name'] and "Copper" in item['name']:
                    copper += item['quantity']
                if "Coin" in item['name'] and "Arena" in item['name']:
                    arena += item['quantity']
                if "Alchemy catalyst" in item['name'] and "catalyst" in item['name']:
                    catalyst += item['quantity']
                if "Lvl.11" in item['name'] and "Str" in item['name']:
                    blue1 += item['quantity']
                if "Lvl.11" in item['name'] and "Int" in item['name']:
                    blue2 += item['quantity']
                if "Lvl.11" in item['name'] and "master" in item['name']:
                    blue3 += item['quantity']
                if "Lvl.11" in item['name'] and "strikes" in item['name']:
                    blue4 += item['quantity']
                if "Lvl.11" in item['name'] and "discipline" in item['name']:
                    blue5 += item['quantity']
                if "Lvl.11" in item['name'] and "penetration" in item['name']:
                    blue6 += item['quantity']
                if "Lvl.11" in item['name'] and "dodging" in item['name']:
                    blue7 += item['quantity']
                if "Lvl.11" in item['name'] and "stamina" in item['name']:
                    blue8 += item['quantity']
                if "Lvl.11" in item['name'] and "magic" in item['name']:
                    blue9 += item['quantity']
                if "Lvl.11" in item['name'] and "fogs" in item['name']:
                    blue10 += item['quantity']
                if "Lvl.11" in item['name'] and "air" in item['name']:
                    blue11 += item['quantity']
                if "Lvl.11" in item['name'] and "fire" in item['name']:
                    blue12 += item['quantity']
                if "Lvl.11" in item['name'] and "immunity" in item['name']:
                    blue13 += item['quantity']
                if "Lvl.11" in item['name'] and "revival" in item['name']:
                    blue14 += item['quantity']
                if "Lvl.11" in item['name'] and "courage" in item['name']:
                    stat1 += item['quantity']
                if "Lvl.11" in item['name'] and "warriors" in item['name']:
                    stat2 += item['quantity']
                if "Lvl.11" in item['name'] and "philosophy" in item['name']:
                    stat3 += item['quantity']
                if "Lvl.11" in item['name'] and "meditation" in item['name']:
                    stat4 += item['quantity']
                if "Lvl.11" in item['name'] and "challenge" in item['name']:
                    stat5 += item['quantity']
                if "Lvl.11" in item['name'] and "focus" in item['name']:
                    stat6 += item['quantity']
                if "Lvl.11" in item['name'] and "flesh" in item['name']:
                    stat7 += item['quantity']
                if "Lvl.11" in item['name'] and "life" in item['name']:
                    stat8 += item['quantity']
                if "Lvl.11" in item['name'] and "mind" in item['name']:
                    stat9 += item['quantity']
                if "Lvl.11" in item['name'] and "spirit" in item['name']:
                    stat10 += item['quantity']
                if "Lvl.11" in item['name'] and "dodging" in item['name']:
                    stat11 += item['quantity']
                if "Lvl.11" in item['name'] and "agility" in item['name']:
                    stat12 += item['quantity']
                if "Lvl.11" in item['name'] and "training" in item['name']:
                    stat13 += item['quantity']
                if "Lvl.11" in item['name'] and "prayer" in item['name']:
                    stat14 += item['quantity']
                if "Pandora's Box" in item['name'] and "" in item['name']:
                    pandora += item['quantity']
                if "Monster Summon Scroll (ekip kullanir)" in item['name'] and "" in item['name']:
                    ms += item['quantity']
                if "Magic stone of luck(Lvl.11)" in item['name'] and "" in item['name']:
                    luck += item['quantity']
                if "Magic stone of steady(Lvl.11)" in item['name'] and "" in item['name']:
                    steady += item['quantity']
                if "ITEM_ETC_E090722_" in item['servername'] and "ICECREAM" in item['servername']:
                    cream += item['quantity']
                if "Genie’s Lamp" in item['name']:
                    lamp += item['quantity']
                if "Dirty Lamp" in item['name']:
                    dLamp += item['quantity']
                if "Red tears" in item['name'] and "" in item['name']:
                    card1 += item['quantity']
                if "Western scriptures" in item['name'] and "" in item['name']:
                    card2 += item['quantity']
                if "Togui mask" in item['name'] and "" in item['name']:
                    card3 += item['quantity']
                if "Red talisman" in item['name'] and "" in item['name']:
                    card4 += item['quantity']
                if "Puppet" in item['name'] and "" in item['name']:
                    card5 += item['quantity']
                if "Dull kitchen knife" in item['name'] and "" in item['name']:
                    card6 += item['quantity']
                if "Elder staff" in item['name'] and "" in item['name']:
                    card7 += item['quantity']
                if "Spell paper" in item['name'] and "" in item['name']:
                    card8 += item['quantity']
                if "Fire flower" in item['name'] and "" in item['name']:
                    card9 += item['quantity']
                if "Horned cattle" in item['name'] and "" in item['name']:
                    card10 += item['quantity']
                if "Flame of oblivion" in item['name'] and "" in item['name']:
                    card11 += item['quantity']
                if "Flame paper" in item['name'] and "" in item['name']:
                    card12 += item['quantity']
                if "Hearthstone flame" in item['name'] and "" in item['name']:
                    card13 += item['quantity']
                if "Enchantress necklace" in item['name'] and "" in item['name']:
                    card14 += item['quantity']
                if "Honghaeah armor" in item['name'] and "" in item['name']:
                    card15 += item['quantity']
                if "Fire dragon sword" in item['name'] and "" in item['name']:
                    card16 += item['quantity']
                if "Silver pendant" in item['name'] and "" in item['name']:
                    card17 += item['quantity']
                if "Cobalt emerald" in item['name'] and "" in item['name']:
                    card18 += item['quantity']
                if "Logbook" in item['name'] and "" in item['name']:
                    card19 += item['quantity']
                if "Love letter" in item['name'] and "" in item['name']:
                    card20 += item['quantity']
                if "Portrait of a woman" in item['name'] and "" in item['name']:
                    card21 += item['quantity']
                if "Jewelry box" in item['name'] and "" in item['name']:
                    card22 += item['quantity']
                if "Diamond watch" in item['name'] and "" in item['name']:
                    card23 += item['quantity']
                if "Mermaid’s tears" in item['name'] and "" in item['name']:
                    card24 += item['quantity']
                if "Broken Key" in item['name'] and "" in item['name']:
                    card25 += item['quantity']
                if "Large tong" in item['name'] and "" in item['name']:
                    card26 += item['quantity']
                if "Phantom harp" in item['name'] and "" in item['name']:
                    card27 += item['quantity']
                if "Evil’s heart" in item['name'] and "" in item['name']:
                    card28 += item['quantity']
                if "Vindictive sprit’s bead" in item['name'] and "" in item['name']:
                    card29 += item['quantity']
                if "Hook hand" in item['name'] and "" in item['name']:
                    card30 += item['quantity']
                if "Sereness’s tears" in item['name'] and "" in item['name']:
                    card31 += item['quantity']
                if "Commander’s patch" in item['name'] and "" in item['name']:
                    card32 += item['quantity']
                if "Faded Bead" in item['name'] and "" in item['name']:
                    faded += item['quantity']
                if 'RARE' in item['servername'] and 'EVENT' not in item['servername'] and 'ARCHEMY' not in item[
                    'servername']:
                    sunItems += 1

    if arg == "Elixir":
        handleChatCommand("party Elixir; Weapon " + str(weapon) + " , Armor " + str(protector) + " , Shield " + str(shield) + " , Accessory " + str(accessory))
    if arg == "Flower3":
        handleChatCommand("party Flower; Life " + str(flower3) + " , Energy " + str(flower4) + " , Evil " + str(flower1) + " , Illusion " + str(flower2) + " , Whirling " + str(flower5))
    if arg == "Blue":
        handleChatCommand("party STR " + str(blue1) + " , INT " + str(blue2) + " , MASTER " + str(blue3) + " , STRIKES " + str(blue4) + " , DSCPLNE " + str(blue5) + " , PNTRTON " + str(blue6) + " , DODGING " + str(blue7) + " , STAMINA " + str(blue8))
    if arg == "Blue2":
        handleChatCommand("party MAGIC " + str(blue9) + " , FOGS " + str(blue10) + " , AIR " + str(blue11) + " , FIRE " + str(blue12) + " , IMMUNITY " + str(blue13) + " , REVIVAL " + str(blue14))
    if arg == "Stat":
        handleChatCommand("party COURAGE " + str(blue1) + " , WARRIORS " + str(blue2) + " , PHILOSOPHY " + str(blue3) + " , MEDITATION " + str(blue4) + " , CHALLENGE " + str(blue5) + " , FOCUS " + str(blue6) + " , FLESH " + str(blue7))
    if arg == "Stat2":
        handleChatCommand("party LIFE " + str(blue8) + " , MIND " + str(blue9) + " , SPIRIT " + str(blue10) + " , DODGING " + str(blue11) + " , AGILITY " + str(blue12) + " , TRAINING " + str(blue13) + " , PRAYER " + str(blue14))
    if arg == "Coin":
        handleChatCommand("party Gold Coin " + str(qgold) + " , Silver Coin " + str(silver) + " , Iron Coin " + str(iron) + " , Copper Coin " + str(copper) + " , Arena Coin " + str(arena))
    if arg == "Catalyst":
        handleChatCommand("party Alchemy Catalyst " + str(catalyst))
    if arg == "Cream":
        handleChatCommand("party Ice Cream " + str(cream))
    if arg == "Pandora":
        handleChatCommand("party Pandora " + str(pandora))
    if arg == "Ms":
        handleChatCommand("party Monster Summon Scroll " + str(ms))
    if arg == "Luck":
        handleChatCommand("party Magic stone of luck " + str(luck))
    if arg == "Steady":
        handleChatCommand("party Magic stone of steady " + str(steady))
    if arg == "Lamp":
        handleChatCommand("party Genie’s Lamp " + str(lamp) + " -- Dirty Lamp " + str(dLamp))
    if arg == "fgw8dg":
        handleChatCommand("party Red tears " + str(card1) + " , Western scriptures " + str(card2) + " , Togui mask " + str(card3) + " , Red talisman " + str(card4) + " , Puppet " + str(card5) + " , Dull kitchen knife " + str(card6) + " , Elder staff " + str(card7) + " , Spell paper " + str(card8))
    if arg == "fgw9dg":
        handleChatCommand("party Fire flower " + str(card9) + " , Horned cattle " + str(card10) + " , Flame of oblivion " + str(card11) + " , Flame paper " + str(card11) + " , Hearthstone flame " + str(card12) + " , Enchantress necklace " + str(card13) + " , Honghaeah armor " + str(card14) + " , Fire dragon sword " + str(card15))
    if arg == "fgw10dg":
        handleChatCommand("party Silver pendant " + str(card1) + " , Cobalt emerald " + str(card2) + " , Logbook " + str(card3) + " , Love letter " + str(card4) + " , Portrait of a woman " + str(card5) + " , Jewelry box " + str(card6) + " , Diamond watch " + str(card7) + " , Mermaid’s tears " + str(card8))
    if arg == "fgw11dg":
        handleChatCommand("party Broken Key " + str(card1) + " , Large tong " + str(card2) + " , Phantom harp " + str(card3) + " , Evil’s heart " + str(card4) + " , Vindictive sprit’s bead " + str(card5) + " , Hook hand " + str(card6) + " , Sereness’s tears " + str(card7) + " , Commander’s patch " + str(card8))
    if arg == "Lamp":
        handleChatCommand("party Genie’s Lamp " + str(lamp) + " -- Dirty Lamp " + str(dLamp))
    if arg == "faded":
        handleChatCommand("party Faded Bead " + str(faded))
    if arg == "Sox":
        handleChatCommand("party " + str(sunItems) + " Parca SoX Ogesi")

def checkGold():
    gold = 0;
    chars = []
    chars = get_character_data()
    if chars != []:
        gold += chars['gold']
    goldS = format(gold, ",")
    handleChatCommand("party Suan " + str(goldS) + " Altin var. ")

def checkExp():
    data = get_character_data()
    currentExp = data['current_exp']
    level = data['level']
    maxExp = data['max_exp']
    exp = float((100 * currentExp) / maxExp)
    handleChatCommand("party Seviye: " + str(level) + " - Tecrube : %" + str("{:.2f}".format(exp)))

def inventorySpace():
    size = 0
    usingSpace = 0
    items = []
    items = get_inventory()['items'][12:]
    size = get_inventory()['size'] - 12
    if items != []:
        for item in items:
            if item != None:
                usingSpace += 1
    size -= 1
    usingSpace -= 1
    handleChatCommand("party Bos Alan " + str(size - usingSpace) + "  ---->  " + str(usingSpace) + "/" + str(size))

def checkJob():
    data = get_character_data()
    currentExp = data['job_current_exp']
    maxExp = data['job_max_exp']
    exp = float((100 * currentExp) / maxExp)
    handleChatCommand("party Job Exp: %" + str("{:.2f}".format(exp)))

def specialtyGoodsBox():
    i = 0
    j = 0
    pouch = get_job_pouch()
    items = []
    items = get_job_pouch()["items"]
    if items != []:
        for item in items:
            j = j + 1
            if item is not None:
                i = i + item["quantity"]
    handleChatCommand("party Specialty -> " + str(i) + " / " + str(j * 5))

def checkGuild():
    items = []
    items = get_guild_storage()['items']
    sunItems = [0 for i in range(11)]
    moonItems = [0 for i in range(10)]
    sosItems = [0 for i in range(10)]
    if items != []:
        for item in items:
            if item != None:
                if 'RARE' in item['servername'] and 'EVENT' not in item['servername'] and 'ARCHEMY' not in item[
                    'servername']:
                    # split = item['servername'].split('_')
                    log(item['servername'])
                    # dg = int(str(split[4]))
                    dg = [int(s) for s in item['servername'].split('_') if s.isdigit()][0]
                    if dg < 11:
                        if '_C_' in item['servername']:
                            sunItems[dg - 1] += 1
                        elif '_B_' in item['servername']:
                            moonItems[dg - 1] += 1
                        elif '_A_' in item['servername']:
                            sosItems[dg - 1] += 1
                    else:
                        if '_A_' in item['servername']:
                            sunItems[10] += 1
    i = 1
    for x in sunItems:
        log(str(i) + " " + str(x) + "\t")
        i = i + 1

def connected():
    global inGame
    inGame = None

def joined_game():
    loadConfigs()

def handle_chat(t, player, msg):
    if player and lstLeaders_exist(player) or t == 100:
        if msg == "ENV":
            inventorySpace()
        elif msg == "EXP":
            checkExp()
        elif msg == "JOBEXP":
            checkJob()
        elif msg == "GOLD":
            checkGold()
        elif msg == "ELIXIR":
            checkInv("Elixir")
        elif msg == "BLUE":
            checkInv("Blue")
        elif msg == "BLUE2":
            checkInv("Blue2")
        elif msg == "STAT":
            checkInv("Stat")
        elif msg == "STAT2":
            checkInv("Stat2")
        elif msg == "FLOWER":
            checkInv("Flower3") 
        elif msg == "PANDORA":
            checkInv("Pandora") 
        elif msg == "LUCK":
            checkInv("Luck") 
        elif msg == "STEADY":
            checkInv("Steady") 
        elif msg == "MS":
            checkInv("Ms") 
        elif msg == "ICE":
            checkInv("Cream") 
        elif msg == "ACC":
            checkInv("Accessory")
        elif msg == "LAMP":
            checkInv("Lamp")
        elif msg == "SOX":
            checkInv("Sox")
        elif msg == "COIN":
            checkInv("Coin")
        elif msg == "CATA":
            checkInv("Catalyst")
        elif msg == "FGW8DG":
            checkInv("fgw8dg")
        elif msg == "FGW9DG":
            checkInv("fgw9dg")
        elif msg == "FGW10DG":
            checkInv("fgw10dg")
        elif msg == "FGW11DG":
            checkInv("fgw11dg")
        elif msg == "FADED":
            checkInv("faded")

def CheckForUpdate():
	global NewestVersion
	#avoid request spam
	if NewestVersion == 0:
		try:
			req = urllib.request.Request('https://github.com/hakankahya48/DenemeEklenti/blob/main/xEsyaBildir.py', headers={'User-Agent': 'Mozilla/5.0'})
			with urllib.request.urlopen(req) as f:
				lines = str(f.read().decode("utf-8")).split()
				for num, line in enumerate(lines):
					if line == 'version':
						NewestVersion = int(lines[num+2].replace(".",""))
						CurrentVersion = int(str(version).replace(".",""))
						if NewestVersion > CurrentVersion:
							log('Plugin: Asağıdakiler için bir güncelleme var [%s]!' % name)
							lblUpdate = QtBind.createLabel(gui,'Mevcut bir Güncelleme Var, Güncellemek için Buraya Basın',100,283)
							button1 = QtBind.createButton(gui, 'button_update', ' Eklentiyi Güncelle ', 350, 280)
		except:
			pass

def button_update():
	path = get_config_dir()[:-7]
	if os.path.exists(path + "Plugins/" + "xEsyaBildir.py"):
		try:
			os.rename(path + "Plugins/" + "xEsyaBildir.py", path + "Plugins/" + "xEsyaBildirYEDEK.py")
			req = urllib.request.Request('https://github.com/hakankahya48/DenemeEklenti/blob/main/xEsyaBildir.py', headers={'User-Agent': 'Mozilla/5.0'})
			with urllib.request.urlopen(req) as f:
				lines = str(f.read().decode("utf-8"))
				with open(path + "Plugins/" + "xEsyaBildir.py", "w+") as f:
					f.write(lines)
					os.remove(path + "Plugins/" + "xEsyaBildirYEDEK.py")
					log('Plugin Basarıyla Güncellendi, Kullanmak için Eklentiyi Yeniden Yükleyin.')
		except Exception as ex:
			log('Güncelleme Hatası [%s] Lütfen Manuel Olarak Güncelleyin veya Daha Sonra Tekrar Deneyin.' %ex)

CheckForUpdate()
log("Plugin: "+pName+" v"+pVersion+" Yüklendi. // edit by hakankahya")

if os.path.exists(getPath()):
	loadConfigs()
else:
	os.makedirs(getPath())
	log('Plugin: '+pName+' klasörü olusturuldu.')
