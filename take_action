def take_action(current_state_vec, is_stealing ,action, player_side):
    if((is_stealing not in range(0,2))):
        raise Exception("is_stealing must be 0 or 1")

    if (action not in range(0,6)):
        raise Exception("action must be in range of 0 to 5")

    if(player_side==0):
        if(current_state_vec[action]==0):
            return current_state_vec,player_side
        s=0
        for i in range(1, current_state_vec[action] + 1):
            if ((action + i) % 14 == 13):   s+=1

        for i in range(1, current_state_vec[action] + 1 + s):
            if ((action + i) % 14 != 13):   current_state_vec[(action+i)%14] += 1

        old_current_state_vec = current_state_vec[action]
        current_state_vec[action] = int(current_state_vec[action] / 13)

        if ((action + old_current_state_vec) % 14 == 6):
            next_turn = 0
        else:
            next_turn = 1

        if(is_stealing):
            if(((action + old_current_state_vec)%13 in range (0,6)) and (current_state_vec[(action + old_current_state_vec)%13]==1) and (current_state_vec[12-((action + old_current_state_vec)%13)]>0)):
                current_state_vec[(action + old_current_state_vec)%13]=0
                current_state_vec[6]+=(current_state_vec[12-((action + old_current_state_vec)%13)]+1)
                current_state_vec[12-((action + old_current_state_vec)%13)]=0
            else:   pass
        else:   pass


    elif(player_side==1):
        action+=7
        if (current_state_vec[action] == 0):
            return current_state_vec, player_side
        s=0
        for i in range(1, current_state_vec[action] + 1):
            if ((action + i) % 14 == 6):   s+=1

        for i in range(1, current_state_vec[action] + 1 + s):
            if ((action + i) % 14 != 6):    current_state_vec[(action + i) % 14] += 1
            else:   s+=1


        old_current_state_vec = current_state_vec[action]
        current_state_vec[action] = int(current_state_vec[action] / 13)

        if ((action + old_current_state_vec) % 14 == 13):
            next_turn = 1
        else:
            next_turn = 0

        if (is_stealing):
            if (((action + old_current_state_vec)%13 in range (7,13)) and (current_state_vec[(action + old_current_state_vec) % 13] == 1) and (current_state_vec[12-((action + old_current_state_vec)%13)]>0)):
                current_state_vec[(action + old_current_state_vec) % 13] = 0
                current_state_vec[13] += (current_state_vec[12 - ((action + old_current_state_vec) % 13)] + 1)
                current_state_vec[12 - ((action + old_current_state_vec) % 13)] = 0
            else:   pass
        else:   pass

    else:
        raise Exception("player_side must be 0 or 1")

    if (current_state_vec[0] == 0 and current_state_vec[1] == 0 and current_state_vec[2] == 0 and current_state_vec[3] == 0 and current_state_vec[4] == 0 and current_state_vec[5] == 0):
        current_state_vec[13]+=(current_state_vec[12]+current_state_vec[11]+current_state_vec[10]+current_state_vec[9]+current_state_vec[8]+current_state_vec[7])
        current_state_vec[12] = 0
        current_state_vec[11] = 0
        current_state_vec[10] = 0
        current_state_vec[9] = 0
        current_state_vec[8] = 0
        current_state_vec[7] = 0
        if(current_state_vec[6]>current_state_vec[13]):
            print("Player 1 wins! (Blue)")
        elif(current_state_vec[6]<current_state_vec[13]):
            print("Player 2 wins! (Red)")
        elif(current_state_vec[6]==current_state_vec[13]):
            print("It's a Draw!")

    elif(current_state_vec[7]==0 and current_state_vec[8]==0 and current_state_vec[9]==0 and current_state_vec[10]==0 and current_state_vec[11]==0 and current_state_vec[12]==0):
        current_state_vec[6] += (current_state_vec[0] + current_state_vec[1] + current_state_vec[2] + current_state_vec[3] +current_state_vec[4] + current_state_vec[5])
        current_state_vec[0] = 0
        current_state_vec[1] = 0
        current_state_vec[2] = 0
        current_state_vec[3] = 0
        current_state_vec[4] = 0
        current_state_vec[5] = 0
        if (current_state_vec[6] > current_state_vec[13]):
            print("Player 1 wins! (Blue)")
        elif (current_state_vec[6] < current_state_vec[13]):
            print("Player 2 wins! (Red)")
        elif (current_state_vec[6] == current_state_vec[13]):
            print("It's a Draw!")

    return current_state_vec,next_turn
