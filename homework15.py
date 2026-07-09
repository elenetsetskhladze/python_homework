class FootballTeam:

    def __init__(self, team_name, coach):
        self.team_name = team_name
        self.coach = coach
        self.players = []

    def add_player(self, name, possition, number, age, nationality):
        player = {
                  "name" : name,
                  "possition" : possition,
                  "number" : number,
                  "age" : age,
                  "nationality" : nationality
        }
        self.players.append(player)
        print(f"{name} added")


    def remove_player(self, number):
        for player in self.players:
            if player ["number"] == number:
                self.players.remove(player)
                print("player removed")
                return
            
        print("player not found")   
            
    def update_player(self, number, key, value):
        for player in self.players:
            if player["number"] == number:
                player[key] = value
                print("Player information updated!")
                return
        print("Player not found!")

    def show_info(self):
        print(f"team: {self.team_name}")
        print(f"coach: {self.coach}") 
        print("players:")
        for player in self.players:
            print(player)

    def show_player_info(self, number):
        for player in self.players:
            if player["number"] == number:
                print(player)
                return
        print("player not found")


    
         


    
    
            

            



