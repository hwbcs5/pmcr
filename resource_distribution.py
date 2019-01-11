def resource_distribution(graph, uid, k, item_u):
    #graph : list containing three sublists representing user, po, item layers
    #uid : target user's id
    #k : length of recommended item list
    #item_u : target user's item set

    #unselected item list
    unselected_list = []

    #resource preset
    i = 0
    for item in graph[2]:
        if item in item_u:
            item.r = 100
        else:
            unselected_list[i] = item
            i = i + 1
            item.r = 0

    #recommendation part
    for user in graph[0]:
        if user.id == uid:
            continue
        op = []    #the overlapped preference set
        cp = []    #the complementary preference set
        cps = []   #the subsets of the complementary preference set
        cpsindex = {}
        index = 0
        overlapped_items = [i for i in user.item_list if i in item_u]
        #calculate op and cp
        if len(overlapped_items) > 0:
            for prefer in graph[0][uid].pref_list:
                if prefer.preferred in overlapped_items:
                    op.append(prefer)
                else:
                    cp.append(prefer)
                    if (prefer.preferred in cpsindex.keys()):
                        cps[cpsindex[prefer.preferred]].append(prefer)
                    else:
                        cpsindex[prefer.preferred] = index
                        index = index + 1
                        arr = []
                        arr.append(prefer)
                        cps.append(arr)

            if len(cp) == 0:
                continue
            user_res = len(op) / ((len(graph[2])-1) * len(cp))    #unit user resource for redistribution
            #calculate final resources located on each item
            for subset in cps:
                item = subset[0].preferred
                idx = unselected_list.index(item)
                unselected_list[idx].r = unselected_list[idx].r + user_res
        else:
            continue

    return sorted(unselected_list, key=lambda item : item.r, reverse=True)
