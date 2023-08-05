from threading import RLock
from typing import List

from bobocep.decider.buffers.shared_versioned_match_buffer import \
    SharedVersionedMatchBuffer
from bobocep.decider.handlers.abstract_handler import AbstractHandler
from bobocep.decider.handlers.nfa_handler_subscriber import \
    INFAHandlerSubscriber
from bobocep.decider.runs.bobo_run import BoboRun
from bobocep.decider.runs.run_subscriber import IRunSubscriber
from bobocep.receiver.clocks.epoch_ns_clock import EpochNSClock
from bobocep.rules.events.bobo_event import BoboEvent
from bobocep.rules.events.composite_event import CompositeEvent
from bobocep.rules.events.histories.bobo_history import BoboHistory
from bobocep.rules.nfas.bobo_nfa import BoboNFA


class BoboNFAHandler(AbstractHandler, IRunSubscriber):
    """A :code:`bobocep` automaton handler.

    :param nfa: The automaton with which the handler is associated.
    :type nfa: BoboNFA

    :param buffer: The buffer in which the handler will store event data.
    :type buffer: SharedVersionedMatchBuffer

    :param max_recent: The maximum number of recent CompositeEvent instances
                        generated by this handler to pass to runs.
                        Minimum of 1, defaults to 1.
    :type max_recent: int, optional
    """

    NFA_NAME = "nfa_name"
    BUFFER = "buffer"
    RUNS = "runs"

    def __init__(self,
                 nfa: BoboNFA,
                 buffer: SharedVersionedMatchBuffer,
                 max_recent: int = 1) -> None:
        super().__init__()

        self.nfa = nfa
        self.buffer = buffer

        self._runs = {}
        self._recent = []
        self._max_recent = max(1, max_recent)
        self._subs = []
        self._lock = RLock()

    def process(self, event: BoboEvent) -> None:
        with self._lock:
            recent = self._recent[:]
            self._check_event_against_runs(event, recent)

            if self.nfa.start_state.process(event, {}, recent):
                # only notify if start state isn't also final state
                self.on_run_clone(
                    state_name=self.nfa.start_state.name,
                    event=event,
                    parent_run_id=None,
                    force_parent=False,
                    notify=True)

    def _check_event_against_runs(self,
                                  event: BoboEvent,
                                  recent: List[CompositeEvent]) -> None:
        for run in tuple(self._runs.values()):
            run.process(event, recent)

    def add_run(self, run: BoboRun) -> None:
        """
        Adds a run to the handler.

        :param run: The run.
        :type run: BoboRun
        """

        with self._lock:
            if run.id in self._runs:
                raise RuntimeError(
                    "Run ID {} already exists in handler for NFA {}.".format(
                        run.id, self.nfa.name))

            self._runs[run.id] = run
            run.subscribe(self)

    def remove_run(self,
                   run_id: str,
                   halt: bool = False,
                   notify: bool = False) -> None:
        """
        Removes a run from the handler.

        :param run_id: The ID of the run to remove.
        :type run_id: str

        :param halt: Halts the run first, defaults to False.
        :type halt: bool, optional

        :param notify: Notifies subscribers that the run has halted
                       *only if* halt is True. Defaults to False.
        :type notify: bool, optional
        """

        with self._lock:
            run = self._runs.get(run_id)

            if run is not None:
                if halt:
                    run.set_halt(notify=notify)

                # remove current run version from the pointers of all
                # match events in buffer
                self.buffer.remove_version(
                    nfa_name=self.nfa.name,
                    version=run.version.get_version_as_str())

                # remove run from handler
                self._runs.pop(run.id, None)

    def clear_runs(self,
                   halt: bool = True,
                   notify: bool = True) -> None:
        """
        Removes all runs from the handler.

        :param halt: Halts all runs first, defaults to False.
        :type halt: bool, optional

        :param notify: Notifies subscribers that runs have halted
                       *only if* halt is True. Defaults to False.
        :type notify: bool, optional
        """

        with self._lock:
            for run in tuple(self._runs.values()):
                self.remove_run(run_id=run.id,
                                halt=halt,
                                notify=notify)

    def on_run_transition(self,
                          run_id: str,
                          state_name_from: str,
                          state_name_to: str,
                          event: BoboEvent,
                          notify: bool = True) -> None:
        with self._lock:
            if notify:
                self._notify_transition(
                    run_id=run_id,
                    state_name_from=state_name_from,
                    state_name_to=state_name_to,
                    event=event)

    def on_run_clone(self,
                     state_name: str,
                     event: BoboEvent,
                     parent_run_id: str = None,
                     force_parent: bool = False,
                     notify: bool = True) -> None:
        """
        :raises RuntimeError: No parent run found when either one is specified
                              or force_parent is True.
        :raises RuntimeError: State name not found in automaton.
        """

        with self._lock:
            if parent_run_id is None:
                parent_run = None
            else:
                parent_run = self._runs.get(parent_run_id)

            if parent_run is None and \
                    (parent_run_id is not None or force_parent):
                raise RuntimeError(
                    "Failed to clone run. No parent run found.")

            next_state = self.nfa.states.get(state_name)

            if next_state is None:
                raise RuntimeError(
                    "Failed to clone run. "
                    "State {} not found in NFA {}.".format(
                        state_name, self.nfa.name))

            clone_run = BoboRun(
                buffer=self.buffer,
                nfa=self.nfa,
                event=event,
                start_state=next_state,
                parent_run=parent_run)

            self.add_run(clone_run)

            if clone_run.is_final():
                self.on_run_final(
                    run_id=clone_run.id,
                    history=BoboHistory({
                        clone_run.current_state.label: [clone_run.event]
                    }),
                    halt=True,
                    notify=notify
                )

            elif notify:
                self._notify_clone(
                    run_id=clone_run.id,
                    state_name=clone_run.current_state.name,
                    event=clone_run.event)

    def on_run_final(self,
                     run_id: str,
                     history: BoboHistory,
                     halt: bool = False,
                     notify: bool = True) -> None:
        """
        :raises RuntimeError: Run ID not found.
        """

        with self._lock:
            run = self._runs.get(run_id)

            if run is None:
                raise RuntimeError(
                    "Run {} not found in handler for NFA {}.".format(
                        run_id, self.nfa.name))

            if halt:
                run.set_halt(notify=False)

            event = CompositeEvent(
                timestamp=EpochNSClock.generate_timestamp(),
                name=self.nfa.name,
                history=history)

            if notify:
                self._notify_final(run_id, event)

            self._add_recent(event)
            self.remove_run(run_id)

    def on_run_halt(self,
                    run_id: str,
                    notify: bool = True) -> None:
        with self._lock:
            if notify:
                self._notify_halt(run_id)
            self.remove_run(run_id)

    def force_run_transition(self,
                             run_id: str,
                             state_name_from: str,
                             state_name_to: str,
                             event: BoboEvent) -> None:
        """
        Forces a state transition on a run without notification.

        :param run_id: The run ID.
        :type run_id: str

        :param state_name_from: The original state before the transition.
        :type state_name_from: str

        :param state_name_to: The new state after the transition.
        :type state_name_to: str

        :param event: The event that caused the state transition.
        :type event: BoboEvent

        :raises RuntimeError: Run ID not found.
        :raises RuntimeError: From state not found.
        :raises RuntimeError: To state not found.
        :raises RuntimeError: To state is not a transition for From state.
        :raises RuntimeError: From state is not the current run state.
        """

        with self._lock:
            run = self._runs.get(run_id)

            if run is None:
                raise RuntimeError(
                    "Run ID {} not found in handler for NFA {}.".format(
                        run_id, self.nfa.name))

            state_from = self.nfa.states.get(state_name_from)

            if state_from is None:
                raise RuntimeError(
                    "State {} not found in NFA {}.".format(
                        state_name_from, self.nfa.name))

            state_to = self.nfa.states.get(state_name_to)

            if state_to is None:
                raise RuntimeError(
                    "State {} not found in NFA {}.".format(
                        state_name_to, self.nfa.name))

            trans_from = self.nfa.transitions[state_name_from]

            if state_name_to not in trans_from.state_names:
                raise RuntimeError(
                    "State {} not a transition for state {}.".format(
                        state_name_to, state_name_from))

            if run.current_state.name != state_name_from:
                raise RuntimeError(
                    "Current state for run {} is {} and not {}.".format(
                        run_id, run.current_state.name, state_name_from))

            run._proceed(event=event,
                         original_state=state_from,
                         trans_state=state_to,
                         increment=state_name_from == state_name_to,
                         notify=False)

    def force_run_clone(self,
                        state_name: str,
                        event: BoboEvent,
                        parent_run_id: str) -> None:
        """
        Forces a run clone without notification.

        :param state_name: The state of the run after cloning.
        :type state_name: str

        :param event: The event that caused the clone.
        :type event: BoboEvent

        :param parent_run_id: The parent run ID.
        :type parent_run_id: str
        """

        with self._lock:
            self.on_run_clone(
                state_name=state_name,
                event=event,
                parent_run_id=parent_run_id,
                force_parent=False,
                notify=False)

            run = self._runs.get(parent_run_id)

            if run is not None:
                run._last_proceed_had_clone = True

    def force_run_halt(self, run_id: str) -> None:
        """
        Forces a halt without notification.

        :param run_id: The run ID.
        :type run_id: str

        :raises RuntimeError: Run ID not found.
        :raises RuntimeError: Run has already halted.
        """

        with self._lock:
            run = self._runs.get(run_id)

            if run is None:
                raise RuntimeError(
                    "Run {} not found in handler for NFA {}.".format(
                        run_id, self.nfa.name))

            if run.is_halted():
                raise RuntimeError(
                    "Run {} has already halted for NFA {}.".format(
                        run_id, self.nfa.name))

            run.set_halt(notify=False)
            self.on_run_halt(run_id, notify=False)

    def force_run_final(self, run_id: str, history: BoboHistory):
        """
        Forces a run to reach its final state without notification.

        :param run_id: The run ID.
        :type run_id: str

        :param history: The history of the accepted run.
        :type history: BoboHistory
        """

        with self._lock:
            self.on_run_final(run_id=run_id,
                              history=history,
                              halt=True,
                              notify=False)

    def subscribe(self, subscriber: INFAHandlerSubscriber) -> None:
        """
        :param subscriber: Subscribes to state transitions within handler.
        :type subscriber: INFAHandlerSubscriber
        """

        with self._lock:
            if subscriber not in self._subs:
                self._subs.append(subscriber)

    def unsubscribe(self, unsubscriber: INFAHandlerSubscriber) -> None:
        """
        :param unsubscriber: Unsubscribes from state transitions within
                             handler.
        :type unsubscriber: INFAHandlerSubscriber
        """

        with self._lock:
            if unsubscriber in self._subs:
                self._subs.remove(unsubscriber)

    def _add_recent(self, event: CompositeEvent) -> None:
        # add new event to the start of the list
        self._recent.insert(0, event)

        # ensure first event has the largest timestamp i.e. is most recent
        self._recent.sort(key=lambda e: e.timestamp, reverse=True)

        # delete oldest event if list length exceeds the maximum
        if len(self._recent) > self._max_recent:
            self._recent.pop()

    def to_dict(self) -> dict:
        """
        :return: A dict representation of the object.
        """

        with self._lock:
            return {
                self.NFA_NAME: self.nfa.name,
                self.BUFFER: self.buffer.to_dict(),
                self.RUNS: [run.to_dict() for run in self._runs.values()
                            if not run.is_halted()]
            }

    def _notify_transition(self,
                           run_id: str,
                           state_name_from: str,
                           state_name_to: str,
                           event: BoboEvent) -> None:
        for subscriber in self._subs:
            subscriber.on_handler_transition(
                nfa_name=self.nfa.name,
                run_id=run_id,
                state_name_from=state_name_from,
                state_name_to=state_name_to,
                event=event)

    def _notify_clone(self,
                      run_id: str,
                      state_name: str,
                      event: BoboEvent) -> None:
        for subscriber in self._subs:
            subscriber.on_handler_clone(
                nfa_name=self.nfa.name,
                run_id=run_id,
                state_name=state_name,
                event=event)

    def _notify_final(self, run_id: str, event: CompositeEvent) -> None:
        for subscriber in self._subs:
            subscriber.on_handler_final(
                nfa_name=self.nfa.name,
                run_id=run_id,
                event=event)

    def _notify_halt(self, run_id: str) -> None:
        for subscriber in self._subs:
            subscriber.on_handler_halt(
                nfa_name=self.nfa.name,
                run_id=run_id)
