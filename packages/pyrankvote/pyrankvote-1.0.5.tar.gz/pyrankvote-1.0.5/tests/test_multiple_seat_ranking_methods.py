import unittest
import pyrankvote
from pyrankvote.models import Candidate, Ballot


class TestPreferentialBlockVoting(unittest.TestCase):
    def test_simple_irv(self):

        
        stay = Candidate("Stay")
        soft = Candidate("Soft Brexit")
        hard = Candidate("Hard Brexit")

        candidates = [stay, soft, hard]

        ballots = [
            Ballot(ranked_candidates=[soft, stay]),
            Ballot(ranked_candidates=[stay, soft]),
            Ballot(ranked_candidates=[stay, soft]),
            Ballot(ranked_candidates=[hard, soft]),
            Ballot(ranked_candidates=[hard, stay, soft]),
        ]

        election_result = pyrankvote.multiple_seat_ranking_methods.preferential_block_voting(
            candidates, ballots, number_of_seats=1
        )
        winners = election_result.get_winners()

        self.assertEqual(1, len(winners), "Function should return a list with one item")

        winner = winners[0]
        self.assertEqual(stay, winner, "Winner should be Soft")

    def test_simple_irv2(self):

        per = Candidate("Per")
        paal = Candidate("Pål")
        askeladden = Candidate("Askeladden")

        candidates = [per, paal, askeladden]

        ballots = [
            Ballot(ranked_candidates=[askeladden, per]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[paal, per]),
            Ballot(ranked_candidates=[paal, per, askeladden]),
        ]

        election_result = pyrankvote.multiple_seat_ranking_methods.preferential_block_voting(
            candidates, ballots, number_of_seats=1
        )
        winners = election_result.get_winners()

        self.assertEqual(1, len(winners), "Function should return a list with one item")
        self.assertListEqual([per], winners, "Winners should be Per")

    def test_simple_pbv(self):

        per = Candidate("Per")
        paal = Candidate("Pål")
        askeladden = Candidate("Askeladden")

        candidates = [per, paal, askeladden]

        ballots = [
            Ballot(ranked_candidates=[askeladden, per]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[paal, per]),
            Ballot(ranked_candidates=[paal, per, askeladden]),
        ]

        election_result = pyrankvote.multiple_seat_ranking_methods.preferential_block_voting(
            candidates, ballots, number_of_seats=2
        )
        winners = election_result.get_winners()

        self.assertEqual(2, len(winners), "Function should return a list with two items")
        self.assertListEqual([per, paal], winners, "Winners should be Per and Pål")

    def test_irv_with_second_selection_if_equal(self):

        stay = Candidate("Stay")
        soft = Candidate("Soft Brexit")
        hard = Candidate("Hard Brexit")

        candidates = [stay, soft, hard]

        ballots = [
            Ballot(ranked_candidates=[stay, soft, hard]),
            Ballot(ranked_candidates=[hard, soft, stay]),
            Ballot(ranked_candidates=[soft, stay, hard]),
        ]

        election_result = pyrankvote.multiple_seat_ranking_methods.preferential_block_voting(
            candidates, ballots, number_of_seats=1
        )

        winners = election_result.get_winners()
        self.assertEqual(1, len(winners), "Function should return a list with one item")

        winner = winners[0]
        self.assertEqual(soft, winner, "Winner should be soft")

    def test_simple_pbv_with_second_selection_if_equal(self):

        stay = Candidate("Stay")
        soft = Candidate("Soft Brexit")
        hard = Candidate("Hard Brexit")

        candidates = [stay, soft, hard]

        ballots = [
            Ballot(ranked_candidates=[stay, soft, hard]),
            Ballot(ranked_candidates=[hard, soft, stay]),
            Ballot(ranked_candidates=[soft, stay, hard]),
        ]

        election_result = pyrankvote.multiple_seat_ranking_methods.preferential_block_voting(
            candidates, ballots, number_of_seats=2
        )
        winners = election_result.get_winners()

        self.assertEqual(2, len(winners), "Function should return a list with two items")
        self.assertListEqual([soft, stay], winners, "Winners should be Soft and Stay")


class TestSingleTransferableVote(unittest.TestCase):
    def test_simple_irv(self):

        stay = Candidate("Stay")
        soft = Candidate("Soft Brexit")
        hard = Candidate("Hard Brexit")

        candidates = [stay, soft, hard]

        ballots = [
            Ballot(ranked_candidates=[soft, stay]),
            Ballot(ranked_candidates=[stay, soft]),
            Ballot(ranked_candidates=[stay, soft]),
            Ballot(ranked_candidates=[hard, soft]),
            Ballot(ranked_candidates=[hard, stay, soft]),
        ]

        election_result = pyrankvote.multiple_seat_ranking_methods.single_transferable_vote(
            candidates, ballots, number_of_seats=1
        )
        winners = election_result.get_winners()

        self.assertEqual(1, len(winners), "Function should return a list with one item")

        winner = winners[0]
        self.assertEqual(stay, winner, "Winner should be Soft")

    def test_simple_irv2(self):

        per = Candidate("Per")
        paal = Candidate("Pål")
        askeladden = Candidate("Askeladden")

        candidates = [per, paal, askeladden]

        ballots = [
            Ballot(ranked_candidates=[askeladden, per]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[paal, per]),
            Ballot(ranked_candidates=[paal, per, askeladden]),
        ]

        election_result = pyrankvote.multiple_seat_ranking_methods.single_transferable_vote(
            candidates, ballots, number_of_seats=1
        )
        winners = election_result.get_winners()

        self.assertEqual(1, len(winners), "Function should return a list with one item")
        self.assertListEqual([per], winners, "Winners should be Per")

    def test_case1_simple(self):

        per = Candidate("Per")
        paal = Candidate("Pål")
        askeladden = Candidate("Askeladden")

        candidates = [per, paal, askeladden]

        ballots = [
            Ballot(ranked_candidates=[askeladden, per]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[paal, per]),
            Ballot(ranked_candidates=[paal, per, askeladden]),
        ]

        election_result = pyrankvote.multiple_seat_ranking_methods.single_transferable_vote(
            candidates, ballots, number_of_seats=2
        )
        winners = election_result.get_winners()

        self.assertEqual(2, len(winners), "Function should return a list with two items")
        self.assertListEqual([per, paal], winners, "Winners should be Per and Pål")

    def test_case2(self):

        per = Candidate("Per")
        paal = Candidate("Pål")
        maria = Candidate("Maria")
        ingrid = Candidate("Ingrid")

        candidates = [per, paal, maria, ingrid]


        # Quote = 4.33 with 10 votes and 2 seat
        ballots = [
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[maria, ingrid]),
            Ballot(ranked_candidates=[ingrid, maria]),
            Ballot(ranked_candidates=[ingrid, maria]),
        ]

        # 1. round: Per: 7, Ingrid: 2, Maria: 1, Pål: 0
        #       --> Per is elected and 2.67 votes are transfered to Pål
        # 2. round: Pål: 2.67, Ingrid: 2, Maria: 1
        #       --> Maria is excluded and her one vote is transfered to Ingrid
        # 3. round: Ingrid: 3, Pål: 2.67
        #       --> Ingrid is elected

        election_result = pyrankvote.multiple_seat_ranking_methods.single_transferable_vote(
            candidates, ballots, number_of_seats=2
        )
        winners = election_result.get_winners()

        self.assertEqual(2, len(winners), "Function should return a list with two items")
        self.assertListEqual([per, ingrid], winners, "Winners should be Per and Ingrid")

    def test_case3(self):

        per = Candidate("Per")
        paal = Candidate("Pål")
        maria = Candidate("Maria")
        ingrid = Candidate("Ingrid")

        candidates = [per, paal, maria, ingrid]

        # Quote = 4.67 with 11 votes and 2 seat
        ballots = [
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[per, paal]),
            Ballot(ranked_candidates=[maria, ingrid]),
            Ballot(ranked_candidates=[ingrid, maria]),
            Ballot(ranked_candidates=[ingrid, maria]),
        ]

        # 1. round: Per: 7, Ingrid: 2, Maria: 1, Pål: 0
        #       --> Per is elected and 3.33 votes are transfered to Pål
        # 2. round: Pål: 3.33, Ingrid: 2, Maria: 1
        #       --> Maria is excluded and her one vote is transfered to Ingrid
        # 3. round: Pål: 3.33, Ingrid: 3
        #       --> Pål is elected

        election_result = pyrankvote.multiple_seat_ranking_methods.single_transferable_vote(
            candidates, ballots, number_of_seats=2
        )
        winners = election_result.get_winners()

        self.assertEqual(2, len(winners), "Function should return a list with two items")
        self.assertListEqual([per, paal], winners, "Winners should be Per and Pål")
        