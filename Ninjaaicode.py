from collections import defaultdict


def plurality_method(votes):
    """
    The candidate with the most first-place votes wins.
    """
    vote_counts = defaultdict(int)
    for vote in votes:
        vote_counts[vote[0]] += 1
    max_votes = max(vote_counts.values())
    winners = [candidate for candidate, count in vote_counts.items() if count == max_votes]
    return winners


def borda_count_method(votes, num_candidates):
    """
    Points are assigned based on rankings and the candidate with the most points wins.
    """
    point_counts = defaultdict(int)
    for vote in votes:
        for i, candidate in enumerate(vote):
            point_counts[candidate] += num_candidates - i - 1
    max_points = max(point_counts.values())
    winners = [candidate for candidate, count in point_counts.items() if count == max_points]
    return winners


def instant_runoff_voting(votes, num_candidates):
    """
    Candidates are eliminated round by round until one candidate secures a majority.
    """
    vote_counts = defaultdict(int)
    for vote in votes:
        vote_counts[vote[0]] += 1
    while True:
        min_votes = min(vote_counts.values())
        losers = [candidate for candidate, count in vote_counts.items() if count == min_votes]
        if len(losers) == num_candidates:
            return losers
        for loser in losers:
            del vote_counts[loser]
            for vote in votes:
                if vote[0] == loser:
                    vote.pop(0)
                    if vote:
                        vote_counts[vote[0]] += 1
        if max(vote_counts.values()) > len(votes) / 2:
            return [max(vote_counts, key=vote_counts.get)]


def condorcet_method(votes):
    """
    The candidate who wins all head-to-head matchups against others is the winner.
    """
    wins = defaultdict(int)
    for i in range(len(votes[0])):
        for j in range(i + 1, len(votes[0])):
            candidate_i = votes[0][i]
            candidate_j = votes[0][j]
            count_i = sum(1 for vote in votes if vote.index(candidate_i) < vote.index(candidate_j))
            count_j = sum(1 for vote in votes if vote.index(candidate_j) < vote.index(candidate_i))
            if count_i > count_j:
                wins[candidate_i] += 1
            elif count_j > count_i:
                wins[candidate_j] += 1
    for candidate in wins:
        if wins[candidate] == len(votes[0]) - 1:
            return [candidate]
    return []


def main():
    num_candidates = int(input("Enter the number of candidates: "))
    candidates = []
    for i in range(num_candidates):
        candidate = input(f"Enter candidate {i + 1} name: ")
        candidates.append(candidate)

    num_voters = int(input("Enter the number of voters: "))
    votes = []
    for i in range(num_voters):
        print(f"Enter the ranked vote for voter {i + 1} (comma-separated):")
        for j, candidate in enumerate(candidates):
            print(f"{j + 1}. {candidate}")
        vote = input().split(',')
        vote = [candidates[int(rank) - 1] for rank in vote]
        votes.append(vote)

    print("\nPlurality Method:")
    winners = plurality_method(votes)
    print("Winner(s):", winners)

    print("\nBorda Count Method:")
    winners = borda_count_method(votes, num_candidates)
    print("Winner(s):", winners)

    print("\nInstant Runoff Voting (IRV):")
    winners = instant_runoff_voting([vote.copy() for vote in votes], num_candidates)
    print("Winner(s):", winners)

    print("\nCondorcet Method:")
    winners = condorcet_method(votes)
    if winners:
        print("Winner:", winners[0])
    else:
        print("No Condorcet winner exists.")


if __name__ == "__main__":
    main()
