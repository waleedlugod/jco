#!/usr/bin/env python3

from picture import Picture
import math

class SeamCarver(Picture):
    ## TO-DO: fill in the methods below
    
    def energy(self, i: int, j: int) -> float:
        
        energy_x = 0
        energy_y = 0
        
        if i < 0 or i >= self.width() or j < 0 or j >= self.height():
                raise IndexError
        else:
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
        # CONSTRUCT THE MEMO TABLE
        memo_tbl = [[0 for i in range(self.width())] for j in range(self.height())]		#format for accessing an element is: memo_tbl[row][col]
        for i in range(self.width()):
            memo_tbl[0][i] = self.energy(i, 0)
            
        for row in range(1, self.height()):			#row
            for col in range(self.width()):			#co1
                if col == self.width()-1:
                    memo_tbl[row][col] = self.energy(col, row) + min(memo_tbl[row-1][col-1], memo_tbl[row-1][col])
                elif col == 0:
                    memo_tbl[row][col] = self.energy(col, row) + min(memo_tbl[row-1][col], memo_tbl[row-1][col+1])
                else:
                    memo_tbl[row][col] = self.energy(col, row) + min(memo_tbl[row-1][col-1], memo_tbl[row-1][col], memo_tbl[row-1][col+1])
                
        # FIND THE VERTICAL SEAM (2 steps)
        # 1. Find the index of the minimum energy at the last row
        vseam = [-1]
        min_energy = 2**63 -1
        for i in range(self.width()):
            if memo_tbl[self.height()-1][i] < min_energy:
                min_energy = memo_tbl[self.height()-1][i]
                vseam[0] = i
                
        # 2. Trace your way up
        for j in range(self.height()-1, 0, -1):
            current_col = vseam[len(vseam)-1]
            
            if current_col == self.width()-1:
                min_energy = min(memo_tbl[j-1][current_col-1], memo_tbl[j-1][current_col])
                
                if memo_tbl[j-1][current_col-1] == min_energy:
                    vseam.append(current_col-1)
                else:
                    vseam.append(current_col)
                    
            elif current_col == 0:
                min_energy = min(memo_tbl[j-1][current_col], memo_tbl[j-1][current_col+1])
                
                if memo_tbl[j-1][current_col] == min_energy:
                    vseam.append(current_col)
                else:
                    vseam.append(current_col+1)
            
            else:
                min_energy = min(memo_tbl[j-1][current_col-1], memo_tbl[j-1][current_col], memo_tbl[j-1][current_col+1])
            
                if memo_tbl[j-1][current_col-1] == min_energy:
                    vseam.append(current_col-1)
                elif memo_tbl[j-1][current_col] == min_energy:
                    vseam.append(current_col)
                else:
                    vseam.append(current_col+1)
                
        vseam.reverse()
        return vseam

    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam
        '''
        self.flip_image()
        hseam = self.find_vertical_seam()
        self.flip_image()
        return hseam

    def remove_vertical_seam(self, seam: list[int]):
        '''
        Remove a vertical seam from the picture
        '''
        if len(seam) != self._height or self._width <= 1: raise SeamError
        # Raise error if seam differs by more than 1
        for col in range(len(seam) - 1):
            if abs(seam[col] - seam[col+1]) > 1: raise SeamError

        # shifts pixels right of seam and deletes last pixel
        for row in range(len(seam)):
            for col in range(seam[row], self._width - 1):
                self[col, row] = self[col+1, row]
            del self[self._width-1, row]
        self._width -= 1
        return

    def remove_horizontal_seam(self, seam: list[int]):
        '''
        Remove a horizontal seam from the picture
        '''
        if len(seam) != self._width or self._height <= 1: raise SeamError
        for row in range(len(seam) - 1):
            if abs(seam[row] - seam[row+1]) > 1: raise SeamError

        self.flip_image()
        self.remove_vertical_seam(seam)
        self.flip_image()
        return

    def flip_image(self):
        '''
        Flip the image
        '''
        swapped = set()
        for col in range(self._width):
            for row in range(self._height):
                if (col, row) not in swapped and (row, col) not in swapped:
                    if (col, row) not in self: self[col, row] = None
                    if (row, col) not in self: self[row, col] = None
                    self[col, row], self[row, col] = self[row, col], self[col, row]
                    if self[col, row] is None: del self[col, row]
                    if self[row, col] is None: del self[row, col]
                    swapped.add((col, row))
                    swapped.add((row, col))
        self._width, self._height = self._height, self._width
        return

class SeamError(Exception):
    pass
