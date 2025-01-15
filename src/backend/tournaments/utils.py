from tournaments.models import TournamentGame


def create_games(tournament, player_slots, round_number, total_rounds, games, parent_game=None):
    if round_number > total_rounds:
        return

    num_games = 2 ** (total_rounds - round_number) // 2
    next_round_games = []
    for i in range(0, len(player_slots), 2):
        player_one = player_slots[i].player if player_slots[i] else None
        player_two = player_slots[i + 1].player if player_slots[i + 1] else None
        game = TournamentGame(
            tournament=tournament,
            round_number=round_number,
            player_one=player_one,
            player_two=player_two,
        )
        games.append(game)
        next_round_games.append(game)

        if parent_game:
            parent_game.next_game = game

    next_round_slots = [None] * (num_games * 2)
    create_games(tournament, next_round_slots, round_number + 1, total_rounds, games)



def generate_links(games, tournament):
    links = []
    games_by_round = {}

    # Group games by round
    for game in games:
        if game.round_number not in games_by_round:
            games_by_round[game.round_number] = []
        games_by_round[game.round_number].append(game)

    # Create links between games
    for round_number in range(1, len(games_by_round)):
        current_round_games = games_by_round[round_number]
        next_round_games = games_by_round.get(round_number + 1, [])

        for i, game in enumerate(current_round_games):
            if i // 2 < len(next_round_games):
                next_game = next_round_games[i // 2]
                links.append({"from": f"match-{game.id}", "to": f"match-{next_game.id}"})

    return links
    # links = []
    # for game in games:
    #     if game.player_one:
    #         links.append(
    #             {"from": f"player-{game.player_one.id}",
    #              "to": f"match-{game.id}"})
    #     if game.player_two:
    #         links.append(
    #             {"from": f"player-{game.player_two.id}",
    #              "to": f"match-{game.id}"})
    #
    #     if game.winner:
    #         next_match = TournamentGame.objects.filter(tournament=tournament, round_number=game.round_number + 1).first()
    #         if next_match:
    #             links.append(
    #                 {"from": f"match-{game.id}",
    #                  "to": f"match-{next_match.id}"})
    # return links