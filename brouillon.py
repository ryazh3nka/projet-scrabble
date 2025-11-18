'''
def echanger(jetons, main, sac):
    if len(sac) < len(jetons) or len(sac) == 0:
        return False
    for jeton in jetons:
        if jeton not in main:
            return False
    jetons_supprimes = []
    for elem in jetons:
        main.remove(elem)
        jetons_supprimes.append(elem)
    completer_main(main, sac)
    sac += jetons_supprimes
    return True

def echanger(jetons, main, sac):
    if len(sac) < len(jetons) or len(sac) == 0:
        return False
    for jeton in jetons:
        if jeton not in main:
            return False
    
    ind_jetons_supprimes = []
    for i in range(len(jetons)):
        ind_jetons_supprimes.append(main.find(jetons[i]))

    jetons_pioches = piocher(len(ind_jetons_supprimes, sac))
    for i in range(len(ind_jetons_supprimes)):
        main[ind_jetons_supprimes[i]] = jetons_pioches[i]
    sac += jetons_supprimes
    return True
'''  

def asdasd(mot, ll):
    ll_copy = list(ll)
    lettres_supprimes = []
    i = 0
    while i < len(ll_copy):
        if ll_copy[i] in mot:
            lettres_supprimes.append(ll_copy.pop(i))
        i += 1
    if len(lettres_supprimes) + len(ll_copy) == len(mot):
        return True
    return False
            
mot = input()
ll = input()
print(asdasd(mot, ll))