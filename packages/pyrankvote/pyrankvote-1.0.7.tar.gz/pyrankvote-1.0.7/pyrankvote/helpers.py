"""
Helper classes used by multiple_seat_ranking_methods.py

"""
from pyrankvote.models import Candidate, Ballot

import random
import functools
from typing import List, NamedTuple
from tabulate import tabulate


def almost_equal(value1, value2):
    CONSIDERED_EQUAL_MARGIN = 0.001
    return abs(value1 - value2) < CONSIDERED_EQUAL_MARGIN


class CandidateStatus:
    Elected = "Elected"
    Hopeful = "Hopeful"
    Rejected = "Rejected"


class CandidateResult(NamedTuple):
    candidate: Candidate
    number_of_votes: float
    status: CandidateStatus


class CandidateVoteCount:
    def __init__(self, candidate: Candidate):
        self.candidate = candidate
        self.status = CandidateStatus.Hopeful

        self.number_of_votes = 0.0
        self.votes: List[Ballot] = []

    @property
    def is_in_race(self):
        return self.status == CandidateStatus.Hopeful

    def as_candidate_result(self) -> CandidateResult:
        return CandidateResult(self.candidate, self.number_of_votes, self.status)


class CompareMethodIfEqual:
    Random = "Random"
    MostSecondChoiceVotes = "MostSecondChoiceVotes"


class NoCandidatesLeftInRaceError(RuntimeError): pass


class ElectionManager:
    def __init__(self,
                 candidates: List[Candidate],
                 ballots: List[Ballot],
                 seats=1,
                 number_of_votes_pr_voter=1,
                 compare_method_if_equal=CompareMethodIfEqual.MostSecondChoiceVotes):

        self._ballots = ballots
        self._candidate_vote_counts: dict[Candidate: CandidateVoteCount] = {
            candidate: CandidateVoteCount(candidate) for candidate in candidates
        }

        self._candidates_in_race: List[CandidateVoteCount] = self._candidate_vote_counts.values()
        self._elected_candidates: List[CandidateVoteCount] = []  # Sorted asc by election round
        self._rejected_candidates: List[CandidateVoteCount] = []  # Sorted desc by election round

        self._number_of_candidates = len(candidates)
        self._number_of_votes_pr_voter = number_of_votes_pr_voter
        self._compare_method_if_equal = compare_method_if_equal

        # Distribute votes to the most preferred candidates (before any candidates are elected or rejected)
        for ballot in ballots:
            # If one vote per voter -> Voters vote goes to the first candidate on the ranked list
            # If more than one vote per voter -> Voters votes goes to the x first candidates on the ranked list
            candidates_that_should_be_voted_on = ballot.ranked_candidates[0:number_of_votes_pr_voter]

            for candidate in candidates_that_should_be_voted_on:
                candidate_vc = self._candidate_vote_counts[candidate]
                candidate_vc.number_of_votes += 1
                candidate_vc.votes.append(ballot)

        # After votes are distributed -> sort candidates
        # This is also done each time transfer_votes(...) is called
        self._sort_candidates_in_race()

    # METHODS WITH SIDE-EFFECTS

    def elect_candidate(self, candidate: Candidate):
        if candidate not in self._candidate_vote_counts:
            raise RuntimeError("Candidate not found in electionManager")

        candidate_cv = self._candidate_vote_counts[candidate]

        candidate_cv.status = CandidateStatus.Elected
        self._elected_candidates.append(candidate_cv)
        self._candidates_in_race.remove(candidate_cv)

    def reject_candidate(self, candidate: Candidate):
        if candidate not in self._candidate_vote_counts:
            raise RuntimeError("Candidate not found in electionManager")

        candidate_cv = self._candidate_vote_counts[candidate]

        candidate_cv.status = CandidateStatus.Rejected
        self._rejected_candidates.append(candidate_cv)
        self._candidates_in_race.remove(candidate_cv)

    def transfer_votes(self, candidate: Candidate, number_of_trans_votes: float):
        if candidate not in self._candidate_vote_counts:
            raise RuntimeError("Candidate not found in electionManager")
        if round(number_of_trans_votes, 4) == 0.000:
            # Do nothing
            return

        candidate_cv = self._candidate_vote_counts[candidate]
        if candidate_cv.status == CandidateStatus.Hopeful:
            raise RuntimeError("ElectionManager can not transfer votes from a candidate "
                               "that is still in the race (candidateStatus == Hopeful)")

        voters = len(candidate_cv.votes)  # Voters/ballots, not votes!
        votes_pr_voter = number_of_trans_votes/float(voters)  # This is a fractional number between 0 and 1

        for ballot in candidate_cv.votes:
            new_candidate_choice = self._get_ballot_candidate_nr_x_in_race_or_none(ballot, self._number_of_votes_pr_voter - 1)

            if new_candidate_choice is None:
                # Chose a candidate at random
                candidates_in_race = self.get_candidates_in_race()
                if len(candidates_in_race) == 0:
                    # If no candidates left in race, do nothing
                    return
                else:
                    new_candidate_choice = random.choice(candidates_in_race)

            new_candidate_cv = self._candidate_vote_counts[new_candidate_choice]
            new_candidate_cv.number_of_votes += votes_pr_voter
            new_candidate_cv.votes.append(ballot)

        candidate_cv.number_of_votes -= number_of_trans_votes
        candidate_cv.votes = []

        self._sort_candidates_in_race()

    # METHODS WITHOUT SIDE-EFFECTS

    def get_number_of_candidates_in_race(self) -> int:
        return len(self._candidates_in_race)

    def get_number_of_elected_candidates(self) -> int:
        number_of_elected_candidates = len(self._elected_candidates)
        return number_of_elected_candidates

    def get_number_of_votes(self, candidate: Candidate) -> float:
        if candidate not in self._candidate_vote_counts:
            raise RuntimeError("Candidate not found in electionManager")

        return self._candidate_vote_counts[candidate].number_of_votes

    def get_candidates_in_race(self) -> List[Candidate]:
        candidates = [
            candidate_vc.candidate
            for candidate_vc in self._candidates_in_race
            if candidate_vc.is_in_race
        ]
        return candidates

    def get_candidate_with_least_votes_in_race(self) -> Candidate:
        if len(self._candidates_in_race) == 0:
            raise NoCandidatesLeftInRaceError("No candidates left in race")

        candidate_with_least_votes = self._candidates_in_race[-1].candidate
        return candidate_with_least_votes

    def get_candidates_with_more_than_x_votes(self, x: int) -> List[Candidate]:
        candidates = [
            candidate_vc.candidate
            for candidate_vc in self._candidates_in_race
            if round(candidate_vc.number_of_votes, 4) > round(x, 4)
        ]
        return candidates

    def get_results(self) -> List[CandidateStatus]:
        candidates_vc: List[CandidateVoteCount] = []
        candidates_vc.extend(self._elected_candidates)
        candidates_vc.extend(self._candidates_in_race)
        candidates_vc.extend(self._rejected_candidates[::-1])

        candidate_results = [candidate_vc.as_candidate_result() for candidate_vc in candidates_vc]
        return candidate_results

    # INTERNAL METHODS
    def _get_ballot_candidate_nr_x_in_race_or_none(self, ballot, x) -> Candidate:
        ranked_candidates_in_race = [
            candidate
            for candidate in ballot.ranked_candidates
            if self._candidate_vote_counts[candidate].is_in_race
        ]

        if len(ranked_candidates_in_race) > x:
            candidate = ranked_candidates_in_race[x]
            return candidate
        else:
            return None

    def _sort_candidates_in_race(self):
        sorted_candidates_in_race = sorted(self._candidates_in_race,
                                           key=functools.cmp_to_key(self._cmp_candidate_vote_counts))
        self._candidates_in_race = sorted_candidates_in_race

    def _cmp_candidate_vote_counts(self, candidate1_vc: CandidateVoteCount, candidate2_vc: CandidateVoteCount) -> int:
        c1_votes: float = candidate1_vc.number_of_votes
        c2_votes: float = candidate2_vc.number_of_votes

        if not almost_equal(c1_votes, c2_votes):
            if c1_votes > c2_votes:
                return -1
            else:
                return 1

        # If equal number of votes
        else:
            if self._compare_method_if_equal == CompareMethodIfEqual.MostSecondChoiceVotes:
                # Choose candidate with most second choices (or third, forth and so on) (default)
                if self._candidate1_has_most_second_choices(candidate1_vc, candidate2_vc, x=1):
                    return -1
                else:
                    return 1

            if self._compare_method_if_equal == CompareMethodIfEqual.Random:
                # Choose randomly
                return random.choice([1, -1])

            else:
                raise SystemError("Compare method unknown/not implemented.")

    def _candidate1_has_most_second_choices(self, candidate1_vc: CandidateVoteCount, candidate2_vc: CandidateVoteCount, x) -> bool:
        if x >= self._number_of_candidates:
            return random.choice([True, False])

        votes_candidate1: int = 0
        votes_candidate2: int = 0

        for ballot in self._ballots:
            candidate = self._get_ballot_candidate_nr_x_in_race_or_none(ballot, x)

            if candidate == candidate1_vc.candidate:
                votes_candidate1 += 1
            if candidate == candidate2_vc.candidate:
                votes_candidate2 += 1
            if candidate is None:
                pass  # Zero votes

        if votes_candidate1 == votes_candidate2:
            return self._candidate1_has_most_second_choices(candidate1_vc, candidate2_vc, x + 1)
        else:
            return votes_candidate1 > votes_candidate2


class ElectionResults:
    def __init__(self):
        self.rounds: List[List[CandidateResult]] = []

    def register_round_results(self, round: List[CandidateResult]):
        self.rounds.append(round)

    def get_winners(self) -> List[Candidate]:
        last_round = self.rounds[-1]
        winner_candidates = [
            candidate_result.candidate
            for candidate_result in last_round
            if candidate_result.status == CandidateStatus.Elected
        ]
        return winner_candidates

    def __repr__(self):
        return "ElectionResults(%i rounds)" % len(self.rounds)

    def __str__(self):
        lines = []
        for i, round_ in enumerate(self.rounds):

            # Print round nr header
            if i == len(self.rounds)-1:
                lines.append("FINAL RESULT")
            else:
                round_nr = i + 1
                lines.append("ROUND %i" % round_nr)

            # Print table
            lines.append(tabulate(round_, headers=['Candidate', 'Votes', 'Status']))

            # Print an extra blank line
            lines.append("")

        string = "\n".join(lines)
        return string
