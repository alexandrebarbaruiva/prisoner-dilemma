import mesa

from .portrayal import portrayPDAgent
from .model import PdGrid


# Make a world that is 50x50, on a 500x500 display.
canvas_element = mesa.visualization.CanvasGrid(portrayPDAgent, 50, 50, 500, 500)

model_params = {
    "height": 50,
    "width": 50,
    "schedule_type": mesa.visualization.Choice(
        "Scheduler type",
        value="Random",
        choices=list(PdGrid.schedule_types.keys()),
    ),
    "cooperation_reward": mesa.visualization.Slider(
        name="Cooperation Reward",
        value=1,
        min_value=-5,
        max_value=5,
        description="Cooperation Reward",
    ),
    "defected_reward": mesa.visualization.Slider(
        name="Defected Reward",
        value=1,
        min_value=-5,
        max_value=5,
        description="Defected Reward",
    ),
    "defection_reward": mesa.visualization.Slider(
        name="Defection Reward",
        value=1,
        min_value=-5,
        max_value=5,
        description="Defection Reward",
    ),
    "mutual_defection_reward": mesa.visualization.Slider(
        name="Mutual Defection Reward",
        value=1,
        min_value=-5,
        max_value=5,
        description="Mutual Defection Reward",
    ),
}

chart = mesa.visualization.ChartModule(
    [
        {"Label": "Cooperating", "Color": "blue"},
        {"Label": "Defecting", "Color": "red"},
    ]
)

proportion_chart = mesa.visualization.ChartModule(
    [
        {"Label": "Proportion", "Color": "green"},
    ]
)

server = mesa.visualization.ModularServer(
    PdGrid,
    [canvas_element, chart, proportion_chart],
    "Prisoner's Dilemma",
    model_params,
)
