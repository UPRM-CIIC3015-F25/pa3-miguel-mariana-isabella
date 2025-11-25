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
    rank_counts = {}
    suit_counts = {}

    for card in hand:
        rank = card.rank.value if isinstance(card.rank, Rank) else card.rank
        suit = card.suit

        rank_counts[rank] = rank_counts.get(rank,0) + 1
        suit_counts[suit] = suit_counts.get(suit,0) + 1

        count_values = sorted(rank_counts.values(), reverse=True)

        flush_suit = None
        for s, count in suit_counts.items():
            if count > 5:
                flush_suit = s
                break
        is_flush = flush_suit is not None


        if 14 in unique_ranks:
            unique_ranks.append(1)


        def has_straight(ranks):
            if len(ranks) < 5:
                return False
        consecutive = 1
        for i in range(1,len(ranks)):
            if ranks[i] == ranks[i-1] + 1:
                consecutive += 1
                if consecutive >= 5:
                    return True
            else:
                consecutive = 1
        return False

    is_straight = has_straight(unique_ranks)

    if is_flush:
        suited_cards = [card for card in hand if card.suit == flush_suit]
        suited_ranks = sorted({c.rank.value if isinstance(c.rank, Rank) else c.rank
                           for c in suited_cards})
        if 14 in suited_ranks:
            suited_ranks.append(1)
        if has_straight(suited_ranks):
            return "Straight Flush"


    if count_values[0] == 4:
        return "Four of a kind"

    if count_values[0] == 3 and count_values[1] >= 2:
        return "Full House"

    if is_flush:
        return "Flush"

    if is_straight:
        return "Straight"

    if count_values[0] == 3:
        return "Three of a Kind"


    if count_values[0] == 2 and count_values[1] == 2:
        return "Two Pair"

    if count_values[0] == 2:
        return "One Pair"

    return "High Card"









    return "High Card" # If none of the above, it's High Card

