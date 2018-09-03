import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import baker
import os


def init_matrix(grid_size, states=2):
    """
    This function will generate a randomized grid. Based on the number of of states, the values can range from 0 to
    n states.
    :param grid_size:
    :param states:
    :return:
    """
    return np.random.randint(states, size=(grid_size, grid_size))


def init_animation(grid_size, neighborhood_size, states, interval, save_count, frames):
    """
    This function starts off the whole animation. It takes in the grid size desired to generate a randomized grid based
    the number of states, 2 being binary. The interval is the delay between frames in milliseconds, the save_count is
    the number of values from frames to cache, and the number of frames to run.
    :param grid_size:
    :param neighborhood_size:
    :param states:
    :param interval:
    :param save_count:
    :param frames:
    :return:
    """
    fig, ax = plt.subplots()
    grid = init_matrix(grid_size, states)
    img = ax.imshow(grid, interpolation='nearest')
    visual = animation.FuncAnimation(fig=fig, func=update_tick,
                                     fargs=(img, grid, neighborhood_size, rule_original),
                                     frames=frames, interval=interval, save_count=save_count)
    visual.save(os.path.join(os.getcwd(), 'output.html'), fps=100, extra_args=['-vcodec', 'libx264'])
    plt.show()
    return visual


def update_tick(frame, img, grid, neighborhood_size, rule_function):
    """
    This function is used to update each frame based on the rule function passed with the parameter being the sum of the
    surrounding neighbors.
    :param frame: The frame that is being updated, this is only used as part of the init_animation function.
    :param img: The image for animation at the current status.
    :param grid: The grid at its current state to make changes to.
    :param neighborhood_size: The size of the neighborhood being evaluated.
    :param rule_function: The rule function being used with the params being the sum, cell's current state, and
    neighborhood size
    :return:
    """
    # TODO add multiprocessing
    assert neighborhood_size % 8 == 0, "Size must be divisible by 8"
    new_grid = grid.copy()
    # iterate through the grid and find what state the cell should be changed to
    for i, row in enumerate(new_grid):  # iterate through rows
        for j, cell in enumerate(row):  # iterate through columns in row
            current_state = new_grid[i, j]  # cell of reference
            ring = neighborhood_size/8
            sum = 0
            for i_r in np.arange(-ring, ring+1):
                for j_r in np.arange(-ring, ring+1):
                    if j_r != 0 or i_r != 0:
                        try:
                            row = i+i_r
                            col = j+j_r
                            if row >= 0 and col >= 0:
                                sum += grid[i + i_r, j + j_r]
                        except IndexError:
                            pass
            new_grid[i, j] = rule_function(sum, current_state, neighborhood_size)
    # update image to reflect the change in states
    img.set_data(new_grid)
    # update grid to reflect change in states
    grid[:] = new_grid[:]
    return img


def rule_original(neighbors_sum, current_state):
    """
    This is the original rule in Conway's Game of Life.
    :param neighbors_sum:
    :param current_state:
    :return:
    """
    if neighbors_sum < 2 or neighbors_sum > 3:
        return 0
    elif neighbors_sum == 2:
        return current_state
    elif neighbors_sum == 3:
        return 1


@baker.command
def run(grid_size=50, neighborhood_size=8, states=2, interval=1, save_count=50, frames=100):
    """
    This runs the program. Can start in the command line with:
    python GOL.py run --grid_size 50 --neighborhood_size 8 --states 2 --interval 1 --save_count 50 --frames 100
    :param grid_size:
    :param neighborhood_size:
    :param states:
    :param interval:
    :param save_count:
    :param frames:
    :return:
    """
    init_animation(grid_size, neighborhood_size, states=states, interval=interval,
                   save_count=save_count, frames=frames)


if __name__ == '__main__':
    baker.run()