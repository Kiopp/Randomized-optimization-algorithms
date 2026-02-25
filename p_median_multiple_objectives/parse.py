import math
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any

import numpy as np
import matplotlib.pyplot as plt



@dataclass
class Instance:
    instance_id: int
    best_known: float
    n: int
    p: int
    capacity: int
    customer_ids: np.ndarray
    xy: np.ndarray
    demand: np.ndarray


def load_instances(path: str) -> Dict[int, Instance]:
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    i = 0
    instances = {}
    while i < len(lines):
        head = lines[i].split()
        instance_id = int(head[0])
        best_known = float(head[1])
        i += 1

        n, p, cap = map(int, lines[i].split())
        i += 1

        ids, xy, dem = [], [], []
        for _ in range(n):
            cid, x, y, d = map(int, lines[i].split())
            ids.append(cid)
            xy.append((x, y))
            dem.append(d)
            i += 1

        instances[instance_id] = Instance(
            instance_id=instance_id,
            best_known=best_known,
            n=n,
            p=p,
            capacity=cap,
            customer_ids=np.array(ids, dtype=int),
            xy=np.array(xy, dtype=float),
            demand=np.array(dem, dtype=float),
        )

    return instances
