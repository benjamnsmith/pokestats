import requests, json

def typeSearch(name):
    r = requests.get("https://pokeapi.co/api/v2/type/{}/".format(name))

    dat = json.loads(r.text)

    print("\n========== {} TYPE SUMMARY ==========".format(dat['name'].upper()))

    for element in dat['damage_relations'].keys():
        if len(dat['damage_relations'][element]) != 0:
            print(element.capitalize().replace("_", " "))
            for i in range(len(dat['damage_relations'][element])):
                print("*", dat['damage_relations'][element][i]['name'].capitalize())
            print()

    print()
    print("There are {} {} type pokemon\n".format(len(dat['pokemon']), dat['name']))

def printHelp(base, nm):
    if base['species']['name'] == nm:
        print("(*)", end=" ")
    print("{:>}".format(base['species']['name'].capitalize()), end="")
    if base['evolution_details'] and base['evolution_details'][0]['item']:
        print(" ({})".format(base['evolution_details'][0]['item']['name'].replace("-", " ")), end="")        
    print()
    if not base['evolves_to']:
        return
    else:
        for i in range(len(base['evolves_to'])):
            printHelp(base['evolves_to'][i], nm)


def evolutionPrinter(info, nm):
    print("\nEvolution chain")
    r3 = requests.get(info)
    ev_dat = json.loads(r3.text)
    
    base = ev_dat['chain']
    printHelp(base, nm)


def nameSearch(name):
    name = input(">> ").replace(" ", "-").lower()

    r1 = requests.get("https://pokeapi.co/api/v2/pokemon/{}/".format(name))
    r2 = requests.get("https://pokeapi.co/api/v2/pokemon-species/{}/".format(name))

    try:
        dat = json.loads(r1.text)
        dat_2 = json.loads(r2.text)
    except:
        print("Could not get data for '{}'".format(name))
        return
    print(dat.keys())
    print(dat_2.keys())

    print("\n========== {} SUMMARY ==========".format(dat['name'].upper()))
    print("{} is a generation {} {}-type pokemon.".format(dat['name'].capitalize().replace("-", " "), dat_2['generation']['name'].split("-")[1].upper(), dat['types'][0]['type']['name']))

    evolutionPrinter(dat_2['evolution_chain']['url'], dat['name'])

    print()

    print("Legendary?", dat_2["is_legendary"])
    print("Mythical?", dat_2["is_mythical"])
    print("Catch probability {:.2f}%\n".format(dat_2['capture_rate']/255*100))

    print()

    print("Abilities")
    prev = ""
    for i in range(len(dat['abilities'])):
        if (dat['abilities'][i]['ability']['name'] != prev):
            print(dat['abilities'][i]['ability']['name'].replace("-", " ").capitalize())
            ability_dat = json.loads(requests.get(dat['abilities'][i]['ability']['url']).text)
            if ability_dat['effect_entries']:
                print("  {}".format(ability_dat['effect_entries'][1]['short_effect']))
            prev = dat['abilities'][i]['ability']['name']
            if dat['abilities'][i]['is_hidden']:
                print(" *this is a hidden ability!*")



def main():
    print("\n========== POKEMON SEARCH ==========")
    while 1:
        print("\nEnter 'name' or 'type' followed by the name or type you'd like to search")
        inp = input(">> ").split()

        if inp[0] == "type":
            typeSearch(inp[1].lower())
        elif inp[0] == "name":
            nameSearch(inp[1:].join("-"))
        elif inp[0] == "q":
            break
        else:
            print("choice not recognized")

main()