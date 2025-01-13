from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404

from tournaments.models import Tournament, TournamentPlayer

class TournamentConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.tournament_id = self.scope['url_route']['kwargs'].get("tournament_id")
        self.tournament_group_name = f'tournament_{self.tournament_id}'

        await self.channel_layer.group_add(
            self.tournament_group_name,
            self.channel_name
        )
        tournament = await sync_to_async(Tournament.objects.get)(id=self.tournament_id)

        players = await self.get_current_players()
        await self.channel_layer.group_send(
            self.tournament_group_name,
            {
                'type': 'tournament_update',
                'players': players,
                'connected_count': len(players),
            }
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.tournament_group_name,
            self.channel_name
        )

    async def receive_json(self, content):
        if content['type'] == 'player_join':
            tournament = await sync_to_async(get_object_or_404)(Tournament, id=self.tournament_id)
            players = await self.get_current_players()
            await self.channel_layer.group_send(
                self.tournament_group_name,
                {
                    'type': 'tournament_update',
                    'players': players,
                }
            )

        if content['type'] == 'start_tournament':
            tournament = await sync_to_async(get_object_or_404)(Tournament, id=self.tournament_id)
            if self.scope["user"].userprofile != tournament.created_by:
                await self.send_json({"error": "You are not the creator of this tournament. Only the creator can start the tournament."})
                return
            await self.channel_layer.group_send(
                self.tournament_group_name,
                {
                    'type': 'start_tournament',
                    'message': 'Tournament started!',
                }
            )

    async def tournament_update(self, event):
        players = event['players']
        is_ready = len(players) >= 4
        await self.send_json({
            'type': 'tournament_update',
            'players': event['players'],
            'connected_count': event.get('connected_count'),
            'ready_to_start': is_ready,
        })

    async def send_update(self, event):
        await self.send_json(event['content'])


    @sync_to_async
    def get_current_players(self):
        tournament = Tournament.objects.get(id=self.tournament_id)
        return [{"id": player.id, "name":player.player.display_name} for player in tournament.tournamentplayer_set.all()]

    async def player_join(self, event):
        await self.send_update(event['content'])