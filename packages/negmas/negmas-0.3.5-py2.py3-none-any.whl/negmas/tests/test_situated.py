from typing import (
    List,
    Optional,
    Tuple,
    Dict,
    Any,
    Union,
    Callable,
    Set,
    Iterable,
    Collection,
)

import pytest

from negmas import (
    Issue,
    AspirationNegotiator,
    LinearUtilityAggregationFunction,
    Mechanism,
    Negotiator,
    SAOMechanism,
    Mechanism,
    Negotiator,
    RenegotiationRequest,
    AgentMechanismInterface,
    MechanismState,
    MappingUtilityFunction,
)
from negmas.helpers import ConfigReader
from negmas.situated import World, Agent, Action, Breach, Contract


results = []  # will keep results not to use printing


class DummyWorld(World):
    def complete_contract_execution(
        self, contract: Contract, breaches: List[Breach], resolved: bool
    ) -> None:
        pass

    def get_contract_finalization_time(self, contract: Contract) -> int:
        return self.current_step + 1

    def get_contract_execution_time(self, contract: Contract) -> int:
        return self.current_step

    def contract_size(self, contract: Contract) -> float:
        return 0.0

    def __init__(self, n_steps=10000, negotiation_speed=20):
        super().__init__(
            n_steps=n_steps,
            negotiation_speed=negotiation_speed,
            neg_n_steps=10,
            neg_time_limit=10,
        )
        self.the_agents = []

    def join(self, x: "Agent", simulation_priority: int = 0):
        super().join(x=x, simulation_priority=simulation_priority)
        self.the_agents.append(x)

    def delete_executed_contracts(self) -> None:
        pass

    def executable_contracts(self) -> Collection[Contract]:
        return []

    def post_step_stats(self):
        pass

    def pre_step_stats(self):
        pass

    def order_contracts_for_execution(
        self, contracts: Collection[Contract]
    ) -> Collection[Contract]:
        return contracts

    def contract_record(self, contract: Contract) -> Dict[str, Any]:
        return contract.__dict__

    def start_contract_execution(self, contract: Contract) -> Set[Breach]:
        return set()

    def _process_breach(
        self, contract: Contract, breaches: List[Breach], force_immediate_signing=True
    ) -> Optional[Contract]:
        return None

    def breach_record(self, breach: Breach):
        return breach.__dict__

    def execute_action(
        self, action: Action, agent: "Agent", callback: Callable = None
    ) -> bool:
        return True

    def get_private_state(self, agent: "Agent") -> Any:
        s = {"partners": [_ for _ in self.the_agents if _ is not agent]}
        return s

    def simulation_step(self):
        pass


class DummyAgent(Agent):
    def init(self):
        pass

    def _respond_to_negotiation_request(
        self,
        initiator: str,
        partners: List[str],
        issues: List[Issue],
        annotation: Dict[str, Any],
        mechanism: AgentMechanismInterface,
        role: Optional[str],
        req_id: Optional[str],
    ) -> Optional[Negotiator]:
        negotiator = AspirationNegotiator(
            ufun=MappingUtilityFunction(mapping=lambda x: 1.0 - x["i1"] / 10.0)
        )
        return negotiator

    def on_neg_request_rejected(self, req_id: str, by: Optional[List[str]]):
        pass

    def on_neg_request_accepted(self, req_id: str, mechanism: AgentMechanismInterface):
        pass

    def on_negotiation_failure(
        self,
        partners: List[str],
        annotation: Dict[str, Any],
        mechanism: AgentMechanismInterface,
        state: MechanismState,
    ) -> None:
        pass

    def on_negotiation_success(
        self, contract: Contract, mechanism: AgentMechanismInterface
    ) -> None:
        pass

    def on_contract_signed(self, contract: Contract) -> None:
        pass

    def on_contract_cancelled(self, contract: Contract, rejectors: List[str]) -> None:
        pass

    def sign_contract(self, contract: Contract) -> Optional[str]:
        return self.id

    def on_contract_executed(self, contract: Contract) -> None:
        pass

    def on_contract_breached(
        self, contract: Contract, breaches: List[Breach], resolution: Optional[Contract]
    ) -> None:
        pass

    def set_renegotiation_agenda(
        self, contract: Contract, breaches: List[Breach]
    ) -> Optional[RenegotiationRequest]:
        return None

    def respond_to_renegotiation_request(
        self, contract: Contract, breaches: List[Breach], agenda: RenegotiationRequest
    ) -> Optional[Negotiator]:
        return None

    def __init__(self, name=None):
        super().__init__(name=name)
        self.id = name
        self.current_step = 0

    def step(self):
        global results
        self.current_step = self.awi.current_step
        if (self.current_step == 2 and self.name.endswith("1")) or (
            self.current_step == 4 and self.name.endswith("2")
        ):
            issues = [Issue(10, name="i1")]
            partners = self.awi.state["partners"]
            self._request_negotiation(
                partners=[_.name for _ in partners] + [self.name], issues=issues
            )
            results.append(f"{self.name} started negotiation with {partners[0].name}")
        results.append(f"{self.name}: step {self.current_step}")


def test_world_runs_with_some_negs(capsys):
    global results
    results = []
    world = DummyWorld(n_steps=10)
    world.join(DummyAgent("A1"))
    world.join(DummyAgent("A2"))
    world.run()
    assert "A1: step 1" in results, "first step logged"
    assert "A2: step 1" in results, "first step logged"
    assert "A1 started negotiation with A2" in results, "negotiation started"
    assert f"A1: step {world.n_steps-1}" in results, "last step logged"
    assert f"A2: step {world.n_steps-1}" in results, "last step logged"
    assert len(world._saved_contracts) == 2
    assert sum(world.stats["n_negotiations"]) == 2


def test_config_reader_with_a_world():

    world = DummyWorld()
    assert world.bulletin_board is not None
    assert world.n_steps == 10000

    world = DummyWorld.from_config(scope=globals(), config={"n_steps": 10})
    assert world.bulletin_board is not None
    assert world.n_steps == 10


def test_config_reader_with_a_world_with_enum():
    from negmas.situated import BulletinBoard, World

    world = DummyWorld()
    assert world.bulletin_board is not None
    assert world.n_steps == 10000

    world = DummyWorld.from_config(
        scope=globals(), config={"n_steps": 10, "negotiation_speed": 2}
    )
    assert world.bulletin_board is not None
    assert world.n_steps == 10
    assert world.negotiation_speed == 2


if __name__ == "__main__":
    pytest.main(args=[__file__])
