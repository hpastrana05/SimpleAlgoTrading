import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from signals.entry_exit_signals import *


SIGNAL_REGISTRY = {
    "ema_cross_above": ema_cross_above,
    "ema_cross_below": ema_cross_below,
}


class FunctionSignal:
    def __init__(self, fn, params: dict):
        self.fn = fn
        self.params = params
    
    def evaluate(self, data) -> bool:
        return self.fn(data, **self.params)


class AND:
    def __init__(self, *signals):
        self.signals = signals
    
    def evaluate(self, data) -> bool:
        return all(s.evaluate(data) for s in self.signals)



class OR:
    def __init__(self, *signals):
        self.signals = signals
    
    def evaluate(self, data) -> bool:
        return any(s.evaluate(data) for s in self.signals)

def build_signal(config: dict):
    t = config["type"]

    if t == "AND":
        return AND(*[build_signal(s) for s in config["signals"]])
    if t == "OR":
        return OR(*[build_signal(s) for s in config["signals"]])

    # Leaf signal — pass all keys except "type" as params
    if t in SIGNAL_REGISTRY:
        params = {k: v for k, v in config.items() if k != "type"}
        return FunctionSignal(SIGNAL_REGISTRY[t], params)

    raise ValueError(f"Unknown signal type: {t}")