import collections

def plurality_vote(votes):
    """Calculates the winner using the Plurality Method."""
    vote_counts = collections.Counter(vote[0] for vote in votes)
    return vote_counts.most_common(1)[0][0]

def borda_count(votes, num_candidates):
    """Calculates the winner using the Borda Count Method."""
    points = {candidate: 0 for candidate in range(num_candidates)}
    for vote in votes:
        for i, candidate in enumerate(vote):
            points[candidate] += num_candidates - i - 1
    return max(points, key=points.get)

def instant_runoff_voting(votes, num_candidates):
    """Calculates the winner using Instant Runoff Voting (IRV)."""
    while True:
        vote_counts = collections.Counter(vote[0] for vote in votes)
        least_votes = min(vote_counts.values())
        eliminated_candidates = [candidate for candidate, count in vote_counts.items() if count == least_votes]
        if len(eliminated_candidates) == 1:
            eliminated_candidate = eliminated_candidates[0]
            votes = [vote for vote in votes if vote[0] != eliminated_candidate]
        else:
            return None  # No clear winner, potential tie
        if len(vote_counts) == 1:
            return list(vote_counts.keys())[0]

def condorcet_method(votes, num_candidates):
    """Calculates the winner using the Condorcet Method."""
    head_to_head_wins = {candidate: 0 for candidate in range(num_candidates)}
    for i in range(num_candidates):
        for j in range(i + 1, num_candidates):
            wins_i = 0
            wins_j = 0
            for vote in votes:
                if vote.index(i) < vote.index(j):
                    wins_i += 1
                else:
                    wins_j += 1
            if wins_i > wins_j:
                head_to_head_wins[i] += 1
            elif wins_j > wins_i:
                head_to_head_wins[j] += 1
    max_wins = max(head_to_head_wins.values())
    condorcet_winner = [candidate for candidate, wins in head_to_head_wins.items() if wins == max_wins]
    if len(condorcet_winner) == 1:
        return condorcet_winner[0]
    else:
        return None  # No clear Condorcet winner, potential tie

def main():
    num_candidates = int(input("Enter the number of candidates: "))
    num_voters = int(input("Enter the number of voters: "))

    candidates = list(range(num_candidates))
    votes = []
    for _ in range(num_voters):
        vote = list(map(int, input("Enter a ranked vote (e.g., 0 1 2 for 3 candidates): ").split()))
        votes.append(vote)

    plurality_winner = plurality_vote(votes)
    borda_winner = borda_count(votes, num_candidates)
    irv_winner = instant_runoff_voting(votes, num_candidates)
    condorcet_winner = condorcet_method(votes, num_candidates)

    print("Plurality winner:", plurality_winner)
    print("Borda Count winner:", borda_winner)
    print("Instant Runoff Voting winner:", irv_winner)
    print("Condorcet winner:", condorcet_winner)

if __name__ == "__main__":
    main()