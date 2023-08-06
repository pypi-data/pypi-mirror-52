from kageku.flags import *
from kageku.consts import *
from kageku.action import *

class Board:
  def __init__(self):
    self.board = self.create_initial_board()
    self.actions = []
    self.piece_taken_last_move = []
    self.turn = WHITE

    self.piece_count = {NONE_PIECE: 0}
    for piece in [KING, QUEEN, ROOK, BISHOP, KNIGHT, PAWN]:
      for team in [WHITE, BLACK]:
        self.piece_count[(piece, team)] = 0

    for row in self.board:
      for piece in row:
        self.piece_count[piece] += 1

  def create_initial_board(self):
    return [
      [(KING, BLACK), NONE_PIECE, (ROOK, BLACK), NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE],
      [(PAWN, BLACK), (PAWN, BLACK), (PAWN, BLACK), NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE],
      [NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE],
      [NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE],
      [NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE],
      [NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE],
      [NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE, (PAWN, WHITE), (PAWN, WHITE), (PAWN, WHITE)],
      [NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE, NONE_PIECE, (ROOK, WHITE), NONE_PIECE, (KING, WHITE)]
    ]

  def available_actions(self, color=None):
    if color is None:
      color = self.turn

    actions = []

    player_pieces = {}
    for l, line in enumerate(self.board):
      for c, piece in enumerate(line):
        if piece[1] == color:
          player_pieces[(l, c)] = piece[0]
          if piece[0] == KING:
            player_king_pos = (l, c)

    addable_positions = self.get_addable_positions(player_king_pos, color)
    mana = self.get_player_mana(player_pieces, color)
    all_adds = self.create_all_adds(addable_positions, mana, color)

    movements = self.get_pieces_movements(player_pieces, color)

    for add in all_adds:
      actions.append(Action(add, color))

    for move in movements:
      move_str = self.int_pos_to_text_pos(move[0]) + self.int_pos_to_text_pos(move[1])
      actions.append(Action(move_str, color))

    return actions

  def get_player_mana(self, player_pieces, color=None):
    if color is None:
      color = self.turn

    has_own_field_pawn = False
    opp_field_pawn_count = 0
    for pos, piece in player_pieces.items():
      if piece == PAWN:
        if (pos[0] < 4 and color == WHITE) or (pos[0] >= 4 and color == BLACK):
          opp_field_pawn_count += 1
        elif not has_own_field_pawn:
          has_own_field_pawn = True

    return opp_field_pawn_count + (1 if has_own_field_pawn else 0)

  def create_all_adds(self, addable_positions, mana, color=None):
    if color is None:
      color = self.turn

    NO_ADD = "---"

    all_adds = []
    for pos in addable_positions:
      if (pos[0] < 4 and color == WHITE) or (pos[0] >= 4 and color == BLACK):
        continue

      curr_adds = []
      pos_repr = self.int_pos_to_text_pos(pos)
      if len(all_adds) == 0:
        all_adds = [NO_ADD]
        for piece, cost in PIECES_COST.items():
          if cost <= mana and self.piece_count[(PIECE_TEXT_TO_ID[piece], color)] < PIECES_MAX[piece]:
            new_line = pos_repr + piece
            all_adds.append(new_line)
      else:
        for line in all_adds:
          curr_mana = mana
          for i in range(0, len(line), 3):
            add_action = line[i: i + 3]
            if add_action != NO_ADD:
              curr_mana -= PIECES_COST[add_action[-1]]

          curr_adds.append(line[:] + NO_ADD)
          for piece, cost in PIECES_COST.items():
            if cost <= curr_mana and self.piece_count[(PIECE_TEXT_TO_ID[piece], color)] < PIECES_MAX[piece]:
              curr_adds.append(line[:] + pos_repr + piece)

        all_adds = curr_adds[:]

    return [i.replace(NO_ADD, "") for i in all_adds if len(i.replace(NO_ADD, "")) > 0]

  def get_pieces_movements(self, player_pieces, color=None):
    if color is None:
      color = self.turn

    color_up = 1 if color == BLACK else -1

    moves = []
    for pos, piece in player_pieces.items():
      if piece == PAWN:
        walk_pos = (pos[0] + color_up, pos[1])
        eat_pos = [(pos[0] + color_up, pos[1] - 1), (pos[0] + color_up, pos[1] + 1)]
        if self.is_valid_position(walk_pos) and self.get_piece_at(walk_pos) == NONE_PIECE:
          moves.append((pos, walk_pos))

        for eat in eat_pos:
          if self.is_valid_position(eat):
            eat_piece = self.get_piece_at(eat)
            if not eat_piece == NONE_PIECE and eat_piece[1] != color:
              moves.append((pos, eat))

      elif piece == ROOK or piece == BISHOP or piece == QUEEN:
        dirs = []

        if piece == ROOK:
          dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        elif piece == BISHOP:
          dirs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        elif piece == QUEEN:
          dirs = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]

        dirs_pos_searching = [True] * len(dirs)
        incr = 0
        while sum(dirs_pos_searching) > 0:
          incr += 1
          offsets = [(pos[0] + dir[0] * incr, pos[1] + dir[1] * incr) for dir in dirs]
          for npi, new_pos in enumerate(offsets):
            if self.is_valid_position(new_pos) and dirs_pos_searching[npi]:
              piece_at = self.get_piece_at(new_pos)
              if piece_at == NONE_PIECE or piece_at[1] != color:
                moves.append((pos, new_pos))
              if piece_at != NONE_PIECE:
                dirs_pos_searching[npi] = False
            else:
              dirs_pos_searching[npi] = False

      elif piece == KNIGHT or piece == KING:
        offsets = []

        if piece == KNIGHT:
          offsets = [(2, 1), (2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
        elif piece == KING:
          offsets = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]

        for offset in offsets:
          new_pos = (pos[0] + offset[0], pos[1] + offset[1])
          if self.is_valid_position(new_pos):
            piece_at = self.get_piece_at(new_pos)
            if piece_at[1] != color:
              moves.append((pos, new_pos))

    return moves

  def get_addable_positions(self, king_pos, color=None):
    if color is None:
      color = self.turn

    addable_positions = []
    position_status = {}
    unchecked_positions = [king_pos]
    for pos in unchecked_positions:
      adj = [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
      for adj_pos in adj:
        if self.is_valid_position(adj_pos):
          piece = self.get_piece_at(adj_pos)
          if piece == NONE_PIECE and adj_pos not in position_status:
            addable_positions.append(adj_pos)
            position_status[adj_pos] = True
          elif piece[1] == color and adj_pos not in position_status:
            unchecked_positions.append(adj_pos)
            position_status[adj_pos] = True

    return addable_positions

  def apply_action(self, action):
    if action.type == MOVE_ACTION:
      from_pos = self.text_pos_to_int_pos(action.details[0:2])
      to_pos = self.text_pos_to_int_pos(action.details[2:4])
      self.piece_taken_last_move.append(self.get_piece_at(to_pos))
      self.piece_count[NONE_PIECE] += 1
      self.piece_count[self.get_piece_at(to_pos)] -= 1
      self.set_piece_at(to_pos, self.get_piece_at(from_pos))
      self.set_piece_at(from_pos, NONE_PIECE)
    elif action.type == ADD_ACTION:
      adds = action.unpack_add_action_details()
      for add in adds:
        pos = self.text_pos_to_int_pos(add[0:2])
        piece = PIECE_TEXT_TO_ID[add[2].lower()]
        self.set_piece_at(pos, (piece, action.color))
        self.piece_count[NONE_PIECE] -= 1
        self.piece_count[(piece, action.color)] += 1

    self.actions.append(action)
    self.change_turn()

  def undo_last_action(self):
    if(len(self.actions) > 0):
      action = self.actions.pop()
      if action.type == MOVE_ACTION:
        from_pos = self.text_pos_to_int_pos(action.details[0:2])
        to_pos = self.text_pos_to_int_pos(action.details[2:4])
        piece_taken_by_move = self.piece_taken_last_move.pop()
        self.piece_count[NONE_PIECE] -= 1
        self.piece_count[piece_taken_by_move] += 1
        self.set_piece_at(from_pos, self.get_piece_at(to_pos))
        self.set_piece_at(to_pos, piece_taken_by_move)
      elif action.type == ADD_ACTION:
        adds = action.unpack_add_action_details()
        for add in adds:
          pos = self.text_pos_to_int_pos(add[0:2])
          piece = PIECE_TEXT_TO_ID[add[2].lower()]
          self.set_piece_at(pos, NONE_PIECE)
          self.piece_count[NONE_PIECE] += 1
          self.piece_count[(piece, action.color)] -= 1

      self.change_turn()

  def is_game_over(self):
    return (PAWN, WHITE) in self.board[0] or (PAWN, BLACK) in self.board[-1] or not self.both_kings_alive()

  def both_kings_alive(self):
    return self.piece_count[(KING, WHITE)] > 0 and self.piece_count[(KING, BLACK)] > 0

  def get_winner(self):
    if not self.is_game_over():
      return NO_COLOR
    else:
      if self.piece_count[(KING, BLACK)] == 0 or (PAWN, WHITE) in self.board[0]:
        return WHITE
      else:
        return BLACK

  def get_piece_at(self, pos):
    return self.board[pos[0]][pos[1]]

  def set_piece_at(self, pos, piece):
    self.board[pos[0]][pos[1]] = piece

  def text_pos_to_int_pos(self, str_pos):
    return (8 - int(str_pos[1]), ord(str_pos[0]) - 97)

  def int_pos_to_text_pos(self, int_pos):
    return chr(int_pos[1] + 97) + str(8 - int_pos[0])

  def change_turn(self):
    self.turn = WHITE if self.turn == BLACK else BLACK

  def is_valid_position(self, pos):
    return pos[0] >= 0 and pos[0] < 8 and pos[1] >= 0 and pos[1] < 8

  def __repr__(self):
    str_repr = ""
    for line in self.board:
      for piece in line:
        piece_repr = PIECE_ID_TO_TEXT[piece[0]] + " "
        piece_repr = piece_repr.upper() if piece[1] == WHITE else piece_repr.lower()
        str_repr += piece_repr
      str_repr += "\n"

    return str_repr
