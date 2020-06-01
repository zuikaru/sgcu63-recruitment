from typing import List
from collections import deque
import json


def trace_path(parent_map: dict, start, end) -> List[str]:
    """ Construct path from parent map """
    # start with end node
    path = [end]
    # find until we reach start node
    while path[-1] != start:
        # append parent of current node
        path.append(parent_map[path[-1]])
    path.reverse()
    return path


def fileSearch(fileToSearch: str, filesObj: str) -> List[str]:
    """ Search for file given JSON string of file and directory 

    Returns:
        list of possible paths to given file as string. If not found, it will return an empty list
    """
    # parse JSON string
    files_tree = json.loads(filesObj)
    # result list
    result = []
    # BFS routine
    # queue
    queue = deque()
    # store path
    parent = dict()
    # root directory
    parent[''] = None
    queue.append(('', files_tree))
    # search until there is nothing
    while len(queue) > 0:
        current_directory, tree = queue.popleft()
        # search for files in directory (if there is any)
        if '_files' in tree:
            for file_in_dir in sorted(tree['_files']):
                # if found
                if fileToSearch == file_in_dir:
                    # construt path to this file
                    path_to_file = trace_path(parent, '', current_directory)
                    path_to_file.append(file_in_dir)
                    # append to result
                    result.append('/'.join(path_to_file))
        # for each sub directory
        for sub_directory in sorted(tree.keys()):
            # exclude _files key
            if sub_directory != '_files':
                # push to queue
                queue.append((sub_directory, tree[sub_directory]))
                # store path data
                parent[sub_directory] = current_directory
    return result


def main():
    path_to_json = input("Path to JSON: ")
    file_to_search = input("File to search: ")
    with open(path_to_json) as f: files_obj = f.read()
    print(fileSearch(file_to_search, files_obj))

if __name__ == '__main__':
    main()
