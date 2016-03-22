import importlib
import sys

#----------------------------------------------------------------------
def dynamic_importer(name, class_name):
    """
    Dynamically imports modules / classes
    """
    try:
        fp, pathname, description = importlib.find_loader()
    except ImportError:
        print("unable to locate module: " + name)
        return None, None

    try:
        example_package = importlib.load_module(name, fp, pathname, description)
    except Exception as e:
        print(e)

    try:
        myclass = importlib.load_module("%s.%s" % (name, class_name), fp, pathname, description)
        print(myclass)

    except Exception as e:
        print(e)

    return example_package, myclass

if __name__ == "__main__":
    module, modClass = dynamic_importer("my_keywords", "Keywords")

