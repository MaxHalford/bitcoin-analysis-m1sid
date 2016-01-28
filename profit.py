NONCE = pow(2, 32)


def hashes_per_day(difficulty, hashrate):
    '''
    Returns the average number of hashes found in one day.

    - difficulty: provided by the system
    - hashrate: hashes per second
    '''
    return 24 / (difficulty * NONCE / hashrate / 3600)


def power_cost_per_day(consumption, price):
    '''
    Return the electricity cost per day.

    - consumption: electricity consumption per hour
    - rate: electricity price per hour
    '''
    return 24 * consumption * price

difficulty = 20000
hashrate = pow(10, 9)

print(hashes_per_day(difficulty, hashrate))
