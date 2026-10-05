import sys

#dict con 'CARTA': (azione, stazione)
#quando fa tapin controlla se carta è gia presente -> ERRORE GIA TAPPATO IN, altrimenti inserisci (carta: stazione,azione) e aggiungi al registro
#quando fa tapout controlla se c'è card -> ERRORE NON TAPPATO IN, altrimenti rimuovi la chiave_card e aggiungi al registro e aggiungi a fares


class Tapes():
    #dict con card:trip
    cards_trip={}

    #dizionario con ogni tap in quella stazione: [mario, gianni, gianni]
    register={} #usare per regulars

    #'card':(actions,station) dict con azioni per tracciare tap in e out 
    #assumo che se la carta c'è è tapin
    actions={}
    def __init__(self):
        self.register={'garibaldi':[],
                        'universita':[],
                        'municipio':[],
                        'toledo':[],
                        'dante':[],
                        'museo':[],
                        'materdei':[],
                        'vanvitelli':[],
                        'augusteo':[],
                        'fuga':[],
                        'mergellina':[],
                        'manzoni':[]}
        self.actions={}
        self.cards_trip={}
        self.fares={}

    def return_current_price_and_save(self, card):
        n_trips=int(self.cards_trip[card])
        if n_trips < 4 and n_trips > 0:
            price = 2
        if n_trips < 6 and n_trips > 3:
            price = 1
        if n_trips >= 6:
            price = '0'
        
        if self.fares.get(card) == None:
            self.fares[card]=int(price)
        else:
            self.fares[card]+=int(price)
        return price

    def tap_in(self,card: str, station: str):
        if self.actions.get(card) != None :
            return('ERROR already in')
        else:
            self.actions[card]=('TAPIN',station)
            if self.register.get(station,0) == 0 :
                # self.register[station]=[card] usare per regulars
                return ('OK')

            self.register[station].append(card)
            return ('OK')
    
    def tap_out(self, card: str, station:str):
        if self.actions.get(card) == None:
            return ('ERROR not in')
        else:
            self.register[station].append(card) # aggiungi al registro
            del self.actions[card]
            if self.cards_trip.get(card) != None:
                self.cards_trip[card]+=1
            else:
                self.cards_trip[card]=1
            return self.return_current_price_and_save(card)
    
    def pending(self):
        traveler=list(self.actions.keys())
        if len(traveler) == 0:
            return 'none'
        traveler.sort()
        string=''
        for person in traveler:
            string=string + ' ' + person
        return string
    
    def fare(self, card):
        if self.fares.get(card) == None:
            return '0'
        else:
            return self.fares[card]

class Parser():

    def __init__(self, tapes:Tapes):
        self.tapes=tapes
        self.possible_cmds={ 'TAPIN': (2, tapes.tap_in),
                             'TAPOUT': (2,tapes.tap_out),
                             'PENDING':(0,tapes.pending),
                             'FARE':(1,tapes.fare),
                             
                    }
        
        self.possible_stations=['garibaldi',
                        'universita',
                        'municipio',
                        'toledo',
                        'dante',
                        'museo',
                        'materdei',
                        'vanvitelli',
                        'augusteo',
                        'fuga',
                        'mergellina',
                        'manzoni']

    def parse(self, cmd : str):
        command_lst=cmd.split()
        command=command_lst[0]
        args=command_lst[1:]

        if command not in self.possible_cmds:
            return 'ERROR invalid command'
        else:
            n_args , funct = self.possible_cmds[command]
            if len(args) != n_args:
                return 'ERROR invalid command'
            else:
                if command == 'TAPIN':
                    if args[1] in self.possible_stations:
                        return funct(*args)
                    return('ERROR invalid command')
                if command == 'TAPOUT':
                    if args[1] in self.possible_stations:
                        return funct(*args)
                    return ('ERROR invalid command')
                if command == 'PENDING':
                    return funct()
                if command == 'FARE':
                    return funct(*args)

def main():
    tapes=Tapes()
    parser=Parser(tapes)

    for line in sys.stdin:
        result=parser.parse(line)
        if result:
            print(result)

main()