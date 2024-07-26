from main_feachers.litematic_optimizer import LitematicOptimizer
from main_feachers.ignored_bloks import ignored_blocks

if __name__ == '__main__':
    o = LitematicOptimizer("big_ship.litematic")
    o.set_ignored_blocks(ignored_blocks)
    o.optimize()
