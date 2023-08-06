from pathlib import Path

def crawl(
    path: str,
    start_depth: int = 0,
    end_depth: int = -1,
    *,
    skip_permission_error: bool = True) -> tuple:

    # path validation
    working_dir = None

    if type(path) == Path:
        working_dir = path
    elif type(path) == str:
        working_dir = Path(path)
    else:
        raise TypeError("'path' must be a str or Path")
    
    if not working_dir.is_dir():
        raise ValueError("'path' must point to a directory")

    # start_depth validation
    if type(start_depth) != int:
        raise TypeError("'start_depth' must be of type int")
    if start_depth < 0:
        raise ValueError("'start_depth' must be greater than or equal to 0")

    # end_depth validation
    if type(end_depth) != int:
        raise TypeError("'end_depth' must be of type int")
    
    # skip_permission_error validation
    if type(skip_permission_error) != bool:
        raise TypeError("'skip_permission_error' must be of type bool")

    depth_zero = working_dir.iterdir()
    pending_dirs = []

    dirs = []
    files = []

    # depth zero
    for i in depth_zero:
        if i.is_dir():
            if start_depth <= 0 and end_depth > 0:
                dirs.append(i)

            pending_dirs.append({
                'path': Path(i),
                'depth': 1
            })
        if start_depth <= 0 and i.is_file():
            files.append(i)

    while len(pending_dirs) > 0:
        current_dir = pending_dirs.pop()
        if end_depth != -1 and current_dir['depth'] > end_depth: # if depth exceeded skip
            continue
        
        is_chosen_depth = current_dir['depth'] >= start_depth and (end_depth == -1 or current_dir['depth'] < end_depth) 
         
        try:
            for i in current_dir['path'].iterdir(): # loop over all subdirs
                if i.is_dir():
                    pending_dirs.append({'path': i, 'depth': current_dir['depth'] + 1})
                    if is_chosen_depth:
                        dirs.append(i)
                elif i.is_file() and is_chosen_depth:
                    files.append(i)
        
        except PermissionError:
            if not skip_permission_error:
                print(f'[PERMISSIONERROR] {current_dir.path}')
            continue
    
    return files, dirs