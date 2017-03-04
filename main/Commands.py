class Commands:

    def __init__(self, connection_endpoint, username, password):
        server = os.
        server.send(username + ' ' + password)

    def parseStatus(self, response):
        words = response.split()
        response_dict = dict()
        response_dict['x'] = words[1]
        response_dict['y'] = words[2]
        response_dict['dx'] = words[3]
        response_dict['dy'] = words[4]
        num_mines = words[6]
        mine_lst = []
        # iterate over mines (owner, x, y)
        for i in range(7, 7 + num_mines * 3, 3):
            mine_lst.append((words[i], words[i+1], words[i+2]))

        response_dict['mines'] = mine_lst
        cur_index = 7 + num_mines * 3
        num_players = words[cur_index + 1]
        player_lst = []
        for i in range(cur_index + 2, cur_index + num_players * 4, 4):
            player_lst.append((words[i], words[i+1], words[i+2], words[i+3]))
        response_dict['players'] = player_lst

        cur_index = cur_index + num_players * 4
        num_bombs = words[cur_index + 1]
        bomb_lst = []
        for i in range(cur_index + 2, cur_index + num_players * 2, 2):
            player_lst.append((words[i], words[i+1]))
        response_dict['bombs'] = bomb_lst

        return response_dict

    def getStatus(self):
        response = server.send('STATUS')
        return self.parseStatus(response)

    def accelerate(self, rad, accel):
        server.send('ACCELERATE ' + str(rad) + str(accel))

    def break(self):
        server.send('BREAK')

    def scan(self, x, y, *args):
        if args:
            server.send('SCAN ' + str(x) + ' ' + str(y) + args[0]
        else:
            server.send('SCAN ' + str(x) + ' ' + str(y)

    def scan(self, x, y):
        response = server.send('SCAN ' + str(x) + ' ' + str(y))
        return self.parseStatus(response)

    def scoreboard(self):
        response = server.send('SCOREBOARD')
        words = response.split()
        scores = []
        for i in range(1, len(words) + 1, 3):
            scores.append((words[i], words[i+1], words[i+2]))
        return scores

    def configurations(self):
        response = server.send('CONFIGURATIONS')
        words = response.split()
        response_dict = dict()
        response_dict['map_width'] = words[1]
        response_dict['map_height'] = words[3]
        response_dict['capture_radius'] = words[5]
        response_dict['vision_radius'] = words[7]
        response_dict['friction'] = words[9]
        response_dict['brake_friction'] = words[11]
        response_dict['bomb_place_radius'] = words[13]
        response_dict['bomb_effect_radius'] = words[15]
        response_dict['bomb_delay'] = words[17]
        response_dict['bomb_power'] = words[19]
        response_dict['scan_radius'] = words[21]
        response_dict['scan_delay'] = words[23]
        return response_dict
