


def sort_reslution(res_set):

    converted_set_to_list=res_set
    print(converted_set_to_list)

    new_res_list_sorted=[]



    new_res_list_sorted=[i.replace("p","") for i in converted_set_to_list]
    new_res_list_sorted=[int(i) for i in new_res_list_sorted]

    new_res_list_sorted.sort(reverse=True)

    converted_set_to_list.clear()
    converted_set_to_list.extend(new_res_list_sorted)
    converted_set_to_list=[str(i) + "p" for i in converted_set_to_list]



    return converted_set_to_list






