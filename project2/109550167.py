import STcpClient_1 as STcpClient
import numpy as np
import random
import copy
import time
'''
    input position (x,y) and direction
    output next node position on this direction
'''
def Next_Node(pos_x,pos_y,direction):
    if pos_y%2==1:
        if direction==1:
            return pos_x,pos_y-1
        elif direction==2:
            return pos_x+1,pos_y-1
        elif direction==3:
            return pos_x-1,pos_y
        elif direction==4:
            return pos_x+1,pos_y
        elif direction==5:
            return pos_x,pos_y+1
        elif direction==6:
            return pos_x+1,pos_y+1
    else:
        if direction==1:
            return pos_x-1,pos_y-1
        elif direction==2:
            return pos_x,pos_y-1
        elif direction==3:
            return pos_x-1,pos_y
        elif direction==4:
            return pos_x+1,pos_y
        elif direction==5:
            return pos_x-1,pos_y+1
        elif direction==6:
            return pos_x,pos_y+1


def checkRemainMove(mapStat):
    free_region = (mapStat == 0)
    temp = []
    for i in range(len(free_region)):
        for j in range(len(free_region[0])):
            if(free_region[i][j] == True):
                temp.append([i,j])
    return temp


'''
    輪到此程式移動棋子
    mapStat : 棋盤狀態(list of list), 為 12*12矩陣, 0=可移動區域, -1=障礙, 1~2為玩家1~2佔領區域
    gameStat : 棋盤歷史順序
    return Step
    Step : 3 elements, [(x,y), l, dir]
            x, y 表示要畫線起始座標
            l = 線條長度(1~3)
            dir = 方向(1~6),對應方向如下圖所示
              1  2
            3  x  4
              5  6
'''
def end(cur_map):
    return not (cur_map==0).any()

def next_map(player, cur_map, move):
    [move_pos_x, move_pos_y] = move[0]  # expected [x,y]
    steps = move[1]  # how many step
    move_dir = move[2]  # 1~6

    next_x = move_pos_x
    next_y = move_pos_y
    cur_map[next_x][next_y] = player
    for i in range(steps - 1): 
        [next_x, next_y]=Next_Node(next_x,next_y,move_dir)
        cur_map[next_x][next_y] = player

    return cur_map

def checkRemainMove(cur_map):
    free_region = (cur_map == 0)
    temp = []
    for i in range(len(free_region)):
        for j in range(len(free_region[0])):
            if(free_region[i][j] == True):
                temp.append([i,j])
    return temp

def legalaction(cur_map):
    free = checkRemainMove(cur_map)
    actions = []
    visit = np.zeros([144, 144])
    for i, j in free:
        if cur_map[i][j] != 0:
            continue
        else:
            actions.append([(i,j), 1, 1])
            legal = []
            for dir in range(1,7):
                [next_x, next_y] = Next_Node(i, j, dir)
                if next_x < 0 or next_x > 11 or next_y < 0 or next_y > 11 or cur_map[next_x][next_y]!=0:
                    continue
                else:
                    if(visit[i+j*12][next_x+next_y*12] == 1):
                        continue
                    actions.append([(i, j), 2, dir])
                    visit[i+j*12][next_x+next_y*12] = visit[next_x+next_y*12][i+j*12] = 1
                    [next_x, next_y] = Next_Node(next_x, next_y, dir)
                    if next_x < 0 or next_x > 11 or next_y < 0 or next_y > 11 or cur_map[next_x][next_y]!=0:
                        continue
                    else:
                        actions.append([(i, j), 3, dir])
    # if(len(actions) > 15):
    #     actions = random.sample(actions, 1)
    return actions

def minimax(player, depth, cur_map, alpha, beta):
    if end(cur_map):
        if player == 1:
            score = 100
        else:
            score = -100
        return [None, score]
    if depth == 0:
        actions = np.array(legalaction(cur_map), dtype=object)
        if np.all(actions[:,2] == 1):
            if(len(actions)%2 == 1):
                if player == 1:
                    score = -99
                else:
                    score = 99
            else:
                if player == 1:
                    score =  99
                else:
                    score = -99
        else:
            score = 0
        return [None, score]
    actions = legalaction(cur_map)
    random.shuffle(actions)
    scores = []
    if len(actions) > 19:
        return [actions[0], 0]

    if player == 1:
        best_action = None
        best_score = float("-inf")
        for action in actions:
            new_map = copy.deepcopy(cur_map)
            new_map = next_map(1, new_map, action)
            _, score = minimax(2, depth-1, new_map, alpha, beta)
        #     scores.append((action, score))
        # best_action, best_score = max(scores, key=lambda item: item[1])
            if best_action is None:
                best_action = action
            if score > alpha:
                best_score = alpha = score
                best_action = action
            if beta <= alpha:
                break
        return [best_action, best_score]
    # opponent minimize
    else:
        min_action = None
        min_score = float("inf")
        for action in actions:
            new_map = copy.deepcopy(cur_map)
            new_map = next_map(2, new_map, action)
            _, score = minimax(1, depth-1, new_map, alpha, beta)
        #     scores.append((action, score))
        # min_action, min_score = min(scores, key=lambda item: item[1])
            if min_action is None:
                min_action = action
            if score < beta:
                    min_score = beta = score
                    min_action = action
            if beta <= alpha:
                break
        return [min_action, min_score]
    
def Getstep(mapStat, gameStat):
    #Please write your code here
    #TODO
    
    step, _ = minimax(1, 9, mapStat, float('-inf'), float('inf'))
    print(_)
    
    # #Please write your code here
    return step
    


# start game
print('start game')
while (True):

    (end_program, id_package, mapStat, gameStat) = STcpClient.GetBoard()
    if end_program:
        STcpClient._StopConnect()
        break
    
    decision_step = Getstep(mapStat, gameStat)
    
    STcpClient.SendStep(id_package, decision_step)