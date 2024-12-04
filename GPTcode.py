from collections import Counter


def get_votes(candidates, num_voters):
    """Get the ranked votes from voters."""
    votes = []
    print(f"\nPlease provide ranked votes from {num_voters} voters (1 is the highest rank):")
    for i in range(num_voters):
        vote = []
        print(f"Voter {i + 1}:")
        for idx, candidate in enumerate(candidates):
            rank = int(input(f"Rank for {candidate}: "))
            vote.append((candidate, rank))
        votes.append(sorted(vote, key=lambda x: x[1]))
    return votes


def plurality_method(votes, candidates):
    """Plurality method: winner is the candidate with most first-place votes."""
    first_place_votes = Counter(vote[0][0] for vote in votes)
    winner = max(first_place_votes, key=first_place_votes.get)
    return winner


def borda_count_method(votes, candidates):
    """Borda Count method: points assigned based on ranking."""
    points = {candidate: 0 for candidate in candidates}
    num_candidates = len(candidates)
    for vote in votes:
        for i, (candidate, rank) in enumerate(vote):
            points[candidate] += (num_candidates - rank)
    winner = max(points, key=points.get)
    return winner


def instant_runoff_voting(votes, candidates):
    """Instant Runoff Voting (IRV): eliminate candidates round by round."""

    def count_first_place_votes(votes):
        """Count the first-place votes for each candidate."""
        first_place = Counter(vote[0][0] for vote in votes)
        return first_place

    remaining_candidates = candidates[:]
    while len(remaining_candidates) > 1:
        first_place_votes = count_first_place_votes(votes)
        least_votes = min(first_place_votes.values())
        eliminated_candidates = [candidate for candidate, votes in first_place_votes.items() if votes == least_votes]

        if len(remaining_candidates) == 2:
            break

        remaining_candidates = [candidate for candidate in remaining_candidates if
                                candidate not in eliminated_candidates]

        # Reallocate votes
        new_votes = []
        for vote in votes:
            new_vote = [candidate for candidate, _ in vote if candidate in remaining_candidates]
            new_votes.append(new_vote)

        votes = [[(candidate, 1) for candidate in new_vote] for new_vote in new_votes]

    return remaining_candidates[0]


def condorcet_method(votes, candidates):
    """Condorcet Method: the candidate who wins all head-to-head matchups."""

    def pairwise_comparison(votes, candidates):
        """Perform pairwise comparisons between candidates."""
        results = {candidate: {other: 0 for other in candidates} for candidate in candidates}
        for vote in votes:
            for i, (candidate1, _) in enumerate(vote):
                for j, (candidate2, _) in enumerate(vote):
                    if i < j:
                        results[candidate1][candidate2] += 1
                    elif i > j:
                        results[candidate2][candidate1] += 1
        return results

    results = pairwise_comparison(votes, candidates)
    condorcet_winner = None
    for candidate in candidates:
        if all(results[candidate][other] > len(votes) // 2 for other in candidates if other != candidate):
            condorcet_winner = candidate
            break

    return condorcet_winner


def main():
    print("Welcome to the Voting Simulation!")

    # Step 1: Get candidates and number of voters
    candidates = input("Enter the list of candidates (comma separated): ").split(",")
    candidates = [candidate.strip() for candidate in candidates]
    num_voters = int(input("Enter the number of voters: "))

    # Step 2: Gather votes
    votes = get_votes(candidates, num_voters)

    # Step 3: Calculate and print winners for each method

    # Plurality Method
    winner_plurality = plurality_method(votes, candidates)
    print(f"Plurality Method winner: {winner_plurality}")

    # Borda Count Method
    winner_borda = borda_count_method(votes, candidates)
    print(f"Borda Count Method winner: {winner_borda}")

    # Instant Runoff Voting (IRV)
    winner_irv = instant_runoff_voting(votes, candidates)
    print(f"Instant Runoff Voting (IRV) winner: {winner_irv}")

    # Condorcet Method
    winner_condorcet = condorcet_method(votes, candidates)
    if winner_condorcet:
        print(f"Condorcet Method winner: {winner_condorcet}")
    else:
        print("Condorcet Method: No clear winner")


if __name__ == "__main__":
    main()
