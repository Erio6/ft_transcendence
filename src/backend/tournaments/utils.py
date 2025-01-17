from tournaments.models import TournamentGame


def create_games(tournament, player_slots, round_number, total_rounds, games):
    if round_number > total_rounds:
        return

    num_games = 2 ** (total_rounds - round_number) // 2
    # num_games = len(player_slots) // 2
    current_round_games = []

    for i in range(0, len(player_slots), 2):
        player_one = player_slots[i] if player_slots[i] else None
        player_two = player_slots[i + 1] if (i + 1) < len(player_slots) and player_slots[i + 1] else None
        # player_two = player_slots[i + 1].player if (i + 1) < len(player_slots) else None
        # player_two = player_slots[i + 1].player if player_slots[i + 1] else None
        # parent_games = parent_game[i // 2] if parent_game else None
        game = TournamentGame(
            tournament=tournament,
            round_number=round_number,
            player_one=player_one,
            player_two=player_two,
        )
        current_round_games.append(game)
        # games.append(game)
        # next_round_games.append(game)
    TournamentGame.objects.bulk_create(current_round_games)
    games.extend(current_round_games)

    # next_round_games = current_round_games
        # if parent_game:
        #     parent_game.next_game = game

    # next_round_slots = [None] * (num_games * 2)

    # if round_number < total_rounds:
    #     for i, game in enumerate(current_round_games):
    #         parent_index = i // 2
    #         next_round_slots[parent_index] = next_round_slots[parent_index] or TournamentGame(
    #             tournament=tournament,
    #             round_number=round_number + 1,
    #         )
    #         game.parent = next_round_slots[parent_index]
    #         game.save()

    next_round_slots = [None] * (num_games * 2)
    # for i, game in enumerate(current_round_games):
    #     if i // 2 < len(next_round_slots):
    #         next_round_slots[i // 2] = game

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

def assign_parent_child_relationships(games):
    # Group games by round
    rounds = {}
    for game in games:
        rounds.setdefault(game.round_number, []).append(game)

    # Sort rounds by round number
    sorted_rounds = sorted(rounds.items())

    # Assign parents for each game
    for i, (current_round, current_games) in enumerate(sorted_rounds[:-1]):
        next_round = sorted_rounds[i + 1][1]  # Get games for the next round

        # Assign each game in the current round to a parent in the next round
        for j, game in enumerate(current_games):
            parent_index = j // 2  # Parent is at half the index in the next round
            if parent_index < len(next_round):
                game.parent = next_round[parent_index]
                game.save()

    # Handle the final round (optional, depends on your logic)
    final_round_games = sorted_rounds[-1][1]
    for game in final_round_games:
        game.parent = game  # Self-reference for championship game
        game.save()