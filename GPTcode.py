def get_candidates():
    candidates = input("Enter the candidates' names, separated by commas: ").split(",")
    return [candidate.strip() for candidate in candidates]


def get_votes(candidates, num_voters):
    votes = []
    for i in range(num_voters):
        while True:
            vote = input(f"Rank the candidates for voter {i + 1} (comma-separated): ").split(",")
            vote = [v.strip() for v in vote]
            if sorted(vote) == sorted(candidates):
                votes.append(vote)
                break
            else:
                print("Invalid vote. Ensure all candidates are ranked exactly once.")
    return votes


def plurality_method(votes):
    tally = {}
    for vote in votes:
        first_choice = vote[0]
        tally[first_choice] = tally.get(first_choice, 0) + 1
    winner = max(tally, key=tally.get)
    print(f"Plurality Winner: {winner}")


def borda_count_method(votes, candidates):
    scores = {candidate: 0 for candidate in candidates}
    num_candidates = len(candidates)

    for vote in votes:
        for rank, candidate in enumerate(vote):
            scores[candidate] += num_candidates - rank - 1

    winner = max(scores, key=scores.get)
    print(f"Borda Count Winner: {winner}")


def instant_runoff_voting(votes, candidates):
    while True:
        tally = {candidate: 0 for candidate in candidates}
        for vote in votes:
            tally[vote[0]] += 1

        max_votes = max(tally.values())
        total_votes = sum(tally.values())
        if max_votes > total_votes / 2:
            winner = max(tally, key=tally.get)
            print(f"IRV Winner: {winner}")
            return

        min_votes = min(tally.values())
        to_eliminate = [candidate for candidate, votes in tally.items() if votes == min_votes]
        candidates = [c for c in candidates if c not in to_eliminate]

        for vote in votes:
            votes[:] = [candidate for candidate in vote if candidate in candidates]


def condorcet_method(votes, candidates):
    def wins_against(a, b):
        return sum(
            (a in vote and b in vote and vote.index(a) < vote.index(b))
            for vote in votes
        )

    pairwise_wins = {candidate: 0 for candidate in candidates}

    for i, a in enumerate(candidates):
        for b in candidates[i + 1:]:
            if wins_against(a, b) > len(votes) / 2:
                pairwise_wins[a] += 1
            elif wins_against(b, a) > len(votes) / 2:
                pairwise_wins[b] += 1

    winner = next(
        (candidate for candidate, wins in pairwise_wins.items() if wins == len(candidates) - 1),
        None
    )

    if winner:
        print(f"Condorcet Winner: {winner}")
    else:
        print("Condorcet Winner: None (No Condorcet winner exists)")


def main():
    candidates = get_candidates()
    num_voters = int(input("Enter the number of voters: "))
    votes = get_votes(candidates, num_voters)

    print("\nResults:")
    plurality_method(votes)
    borda_count_method(votes, candidates)
    instant_runoff_voting(votes, candidates)
    condorcet_method(votes, candidates)


if __name__ == "__main__":
    main()
