class Player:
    # Creating a set of signs so none could have the other's
    signs_set = set()

    def __init__(self, sign, name):
        self.sign = sign
        self.name = name
        self.wins = 0

    @staticmethod
    def create_player():
        name = None
        sign = None
        while name is None:
            name = input("Please, enter the player's name\n")
            while sign is None or sign == ' ' or sign in Player.signs_set:
                sign = input("Please, input the player's sign (not a space) and not like the other ones\n")
        Player.signs_set.add(sign)
        return Player(sign, name)


class Game:

    def __init__(self, players, rows=3, cols=4):
        self.rows = rows
        self.cols = cols
        self.players = players
        self.board = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]

    def print_board(self):
        for row in self.board:
            print('|'.join(row))
        print('—' * (len(row) * 2 - 1))

    def check_winner(self, row, col, player_sign):
        # Check horizontally
        for c in range(col - 3, col + 1):
            if 0 <= c <= len(self.board[0]) - 4:
                if all(self.board[row][c + i] == player_sign for i in range(4)):
                    return True

        # Check vertically
        for r in range(row - 3, row + 1):
            if 0 <= r <= len(self.board) - 4:
                if all(self.board[r + i][col] == player_sign for i in range(4)):
                    return True

        # Check diagonally (up-right)
        for i in range(-3, 1):
            if (0 <= row + i <= len(self.board) - 4) and (0 <= col + i <= len(self.board[0]) - 4):
                if all(self.board[row + i + j][col + i + j] == player_sign for j in range(4)):
                    return True

        # Check diagonally (up-left)
        for i in range(-3, 1):
            if (0 <= row + i <= len(self.board) - 4) and (0 <= col - i <= len(self.board[0]) - 4):
                if all(self.board[row + i + j][col - i - j] == player_sign for j in range(4)):
                    return True

        return False

    def is_full(self):
        return all(cell != ' ' for row in self.board for cell in row)

    def start_game(self):
        curr_index = 0
        curr_player = self.players[curr_index]

        while True:
            self.print_board()
            print(f"{curr_player.name}'s turn")

            try:
                col = int(input(f"Enter column (0-{self.cols - 1}): "))
                if 0 <= col < self.cols and self.board[0][col] == ' ':
                    for row in range(self.rows - 1, -1, -1):
                        if self.board[row][col] == ' ':
                            self.board[row][col] = curr_player.sign
                            break
                else:
                    print("Invalid move. Try again.")
                    continue
            except ValueError:
                print(f"Invalid input. Enter a valid column (0-{self.cols - 1}).")
                continue

            if self.check_winner(row, col, curr_player.sign):
                self.print_board()
                print(f"Player {curr_player.name} wins!")
                curr_player.wins += 1
                break
            elif self.is_full():
                self.print_board()
                print("It's a tie!")
                break

            curr_index = curr_index + 1 if curr_index + 1 < len(self.players) else 0

            curr_player = self.players[curr_index]


if __name__ == "__main__":

    PLAYERS = 2
    players_list = []
    for i in range(PLAYERS):
        player = Player.create_player()
        players_list.append(player)

    is_ended = False

    while not is_ended:
        game = Game(players_list)
        game.start_game()

        for player in players_list:
            print(f'{player.name} won {player.wins} games!')

        print('Do you want to exit?')
        is_ended = input("Enter 'Yes' to leave, anything else -- to continue\n").upper() == "YES"
