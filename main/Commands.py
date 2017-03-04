import socket
import sys


class Commands:
    host = 'localhost'
    port = 6060

    def __init__(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print 'Failed to create socket'
            sys.exit()

        try:
            remote_ip = socket.gethostbyname(self.host)
            self.server.connect((self.host, self.port))
        except socket.gaierror:
            print 'Hostname could not be resolved. Exiting'
            sys.exit()

        print 'Socket Connected to ' + self.host + ' on ip ' + remote_ip


    def receive(self):
        try:
            data = self.server.recv(2048)
            if data:
                return data.decode('utf-8')
            else:
                raise "you dumb"
        except:
            raise "you dumb"

    def parseStatus(self, response):
        words = response.split()
        response_dict = dict()
        response_dict['x'] = words[1]
        response_dict['y'] = words[2]
        response_dict['dx'] = words[3]
        response_dict['dy'] = words[4]
        cur_index = 6
        num_mines = int(words[cur_index])
        mine_lst = []
        # iterate over mines (owner, x, y)
        for i in range(cur_index + 1, cur_index + 1 + num_mines * 3, 3):
            mine_lst.append((words[i], words[i + 1], words[i + 2]))

        response_dict['mines'] = mine_lst

        cur_index = cur_index + 1 + num_mines * 3 + 1
        num_players = int(words[cur_index])
        player_lst = []
        # iterate over player
        for i in range(cur_index + 1, cur_index + 1 + num_players * 4, 4):
            player_lst.append((words[i], words[i + 1], words[i + 2], words[i + 3]))
        response_dict['players'] = player_lst

        cur_index = cur_index + 1 + num_players * 4 + 1
        num_bombs = int(words[cur_index])
        bomb_lst = []
        for i in range(cur_index + 1, cur_index + 1 + num_bombs * 2, 2):
            player_lst.append((words[i], words[i + 1]))
        response_dict['bombs'] = bomb_lst

        return response_dict


    def getStatus(self):
        self.server.send('STATUS')
        return self.parseStatus(self.receive())


    def accelerate(self, rad, accel):
        self.server.send('ACCELERATE ' + str(rad) + ' ' + str(accel))


    def stop(self):
        self.server.send('BREAK')

    def scan(self, x, y, *args):
        if args:
            self.server.send('SCAN ' + str(x) + ' ' + str(y) + ' ' + args[0])
        else:
            self.server.send('SCAN ' + str(x) + ' ' + str(y))


    def scoreboard(self):
        self.server.send('SCOREBOARD')
        words = self.receive().split()
        scores = []
        for i in range(1, len(words) + 1, 3):
            scores.append((words[i], words[i + 1], words[i + 2]))
        return scores


    def configurations(self):
        self.server.send('CONFIGURATIONS')
        words = self.receive().split()
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
