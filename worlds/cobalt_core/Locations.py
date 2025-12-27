location_table = {f'Card Draw {i}': 185000 + i for i in range(1, 10+1)} \
    | {f'Rare Card Draw {i}': 186000 + i for i in range(1, 2+1)} \
    | {f'Artifact {i}': 187000 + i for i in range(1, 7+1)} \
    | {f'Boss Artifact {i}': 188000 + i for i in range(1, 2+1)} \
    | {f'Act {i} Boss': None for i in range(1, 3+1)}
