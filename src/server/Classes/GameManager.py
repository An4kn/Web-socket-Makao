# class GameManager:
#     """Klasa zarządzająca grami."""
#     def __init__(self):
#         self.games = {}  # Słownik do przechowywania gier po ID

#     def create_game(self, game_id):
#         """Tworzenie nowej gry i zapisanie jej w słowniku."""
#         game = Game()
#         self.games[game_id] = game
#         return game

#     def get_game(self, game_id):
#         """Pobranie gry na podstawie ID."""
#         return self.games.get(game_id)

#     def delete_game(self, game_id):
#         """Usunięcie gry z pamięci."""
#         if game_id in self.games:
#             del self.games[game_id]
#             return True
#         return False


# # Przykład użycia:
# game_manager = GameManager()

# # Tworzymy nową grę o ID 1
# game1 = game_manager.create_game(1)

# # Tworzymy kolejną grę o ID 2
# game2 = game_manager.create_game(2)

# # Pobieramy grę o ID 1
# game = game_manager.get_game(1)
# if game:
#     print(f"Gra o ID 1 istnieje: {game}")
# else:
#     print("Gra o ID 1 nie istnieje.")

# # Usuwamy grę o ID 2
# game_manager.delete_game(2)
