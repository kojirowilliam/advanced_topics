yamada = \
       " - 2 2 2 2 2 2 "\
       " - 1 0 0 0 0 2 "\
       " 2 0 1 0 2 0 2 "\
       " 1 0 1 0 0 0 0 "\
       " 2 0 0 0 1 1 2 "\
       " - 2 - 2 2 2 -  "

if __name__ == '__main__':
    from hw4_util import read_world
    assert yamada is not None, "Make sure that you have a variable"\
           "name with your lastname as the configuration of your world"
    print("Parsed world:")
    for r in read_world(yamada):
        print(f"\t{r}")