import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend

n = 6411 # 226
d = 52.1 # 25

# Erdos Renyi
g = nx.erdos_renyi_graph(n,d/n)
# Preferential Attachment
#g = nx.barabasi_albert_graph(n, round(d/2))

# Model selection
model  = ep.SIRModel(g)

# Model Configuration
cfg = mc.Configuration()
cfg.add_model_parameter('beta', 0.00025)                   # Infection probability     S -> I
cfg.add_model_parameter('gamma', 0.0025)                   # Removal probability       I -> R
cfg.add_model_parameter("fraction_infected", 0.0005)       # Infected nodes at start in the network 
model.set_initial_status(cfg)

# Simulation execution
iterations = model.iteration_bunch(1000)
trends = model.build_trends(iterations)

# Show simulation
viz = DiffusionTrend(model, trends)
viz.plot("diffusion")