# S4-2026 MakeMeStrong homework

## Repo content

- `login_makeMeStrong.py`: the file to fill-in
- `strong_connectivity.py`: usefull functions
- `files\`: digraphs for your tests (see the readme...)

## Your work

- Write one or several functions with the following specifications:
    - take a digraph G as parameter 
    - make the digraph G strongly connected (add to G the edges to make it strongly connected)
    - return the number of added edges (0 if the digraph is already strongly connected!)
- In your code, only functions not prefixed by `__` will be tested.

### How many edges?

- You cannot add more edges than the number of strongly connected components! (if you want points...)
- Your grade will increase if you can add less edges


## Handout

You can deposit your "contribution": the single file `login_makeMeStrong.py` (do not forget to replace `login`...) on [Moodle](https://moodle.cri.epita.fr/course/view.php?id=1103&section=3)
- As usual your `login_makeMeStrong.py` does not contain tests, but only function definitions
- You can import anything from `algo_py` except `timing` (do not forget to delete the potential `@timing.timing`...)
- You can also import any built-in module
 
- **your submission will not be tested:**
    - if you left `print` or tests
    - if has the wrong name
    
    
## Deadlines

- Sunday, April the 2nd, 10PM: tests with the digraphs in `files`
- Monday, April the 10th, 10PM: more tests...

## Reminders

### Your `.py

- **Remove all `print`!**: **tests should be in another file**
- Do not include test functions to your code: **tests should be in another file**
- Do not import anything except
  - modules in `algo_py` (reminder: `algopy` was renamed `algo_py`)
  - built-in Python modules
  - do not forget to import all modules needed in your code!
  
- **No `from module import *`: the functions imported will be included in our tests :(**
 - All intermediate functions must begin with `__`
 - Your tests should be in another file: so you do not have to comment them...
 - **No decorators**
 
**Test your code!!!!**