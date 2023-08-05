from .base import *
from carball.generated.api.game_pb2 import mutators_pb2 as mutators
from carball.json_parser.actor_parsing import BallActor

BALL_TYPES = {
    'Archetypes.Ball.Ball_Default': mutators.DEFAULT,
    'Archetypes.Ball.Ball_Basketball': mutators.BASKETBALL,
    'Archetypes.Ball.Ball_Puck': mutators.PUCK,
    'Archetypes.Ball.CubeBall': mutators.CUBEBALL,
    'Archetypes.Ball.Ball_Breakout': mutators.BREAKOUT
}


class BallHandler(BaseActorHandler):

    @classmethod
    def can_handle(cls, actor: dict) -> bool:
        return actor['TypeName'].startswith('Archetypes.Ball.')

    def update(self, actor: dict, frame_number: int, time: float, delta: float) -> None:
        if actor.get('TAGame.RBActor_TA:bIgnoreSyncing', False):
            return

        if self.parser.game.ball_type is None:
            self.parser.game.ball_type = BALL_TYPES.get(actor['TypeName'], mutators.DEFAULT)

        ball_data = BallActor.get_data_dict(actor, self.parser.replay_version)
        self.parser.ball_data[frame_number] = ball_data
