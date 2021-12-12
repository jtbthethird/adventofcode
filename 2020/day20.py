import template
import copy
import regex as re
import math 
import numpy as np
import plotly.express as px

filename="input20.txt"
# filename="testinput20.txt"

input = []
with open(filename) as f:
    input = [groups.split('\n') for groups in f.read().split('\n\n')]
    # input = f.readlines()
    # input = [int(x.strip()) for x in input[0].split(',')]
    # input = [[z for z in x.strip()] for x in input]
    # input = [x.strip() for x in input]
    
# --- #
def get_edges(tile_data):
    return [
        tile_data[0], # Top
        tile_data[:,0], # Left
        tile_data[-1], # Bottom 
        tile_data[:,-1] # Right
    ]

class Tile:
    def __init__(self, tile_str):
        self.tile_id = int(tile_str[0].split(' ')[1][:-1])
        t_data = [[z for z in row] for row in tile_str[1:]]
        self.tile_data = np.array(t_data)
        self.edges = get_edges(self.tile_data)
        
        self.open_edges = [0,1,2,3]
        
        self.adjascent_tiles = [None, None, None, None]
        # if 
        
    def flip_x(self):
        self.tile_data = np.flip(self.tile_data, 1)
        self.edges = get_edges(self.tile_data)
        
    def flip_y(self):
        self.tile_data = np.flip(self.tile_data, 0)
        self.edges = get_edges(self.tile_data)
    
    def rotate_ccw(self, times):
        self.tile_data = np.rot90(self.tile_data, times)
        self.edges = get_edges(self.tile_data)
        
    def strip_borders(self):
        self.tile_data = self.tile_data[1:-1,1:-1]
    
    
    def has_natural_edge_match(self, other_tile):
        # Just find a match for the right edge
        for i in self.open_edges:
            e1 = self.edges[i]            
            e2_index = (i+2)%4
            # print("matching edge %d with other edge %d"%(i, other_tile.edges[]))
            e2 = other_tile.edges[e2_index]
            if (e1 == e2).all():
                # We have a match
                # print("Natural Match", self.tile_id, other_tile.tile_id, "edge: ", i)
                return i
        return -1
    
    def match_other_tile(self, other_tile):
        for i in range(4):
            other_tile.rotate_ccw(1)
        
            h = self.has_natural_edge_match(other_tile)
            if h >= 0:
                # print("Found a match for myself. I am %d"%self.tile_id)
                # print(self.tile_data)
                # print("Matched other tile %d"%other_tile.tile_id)
                # print("Matched in direction %d"%h)
                # print(other_tile.tile_data)
                return h
        other_tile.flip_x()
        for i in range(4):
            other_tile.rotate_ccw(1)
        
            h = self.has_natural_edge_match(other_tile)
            if h >= 0:
                # print("Found a match for myself. I am %d"%self.tile_id)
                # print(self.tile_data)
                # print("Matched other tile %d"%other_tile.tile_id)
                # print("Matched in direction %d"%h)
                # print(other_tile.tile_data)
                return h
        return -1
    
    def find_matching_tiles(self, other_tiles):
        # Check the natural edges, then rotate, then flip, then rotate
        matches = []
        
        for t in other_tiles:
            m = self.match_other_tile(t)
            if m >= 0:
                matches.append((m, t))
        return matches


def index_from_direction(my_idx, direction):
    adder = [
        (0, -1),
        (-1, 0),
        (0, 1),
        (1, 0)
    ][direction]

    return (my_idx[0] + adder[0], my_idx[1] + adder[1])

def insert_value_into_map(tmap, value, idx):
    (ydim, xdim) = tmap.shape
    if idx[0] < 0:
        tmap = np.insert(tmap, 0, 0, axis=1)
        idx = (idx[0]+1, idx[1])
    elif idx[0] >= tmap.shape[1]:
        tmap = np.insert(tmap, tmap.shape[1], 0, axis=1)
    if idx[1] < 0:
        tmap = np.insert(tmap, 0, 0, axis=0)
        idx = (idx[0], idx[1]+1)
    elif idx[1] >= tmap.shape[0]:
        tmap = np.insert(tmap, tmap.shape[0], 0, axis=0)
    tmap[idx[1]][idx[0]] = value
    return tmap
    

def build_map(all_tiles):
    ## Put the first tile in a map
    
    # For each edge, find a tile that matches its edge
    # If those tiles aren't already in the map, add them
    # If those tiles wen're already in the map, do this with those tiles     
    
    
    # To find a matching tile edge:
    #     # Try each naturally connecting edge
    #     # Rotate and try again (3x)
    #     # Flip, then try again with rotates (3x) 
    
    # When you find a match,
    #     Add it to the map
    #.    Remove the free edge from both
    #.    Add it to the queue to search
    
    all_tiles_copy = copy.copy(all_tiles)
    
    tile = all_tiles.pop(0)
    
    tile_map = np.array([[tile.tile_id]])
    
    x = 0
    y = 0
    
    tiles_to_search = [tile]
    
    while len(tiles_to_search) > 0:
        t = tiles_to_search.pop(0)
        
        matches = t.find_matching_tiles(all_tiles)
        # print("MATCHES: ", matches)
        for (direction, other_tile) in matches:            
            tiles_to_search.append(other_tile)
            
            my_np_idx = np.where(tile_map==t.tile_id)
            my_idx = (my_np_idx[1][0], my_np_idx[0][0])
            new_idx = index_from_direction(my_idx, direction)
            # print(tile_map, my_idx)
            # print("New tile %d should get inserted at "%other_tile.tile_id, new_idx)
            tile_map = insert_value_into_map(tile_map, other_tile.tile_id, new_idx)

            # Add other_tile to the map
            t.adjascent_tiles[direction] = other_tile
            other_tile.adjascent_tiles[(direction+2)%4] = t
            
            # Remove the free edge
            t.open_edges.remove(direction)
            other_tile.open_edges.remove((direction+2)%4)
        
            all_tiles = [x for x in all_tiles if x.tile_id != other_tile.tile_id]
        
        # print(tile_map)
    return tile_map
        
def create_clean_map(m):
    output = np.array([[]])

        
def part1():
    tiles = []
    for tile_str in input:
        t = Tile(tile_str)
        tiles.append(t)
        
    m = build_map(tiles)
    
    print(m)
    
    return m[0][0] * m[0][-1] * m[-1][0] * m[-1][-1]

def map_to_str(m):
    x = '\n'.join([''.join([v for v in row]) for row in m])
    return x


def get_monster_count(bmap):
    
    # smon_top_full=r"^                  \# .*".replace(' ', '.')
    # smon_middle=r"^(.*)#....##....##....###(.*)$"
    # smon_bot_full=r"^ \#  \#  \#  \#  \#  \#   .*".replace(' ', '.')
    # print("smontop", smon_top_full)
    
    smon_top_grouped = r"^(..................)\#(.*)$"
    smon_mid_grouped = r"#(....)##(....)##(....)###(.*)$"
    smon_bot_grouped = r"^(.)#(..)#(..)#(..)#(..)#(..)#(.*)$"
    
    # smon_top_xs = "                  # ".replace(' ', '_').replace('#', 'X')
    # smon_mid_xs = "#    ##    ##    ###".replace(' ', '_').replace('#', 'X')
    # smon_bot_xs = " #  #  #  #  #  #   ".replace(' ', '_').replace('#', 'X')
    
    

    smon_top_0s = r"\1o\2"
    smon_mid_0s = r"o\1oo\2oo\3ooo\4"
    smon_bot_0s = r"\1o\2o\3o\4o\5o\6o\7"
    # smon=r"..................(#)..*$\n^.*(#)....(##)....(##)....(###).*\n^.*.(#)..(#)..(#)..(#)..(#)..(#)..."
    
    monster_found = False
    monsters_found = 0
    strs = [''.join(row) for row in bmap]
    
    
    for i, row_str in enumerate(strs[1:-1]):
        row_has_monster = False
        x = re.search(smon_mid_grouped, strs[i+1])
        
        while x is not None:
            prefix = x.start()
            # print("\nRow: %d, Prefix: "%(i+1), prefix)
            # print("Match: ", x, x.span(), x.groups())
            #
            # print(i, strs[i]) #, len(smon_top_xs))
            # print(i+1, strs[i+1]) #, prefix, x.group(1), x.start(2))
            # print(i+2, strs[i+2])

            
            top_match = re.match(smon_top_grouped, strs[i][prefix:])
            if top_match is not None:
                # print("Top match: ", top_match.groups())
                bot_match = re.match(smon_bot_grouped, strs[i+2][prefix:])
                if bot_match is not None:
                    
                    # print("new rows:")
                    trow = strs[i][:prefix] + re.sub(smon_top_grouped, smon_top_0s, strs[i][prefix:])
                    mrow = re.sub(smon_mid_grouped, smon_mid_0s, strs[i+1])
                    brow = strs[i+2][:prefix] + re.sub(smon_bot_grouped, smon_bot_0s, strs[i+2][prefix:])
                    
                    
                    # print(i, trow)
                    # print(i+1, mrow)
                    # print(i+2, brow)
                    
                    strs[i] = trow
                    strs[i+1] = mrow
                    strs[i+2] = brow
                    print("!! MONSTER FOUND AT (%d, %d)"%(prefix, i))
                    monsters_found += 1
                    row_has_monster = True
                    
            if row_has_monster:
                x = re.search(smon_mid_grouped, strs[i+1])
                # print("searching again: ", x)
                # print(strs[i+1])
            else:
                x = None

    if monsters_found > 0:
        print()
        for i, row_str in enumerate(strs):
            # x = re.search(smon_middle, row_str)
            print(i, row_str)
        # print("MY COUNT: ", '\n'.join(strs).count('#'))
    return monsters_found
        
def part2():
    tiles = []
    tile_map = {}
    for tile_str in input:
        t = Tile(tile_str)
        tiles.append(t)
        tile_map[t.tile_id] = t
        
    m = build_map(tiles)
    
    t_vec = np.vectorize(lambda t: tile_map[t])
    m2 = t_vec(m)
    
    big_map = None
    for row in m2:
        r = None
        for t in row:
            t.strip_borders()
            if r is None:
                r = t.tile_data
            else:
                r = np.concatenate((r, t.tile_data), axis=1)
        if big_map is None:
            big_map = r
        else:
            big_map = np.concatenate((big_map, r), axis=0)
    
    
    for i in range(4):
        # print("\nChecking for monsters")
        big_map = np.rot90(big_map, 1)
        c = get_monster_count(big_map)
        if c > 0:
            print(map_to_str(big_map))
            return map_to_str(big_map).count('#') - 15*c
            
    big_map = np.flip(big_map, 0)
    
    for i in range(4):
        # print("\nChecking for monsters")
        big_map = np.rot90(big_map, 1)
        c = get_monster_count(big_map)
        if c > 0:
            # print()
            # print(map_to_str(big_map))
            return map_to_str(big_map).count('#') - 15*c
            
    return -1

# --- #

if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    template.funWrapper(part2, "Part 2")

    
        