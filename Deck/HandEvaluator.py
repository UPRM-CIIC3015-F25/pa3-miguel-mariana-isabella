from Cards.Card import Card, Rank

# TODO (TASK 3): Implement a function that evaluates a player's poker hand.
#   Loop through all cards in the given 'hand' list and collect their ranks and suits.
#   Use a dictionary to count how many times each rank appears to detect pairs, three of a kind, or four of a kind.
#   Sort these counts from largest to smallest. Use another dictionary to count how many times each suit appears to check
#   for a flush (5 or more cards of the same suit). Remove duplicate ranks and sort them to detect a
#   straight (5 cards in a row). Remember that the Ace (rank 14) can also count as 1 when checking for a straight.
#   If both a straight and a flush occur in the same suit, return "Straight Flush". Otherwise, use the rank counts
#   and flags to determine if the hand is: "Four of a Kind", "Full House", "Flush", "Straight", "Three of a Kind",
#   "Two Pair", "One Pair", or "High Card". Return a string with the correct hand type at the end.
def evaluate_hand(hand: list[Card]):
    # ---------------- Collect ranks and suits ----------------
    rank_counts = {}
    suit_counts = {}

    ranks = []
    suits = []

    for card in hand:
        r = card.rank
        s = card.suit
        ranks.append(r)
        suits.append(s)


        rank_counts[r] = rank_counts.get(r, 0) + 1

        suit_counts[s] = suit_counts.get(s, 0) + 1


    sorted_counts = sorted(rank_counts.values(), reverse=True)


    is_flush = any(count >= 5 for count in suit_counts.values())


    unique_ranks = sorted(set(ranks))


    if 14 in unique_ranks:
        unique_ranks.append(1)
        unique_ranks = sorted(set(unique_ranks))

    is_straight = False
    for i in range(len(unique_ranks) - 4):
        window = unique_ranks[i:i+5]
        if window == list(range(window[0], window[0] + 5)):
            is_straight = True
            break


    if is_straight and is_flush:
        return "Straight Flush"


    if sorted_counts[0] == 4:
        return "Four of a Kind"

    if sorted_counts[0] == 3 and sorted_counts[1] >= 2:
        return "Full House"

    if is_flush:
        return "Flush"

    if is_straight:
        return "Straight"

    if sorted_counts[0] == 3:
        return "Three of a Kind"

    if sorted_counts[0] == 2 and sorted_counts[1] == 2:
        return "Two Pair"

    if sorted_counts[0] == 2:
        return "One Pair"

    return "High Card"










