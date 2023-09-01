import json
from pathlib import Path

import json_hydrate_benchmark


class Landsat:
    def setup(self) -> None:
        data = Path(__file__).parents[1] / "tests" / "data"
        with open(data / "landsat-c2-l1.json") as f:
            self.base = json_hydrate_benchmark.base_item(json.load(f))
        with open(data / "dehydrated" / "LM04_L1GS_001001_19830527_02_T2.json") as f:
            self.item = json.load(f)

    def time_python(self) -> None:
        json_hydrate_benchmark.python(self.base, self.item)

    def time_serde_json(self) -> None:
        json_hydrate_benchmark.serde_json(self.base, self.item)
