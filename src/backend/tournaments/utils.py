from tournaments.models import TournamentGame
from game.models import Game


def create_games(tournament, player_slots, round_number, total_rounds, games):
    if round_number > total_rounds:
        return

    # num_games = 2 ** (total_rounds - round_number) // 2
    num_games = (len(player_slots) + 1) // 2
    current_round_games = []
    next_round_slots = []
    for i in range(num_games):
        player_one = player_slots[i * 2] if i * 2 < len(player_slots) else None
        player_two = player_slots[i * 2 + 1] if i * 2 + 1 < len(player_slots) else None

        game_instance = None
        if player_one and player_two:
            print(f"Creating game for {player_one.player} and {player_two.player}")
            game_instance = Game.objects.create(
                player_one=player_one.player,
                player_two=player_two.player,
                player_one_score=0,
                player_two_score=0,
                type_of_game='tournament'
            )

        game = TournamentGame(
            tournament=tournament,
            round_number=round_number,
            player_one=player_one,
            player_two=player_two,
            game=game_instance
        )
        current_round_games.append(game)

        if player_one and player_two:
            next_round_slots.append(None)
        else:
            next_round_slots.append(player_one or player_two)

    print(f"Round {round_number}: {[(game.player_one, game.player_two, game.game) for game in current_round_games]}")

    TournamentGame.objects.bulk_create(current_round_games)
    games.extend(current_round_games)


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

