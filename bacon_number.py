# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 22:56:47 2023

@author: jeonghin@umich.edu
"""

class Node:
    def __init__(self, value):
        """Initialize a Node object with the given value."""
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self, values=None):
        """Initialize a LinkedList object."""
        self.head = None
        self.tail = None
        self.size = 0

        if values is not None:
            for value in values:
                self.append(value)

    def is_empty(self):
        """
        Check if the linked list is empty.

        Returns:
            bool: True if the linked list is empty, False otherwise.
        """
        return self.size == 0

    def append(self, item):
        """Add an item to the end of the linked list."""
        new_node = Node(item)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def pop_left(self):
        """Removes the front node and returns the data in that node."""
        if self.is_empty():
            return None
        node_to_remove = self.head
        if self.size == 1:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
        self.size -= 1
        return node_to_remove.value

    def size(self):
        """
        Return the size of linked list
        
        Returns:
            int: The size of linked list.
        """
        return self.size

class DefaultListDict:
    
    def __init__(self):
        """Initialize a DefaultListDict object."""
        self.dict = {}

    def __getitem__(self, key):
        """Return the values of a given key"""
        if key not in self.dict:
            self.dict[key] = []
        return self.dict[key]

    def __setitem__(self, key, value):
        """Set the values of a given key"""
        self.dict[key] = value

    def __contains__(self, key):
        """
        Return if key is present in a DefaultListDict object.
        
        Returns:
            bool: True if key is present in a DefaultListDict object, False otherwise.        
        """
        return key in self.dict

    def keys(self):
        """Return the keys of a DefaultListDict object."""
        return self.dict.keys()

    def values(self):
        """Return the values of a DefaultListDict object."""
        return self.dict.values()

    def items(self):
        """Return the items of a DefaultListDict object."""
        return self.dict.items()

def read_movie_data(file_path):
    '''
    Read movie data from a text file.

    Parameters:
        file_path (str): The location of the text file.

    Returns:
        dict: A dictionary where keys are movie names and values are lists of actors in each movie.
    '''
    movie_actors = {}


    with open(file_path, 'r', errors = 'ignore') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace and newlines
            if line:
                parts = line.split('/')
                movie = parts[0].strip()
                actors = [actor.strip() for actor in parts[1:]]

                # movies.append(movie)

                for actor in actors:
                    if len(actor.split(', ')) == 2:
                        full_name = actor.split(', ')[1] + " " + actor.split(', ')[0] 
                        
                    else:
                        full_name = actor.split(', ')[0]                         
                        
                    # if full_name not in actor_movies:
                    #     actor_movies[full_name] = []
                    # actor_movies[full_name].append(movie)
                    
                    if movie not in movie_actors:
                        movie_actors[movie] = []
                    movie_actors[movie].append(full_name)

    return movie_actors

def actor_colab(movie_actors):
    '''
    Create a dictionary of actor collaborations based on movie data.

    Parameters:
        movie_actors (dict): A dictionary where keys are movie names and values are lists of actors in each movie.

    Returns:
        dict: A dictionary where keys are actor names and values are lists of other actors they have acted with.
    '''
    actor_collaborations = DefaultListDict()
    
    for movie, actors in movie_actors.items():
        for i in range(len(actors)):
            actor1 = actors[i]
            for j in range(i+1, len(actors)):
                actor2 = actors[j]
                actor_collaborations[actor1].append(actor2)
                actor_collaborations[actor2].append(actor1)

    return actor_collaborations

    
def find_shortest_path(graph, actor1, actor2):
    '''
    Find the shortest path between two actors in a graph.

    Parameters:
        graph (dict): A graph representation where keys are actor names and values are lists of other actors they have acted with.
        actor1 (str): The name of the first actor.
        actor2 (str): The name of the second actor.

    Returns:
        list: The shortest path as a list of actor names.
        int: The number of degrees of separation between the two actors.
    '''    
    queue = LinkedList([(actor1, 0)])
    prev = {}
    visited = {actor1}
    
    while queue:
        if not queue.is_empty():
            node, dist = queue.pop_left()
            if node == actor2:
                break
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append((neighbor, dist + 1))
                    visited.add(neighbor)
                    prev[neighbor] = node
        else:
            return [], None
                
    #length_of_shortest_path = dist
    shortest_path = []
    actor = actor2
    while actor:
        shortest_path.append(actor)
        if actor not in prev:
            break
        actor = prev[actor]
        
    #print(shortest_path)
    return shortest_path, dist

def main():
    '''
    The main function that performs the main logic of the program.
    '''
    
    file_path = "BaconCastFull.txt"
    graph = actor_colab(read_movie_data(file_path))   


    # Calculating the mean and median so that it can be displayed when the user quits the program.
    
    distance_KB = DefaultListDict()
    visited = set()
    visited.update("Kevin Bacon")

    num_key = 0
    cum_sum = 0
    cum_list = []
    c = 0
    ans_median = 0

    while True:
        c += 1
        ans = set()
        if c == 1:
            ans = set(j for i in graph["Kevin Bacon"] for j in graph[i])
            ans = ans - visited

            distance_KB[c].append(list(ans))

            visited.update(ans)

            num_key += len(ans)
            cum_sum += c * len(ans)
            cum_list += [c] * len(ans)
            
        else:
            for i in distance_KB[c-1][0]:
                for j in graph[i]:
                    ans.add(j)
            
            ans = ans - visited  

            if ans:
                 

                distance_KB[c].append(list(ans))
                visited.update(ans)

                num_key += len(ans)
                cum_sum += c * len(ans)
                cum_list += [c] * len(ans)

            else:
                break

    if num_key % 2 == 1:
        ans_median = cum_list[num_key // 2]
    else:
        middle = num_key // 2
        ans_median = (cum_list[middle - 1] + cum_list[middle]) / 2
        
        
        
        
    # Allow user to enter the actors' names to find their degree of separation.
    
    while True:
        actor1 = input("Enter the name of the first actor: ")
        actor2 = input("Enter the name of the second actor: ")      

        if actor1 not in graph or actor2 not in graph:
            print("One or both actors not found. Please try again.")
            continue

        if actor1 == actor2:
            print("They are the same person, so they have 0 degree of separation")
            response = input("Do you want to find degrees of separation between other actors? (yes/no): ")
            if response.lower() != 'yes':
                break
            else:
                continue
            
        else:
            shortest_path, degrees_of_separation = find_shortest_path(graph, actor1, actor2)
            
        if degrees_of_separation:
            print(shortest_path)
            print(f"{actor1} is {degrees_of_separation} degrees of separation from {actor2}")
        else:
            print(f"No path found between {actor1} and {actor2}")
                    

        response = input("Do you want to find degrees of separation between other actors? (yes/no): ")
        if response.lower() != 'yes':
            break

    print("Mean: ", round(cum_sum/num_key, 3))
    print("Median: ", ans_median)

        
if __name__ == '__main__':
    main()