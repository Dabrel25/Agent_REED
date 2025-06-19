import os

def simple_test():
    try:
        print("Testing basic os functions...")
        path = os.path.abspath("calculator")
        print(f"Absolute path: {path}")
        items = os.listdir(path)
        print(f"Directory contents: {items}")
        
        for item in items:
            item_path = os.path.join(path, item)
            print(f"Processing: {item}")
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            print(f"  Size: {size}, Is dir: {is_dir}")
            
    except Exception as e:
        print(f"Error: {e}")
        print(f"Error type: {type(e)}")

simple_test()