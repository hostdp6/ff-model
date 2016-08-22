STATS_BOOK = 'NFL Stats'
PROJECTION_SHEET = 'DH PROJECTIONS'
YEARS_WEIGHT = {
    '2015': 4,
    '2014': 2,
    '2013': 1
}
YEARS_PENALTY = {
    '2015': 0.9
}
PROJ_YEAR = '2016'
SCORING = {
    'PASSING': {
        'TD': 4.0,
        'YDS': 0.04,
        'INT': -1.0,
        '2PC': 1.0,
        '4YP': 1.0,
        'FUML': -1.0,
    },
    'RUSHING': {
        'YDS': 0.1,
        '2PR': 2.0,
        'TD': 6.0,
        '2YR': 1.0,
        'FUML': -1.0,
    },
    'RECEIVING': {
        'YDS': 0.1,
        'TD': 6.0,
        'REC': 0.5,
        '2PC': 2.0,
        '2YR': 1.0,
        'FUML': -1.0,
    },
    'KICKING': {
        'PAT': 1.0,
        'FG39': 3.0,
        'FG49': 3.0,
        'FG50': 4.0,
        'MISS': -1.0
    },
    'DEFENSE': {
        'SA': 1.0,
        'TD': 6.0,
        'BLKK': 2.0,
        'INT': 2.0,
        'FR': 2.0,
        'SF': 2.0,
        'PA0': 10.0,
        'PA1': 7.0,
        'PA7': 4.0,
        'PA14': 1.0,
        'PA22': -1.0,
        'PA28': -3.0,
        'PA35': -5.0,
        'PA46': -8.0
    }
}
