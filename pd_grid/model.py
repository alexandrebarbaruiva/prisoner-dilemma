import mesa

from .agent import PDAgent


def get_proportion(model):
    defecting = get_num_defecting(model)
    if defecting == 0:
        return 100
    cooperating = get_num_cooperating(model)
    alive = get_num_alive(model)
    return (cooperating - defecting) / alive


def get_num_alive(model):
    alive = 0
    for agent in model.schedule.agents:
        if agent.isAlive:
            alive += 1
    return alive


def get_num_defecting(model):
    defecting = 0
    for agent in model.schedule.agents:
        if not agent.isCooperating and agent.isAlive:
            defecting += 1
    return defecting


def get_num_cooperating(model):
    cooperating = 0
    for agent in model.schedule.agents:
        if agent.isCooperating and agent.isAlive:
            cooperating += 1
    return cooperating


class PdGrid(mesa.Model):
    """Model class for iterated, spatial prisoner's dilemma model."""

    schedule_types = {
        "Sequential": mesa.time.BaseScheduler,
        "Random": mesa.time.RandomActivation,
        "Simultaneous": mesa.time.SimultaneousActivation,
    }

    # This dictionary holds the payoff for this agent,
    # keyed on: (my_move, other_move)

    def __init__(
        self,
        width=50,
        height=50,
        schedule_type="Random",
        cooperation_reward=1,
        defected_reward=-0.5,
        defection_reward=1.5,
        mutual_defection_reward=-1,
        seed=None,
    ):
        """
        Create a new Spatial Prisoners' Dilemma Model.

        Args:
            width, height: Grid size. There will be one agent per grid cell.
            schedule_type: Can be "Sequential", "Random", or "Simultaneous".
                           Determines the agent activation regime.
            payoffs: (optional) Dictionary of (move, neighbor_move) payoffs.
        """
        self.payoff = {
            ("C", "C"): cooperation_reward,
            ("C", "D"): defected_reward,
            ("D", "C"): defection_reward,
            ("D", "D"): mutual_defection_reward,
        }
        self.grid = mesa.space.SingleGrid(width, height, torus=True)
        self.schedule_type = schedule_type
        self.schedule = self.schedule_types[self.schedule_type](self)

        # Create agents
        for x in range(width):
            for y in range(height):
                agent = PDAgent((x, y), self)
                self.grid.place_agent(agent, (x, y))
                self.schedule.add(agent)
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Cooperating": get_num_cooperating,
                "Defecting": get_num_defecting,
                "Proportion": get_proportion,
            },
        )

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        proportion = get_proportion(self)
        if proportion == 0 or proportion == 1 or self.step == 100:
            self.running = False

    def run(self, n):
        """Run the model for n steps."""
        for _ in range(n):
            self.step()
