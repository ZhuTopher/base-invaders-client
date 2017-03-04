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
            data = self.server.recv(4096)
            if data:
                return data.decode('utf-8')
            else:
                raise "you dumb"
        except:
            raise "you dumb"

    def parseScan(self, words, response_dict=dict()):
        cur_index = 1
        num_mines = int(words[cur_index])
        mine_lst = []
        # iterate over mines (owner, x, y)
        for i in range(cur_index + 1, cur_index + 1 + num_mines * 3, 3):
            mine_lst.append((words[i], float(words[i + 1]), float(words[i + 2])))

        response_dict['mines'] = mine_lst

        cur_index = cur_index + 1 + num_mines * 3 + 1
        num_players = int(words[cur_index])
        player_lst = []
        # iterate over player
        for i in range(cur_index + 1, cur_index + 1 + num_players * 4, 4):
            player_lst.append((float(words[i]), float(words[i + 1]), float(words[i + 2]), float(words[i + 3])))

        response_dict['players'] = player_lst

        cur_index = cur_index + 1 + num_players * 4 + 1
        num_bombs = int(words[cur_index])
        bomb_lst = []
        for i in range(cur_index + 1, cur_index + 1 + num_bombs * 2, 2):
            player_lst.append((float(words[i]), float(words[i + 1])))
        response_dict['bombs'] = bomb_lst

        return response_dict

    def parseStatus(self, words):
        response_dict = dict()
        response_dict['x'] = float(words[1])
        response_dict['y'] = float(words[2])
        response_dict['dx'] = float(words[3])
        response_dict['dy'] = float(words[4])
        return self.parseScan(words[5:], response_dict)

    def getStatus(self):
        self.server.send('STATUS')
        return self.parseStatus(self.receive().split())

    def accelerate(self, rad, accel):
        self.server.send('ACCELERATE ' + str(rad) + ' ' + str(accel))
        return self.receive()

    def stop(self):
        self.server.send('BRAKE')
        return self.receive()

    def bomb(self, x, y, *args):
        if args:
            self.server.send('BOMB ' + str(x) + ' ' + str(y) + ' ' + str(args[0]))
        else:
            self.server.send('BOMB ' + str(x) + ' ' + str(y))
        resp = self.receive()
        if "ERROR" in resp:
            raise Exception("Bomb too soon")
        return resp

    def scan(self, x, y):
        self.server.send('SCAN ' + str(x) + ' ' + str(y))
        resp = self.receive()
        if "ERROR" in resp:
            raise Exception("Scanning too soon")
        return self.parseScan(resp.split()[1:])

    def scoreboard(self):
        # (name, score, mines)
        self.server.send('SCOREBOARD')
        words = self.receive().split()
        print len(words)
        scores = []
        for i in range(1, len(words), 3):
            scores.append((words[i], int(words[i + 1]), int(words[i + 2])))
        return scores

    def configurations(self):
        self.server.send('CONFIGURATIONS')
        words = self.receive().split()
        response_dict = dict()
        response_dict['map_width'] = float(words[2])
        response_dict['map_height'] = float(words[4])
        response_dict['capture_radius'] = float(words[6])
        response_dict['vision_radius'] = float(words[8])
        response_dict['friction'] = float(words[10])
        response_dict['brake_friction'] = float(words[12])
        response_dict['bomb_place_radius'] = float(words[14])
        response_dict['bomb_effect_radius'] = float(words[16])
        response_dict['bomb_delay'] = int(words[18])
        response_dict['bomb_power'] = float(words[20])
        response_dict['scan_radius'] = float(words[22])
        response_dict['scan_delay'] = float(words[24])
        return response_dict
