#!/usr/bin/env python3

from picture import Picture
import math

class SeamCarver(Picture):
    ## TO-DO: fill in the methods below
    def energy(self, i: int, j: int) -> float:
        
        energy_x = 0
        energy_y = 0
        
        for x in range(3):
            if i == self.width()-1:
                energy_x += (self[0, j][x]-self[i-1, j][x])**2
            elif i == 0:
                energy_x += (self[self.width()-1, j][x]-self[i+1, j][x])**2
            else:
                energy_x += (self[i-1, j][x]-self[i+1, j][x])**2
        
        for x in range(3):
            if j == self.height()-1:
                energy_y += (self[i, 0][x]-self[i, j-1][x])**2
            elif j == 0:
                energy_y += (self[i, self.height()-1][x]-self[i, j+1][x])**2
            else:
                energy_y += (self[i, j+1][x]-self[i, j-1][x])**2
        
        energy = math.sqrt(energy_y + energy_x)
        energy_x = 0
        energy_y = 0
        
        return energy
    
        raise NotImplementedError

    def find_vertical_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        vertical seam
        '''
        raise NotImplementedError

    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam
        '''
        raise NotImplementedError

    def remove_vertical_seam(self, seam: list[int]):
        '''
        Remove a vertical seam from the picture
        '''
        raise NotImplementedError

    def remove_horizontal_seam(self, seam: list[int]):
        '''
        Remove a horizontal seam from the picture
        '''
        raise NotImplementedError

class SeamError(Exception):
    pass
