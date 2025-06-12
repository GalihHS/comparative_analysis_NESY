
from collections import deque
import scallopy

def find_all_linking_paths(graph, start, end, max_length, max_path_amount):
    linking_paths = [] 

    current_node, current_path = start, [start]
    queue = deque([(current_node, current_path)])

    while len(queue) != 0 and len(linking_paths) < max_path_amount:
        current_node, current_path = queue.popleft()

        if len(current_path) > max_length:
            continue

        if current_node == end:
            linking_paths.append(current_path)
            continue

        if current_node not in graph:
            continue

        for neighbor in graph[current_node]:
            if neighbor in current_path:
                continue

            new_path = current_path + [neighbor]
            queue.append((neighbor, new_path))

    return linking_paths



def create_graph_dict(graph):
    final_graph = {}

    for triple in graph:
        # Split the line by tab to extract the node connections
        node_a = triple[0]
        node_b = triple[2]
        
        # Check if node_a is already in the graph dictionary
        if node_a in final_graph:
            final_graph[node_a].append(node_b)
        else:
            final_graph[node_a] = [node_b]
    
    return final_graph


def create_sub_graph(graph_file_path, needed_nodes):
    graph = []

    # Open and read the file line by line
    """with open(graph_file_path, 'r') as file:
        graph = []
        for i in range(17):
            graph.append([])
        for line in file:
            # Split the line by tab to extract the node connections
            node_a, relation, node_b = line.strip().split('\t')
            
            # Convert node_a and node_b to integers
            node_a, node_b = int(node_a), int(node_b)
            relation_id = relation_dict[relation]

            if node_a in needed_nodes and node_b in needed_nodes:
                graph[relation_id].append((node_a, node_b))"""
    
    for i in range(17):
        graph.append([])

    for triple in graph_file_path:
        node_a, relation_id, node_b = triple
        if node_a in needed_nodes and node_b in needed_nodes:
            graph[relation_id].append((node_a, node_b))

    
    return graph
    


def metric_computation(predicted_relation_and_score,logic_res_list,relation_dictionary):
    #List of compatible things
    metric = 0
    found = 0
    
    for triple_possible in logic_res_list:
        if triple_possible:
            found = -1
    
    #format of predicted_relation_and_score : (5, 0.4)

    if logic_res_list[predicted_relation_and_score[0]]:
        metric = predicted_relation_and_score[1]
        found = 1
    else:
        metric = - predicted_relation_and_score[1]


    """idées : log, seulement prendre en compte les positifs, ..."""
    return metric, found


def logic_computation_metric(graph,start_node,end_node,rel,K_1,K_2,predicted_relation_and_score,mode):

    #Ontology is supposed to always be the same
    relation_dictionary = {
        "nephew": 0,
        "son": 1,
        "brother": 2,
        "aunt": 3,
        "daughter": 4,
        "niece": 5,
        "wife": 6,
        "mother": 7,
        "husband": 8,
        "father": 9,
        "sister": 10,
        "uncle": 11,
        "cousin": 12,
        "female": 13,
        "grandparent": 14,
        "male": 15,
        "parent": 16
    }
    
    graph_dict = create_graph_dict(graph)


    paths = find_all_linking_paths(graph_dict, start_node, end_node, K_1, K_2)

    needed_nodes = []
    for path in paths:
        for node in path:
            if node not in needed_nodes:
                needed_nodes.append(node)

    reversed_dict = {v: k for k, v in relation_dictionary.items()}

    sub_graph = create_sub_graph(graph, needed_nodes)

    #print(sub_graph)

    ctx = scallopy.ScallopContext()

    ctx.add_relation("nephew",(int,int))
    ctx.add_facts("nephew", sub_graph[0])
    ctx.add_relation("son",(int,int))
    ctx.add_facts("son", sub_graph[1])
    ctx.add_relation("brother",(int,int))
    ctx.add_facts("brother", sub_graph[2])
    ctx.add_relation("aunt",(int,int))
    ctx.add_facts("aunt", sub_graph[3])
    ctx.add_relation("daughter",(int,int))
    ctx.add_facts("daughter", sub_graph[4])
    ctx.add_relation("niece",(int,int))
    ctx.add_facts("niece", sub_graph[5])
    ctx.add_relation("wife",(int,int))
    ctx.add_facts("wife", sub_graph[6])
    ctx.add_relation("mother",(int,int))
    ctx.add_facts("mother", sub_graph[7])
    ctx.add_relation("husband",(int,int))
    ctx.add_facts("husband", sub_graph[8])
    ctx.add_relation("father",(int,int))
    ctx.add_facts("father", sub_graph[9])
    ctx.add_relation("sister",(int,int))
    ctx.add_facts("sister", sub_graph[10])
    ctx.add_relation("uncle",(int,int))
    ctx.add_facts("uncle", sub_graph[11])
    ctx.add_relation("cousin",(int,int))
    ctx.add_facts("cousin", sub_graph[12])
    ctx.add_relation("female",(int))
    ctx.add_facts("female", sub_graph[13])
    ctx.add_relation("grandparent",(int,int))
    ctx.add_facts("grandparent", sub_graph[14])
    ctx.add_relation("male",(int))
    ctx.add_facts("male", sub_graph[15])
    ctx.add_relation("parent",(int,int))
    ctx.add_facts("parent", sub_graph[16])


    ctx.add_rule("aunt(X,Z) = sister(X,Y) and parent(Y,Z)")
    ctx.add_rule("aunt(X,Z) = wife(X,Y) and uncle(Y,Z)")
    ctx.add_rule("aunt(X,Y) = nephew(Y,X) and female(X)")
    ctx.add_rule("aunt(X,Y) = niece(Y,X) and female(X)")
    ctx.add_rule("brother(X,Z) = brother(X,Y) and brother(Y,Z) and X != Z")
    ctx.add_rule("brother(X,Z) = brother(X,Y) and sister(Y,Z) and X != Z")
    ctx.add_rule("brother(X,Y) = brother(Y,X) and male(X)")
    ctx.add_rule("brother(X,Y) = sister(Y,X) and male(X)")
    ctx.add_rule("brother(X,Z) = son(X,Y) and parent(Y,Z) and X != Z")
    ctx.add_rule("cousin(X,Z) = parent(Y,X) and uncle(Y,Z)")
    ctx.add_rule("cousin(X,Z) = parent(Y,X) and aunt(Y,Z)")
    ctx.add_rule("cousin(X,Z) = nephew(X,Y) and parent(Y,Z)")
    ctx.add_rule("cousin(X,Z) = niece(X,Y) and parent(Y,Z)")
    ctx.add_rule("daughter(X,Y) = parent(Y,X) and female(X)")
    ctx.add_rule("daughter(X,Z) = sister(X,Y) and parent(Z,Y)")
    ctx.add_rule("daughter(X,Z) = daughter(X,Y) and husband(Y,Z)")
    ctx.add_rule("daughter(X,Z) = daughter(X,Y) and wife(Y,Z)")
    ctx.add_rule("father(X,Z) = father(X,Y) and brother(Y,Z)")
    ctx.add_rule("father(X,Z) = father(X,Y) and sister(Y,Z)")
    ctx.add_rule("father(X,Y) = son(Y,X) and male(X)")
    ctx.add_rule("father(X,Y) = daughter(Y,X) and male(X)")
    ctx.add_rule("father(X,Y) = parent(X,Y) and male(X)")
    ctx.add_rule("female(X) = mother(X,Y)")
    ctx.add_rule("female(X) = sister(X,Y)")
    ctx.add_rule("female(X) = aunt(X,Y)")
    ctx.add_rule("female(X) = niece(X,Y)")
    ctx.add_rule("female(X) = daughter(X,Y)")
    ctx.add_rule("female(X) = wife(X,Y)")
    ctx.add_rule("grandparent(X,Y) = parent(X,Z) and parent(Z,Y)")
    ctx.add_rule("husband(X,Y) = wife(Y,X) and male(X)")
    ctx.add_rule("husband(X,Y) = parent(X,Z) and parent(Y,Z) and male(X) and X != Y")
    ctx.add_rule("male(X) = father(X,Y)")
    ctx.add_rule("male(X) = brother(X,Y)")
    ctx.add_rule("male(X) = uncle(X,Y)")
    ctx.add_rule("male(X) = nephew(X,Y)")
    ctx.add_rule("male(X) = son(X,Y)")
    ctx.add_rule("male(X) = husband(X,Y)")
    ctx.add_rule("mother(X,Z) = mother(X,Y) and brother(Y,Z)")
    ctx.add_rule("mother(X,Z) = mother(X,Y) and sister(Y,Z)")
    ctx.add_rule("mother(X,Y) = son(Y,X) and female(X)")
    ctx.add_rule("mother(X,Y) = daughter(Y,X) and female(X)")
    ctx.add_rule("mother(X,Y) = parent(X,Y) and female(X)")
    ctx.add_rule("nephew(X,Z) = son(X,Y) and brother(Y,Z)")
    ctx.add_rule("nephew(X,Z) = son(X,Y) and sister(Y,Z)")
    ctx.add_rule("nephew(X,Z) = nephew(X,Y) and husband(Y,Z)")
    ctx.add_rule("nephew(X,Z) = nephew(X,Y) and wife(Y,Z)")
    ctx.add_rule("nephew(X,Y) = uncle(Y,X) and male(X)")
    ctx.add_rule("nephew(X,Y) = aunt(Y,X) and male(X)")
    ctx.add_rule("niece(X,Z) = daughter(X,Y) and brother(Y,Z)")
    ctx.add_rule("niece(X,Z) = daughter(X,Y) and sister(Y,Z)")
    ctx.add_rule("niece(X,Z) = niece(X,Y) and husband(Y,Z)")
    ctx.add_rule("niece(X,Z) = niece(X,Y) and wife(Y,Z)")
    ctx.add_rule("niece(X,Y) = uncle(Y,X) and female(X)")
    ctx.add_rule("niece(X,Y) = aunt(Y,X) and female(X)")
    ctx.add_rule("parent(X,Y) = father(X,Y)")
    ctx.add_rule("parent(X,Y) = mother(X,Y)")
    ctx.add_rule("parent(X,Y) = son(Y,X)")
    ctx.add_rule("parent(X,Y) = daughter(Y,X)")
    ctx.add_rule("sister(X,Z) = sister(X,Y) and brother(Y,Z) and X != Z")
    ctx.add_rule("sister(X,Z) = sister(X,Y) and sister(Y,Z) and X != Z")
    ctx.add_rule("sister(X,Y) = sister(Y,X) and female(X)")
    ctx.add_rule("sister(X,Y) = brother(Y,X) and female(X)")
    ctx.add_rule("sister(X,Z) = daughter(X,Y) and parent(Y,Z) and X != Z")
    ctx.add_rule("son(X,Y) = parent(Y,X) and male(X)")
    ctx.add_rule("son(X,Z) = brother(X,Y) and parent(Z,Y)")
    ctx.add_rule("son(X,Z) = son(X,Y) and husband(Y,Z)")
    ctx.add_rule("son(X,Z) = son(X,Y) and wife(Y,Z)")
    ctx.add_rule("uncle(X,Z) = brother(X,Y) and parent(Y,Z)")
    ctx.add_rule("uncle(X,Z) = husband(X,Y) and aunt(Y,Z)")
    ctx.add_rule("uncle(X,Y) = nephew(Y,X) and male(X)")
    ctx.add_rule("uncle(X,Y) = niece(Y,X) and male(X)")
    ctx.add_rule("wife(X,Y) = husband(Y,X) and female(X)")
    ctx.add_rule("wife(X,Y) = parent(X,Z) and parent(Y,Z) and female(X) and X != Y")

    # Run the scallop program
    ctx.run()

    # Get the results from relation sum_2
    logic_res_list=[False for i in range(17)]

    for i in range(17):
        if i == 13 or i == 15: #female or male
            continue
        for prob, tup in ctx.relation(reversed_dict[i]):
            if prob == start_node and tup == end_node:
                logic_res_list[i] = True


    found_smthg = False
    for i in range(17):
        if logic_res_list[i]:
    #        print("relation possible: ", reversed_dict[i])
            found_smthg = True

    #metric_value, found = metric_computation(predicted_relation_and_score,logic_res_list,relation_dictionary)
    metric_value = predicted_relation_and_score[1]
    
    #REAL found_smthg definition here: we check directly on the completed train graph.
    completed_file_path = "data/family_small/train_sat.txt"
    
    found = 0

    with open(completed_file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()  # Split by whitespace
            # Check if the line has at least 3 parts
            if len(parts) >= 3:
                subject_id = int(parts[0])
                relation_id = relation_dictionary[parts[1]]
                object_id = int(parts[2])
                if found == 0 and subject_id == start_node and object_id == end_node:
                    found = -1
                if (found == -1 or found == 0) and subject_id == start_node and relation_id == rel and object_id == end_node:
                    found = 1


    #if paths != []:
    #print(start_node,end_node)
    metric_value_TRUE = 0
    metric_value_FALSE = 0
    metric_value_NOT_FOUND = 0
    if found == 1:
        metric_value_TRUE += 1
        print(found,metric_value,"heeeeyyyyyyyyyyyyyyyyyyyyyyyyy")
    elif found == -1 :
        metric_value_FALSE += 1
        print(found,-metric_value)
    else:
        metric_value_NOT_FOUND += 1


    return (metric_value_TRUE, metric_value_FALSE, metric_value_NOT_FOUND)

