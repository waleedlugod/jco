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
                if i == self.width()-1:
                    memo_tbl[row][col] = self.energy(col, row) + min(memo_tbl[row-1][col-1], memo_tbl[row-1][col])
                elif i == 0:
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
                
        raise NotImplementedError
    

    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam
        '''
        
        # CONSTRUCT A (REVERSED) MEMO TABLE
        memo_tbl = [[0 for j in range(self.height())] for i in range(self.width())]		#format is memo_tbl[col][row]
        for i in range(self.height()):
            memo_tbl[0][i] = self.energy(0, i)
            
        for j in range(1, self.width()):
            for i in range(self.height()):
                if i == self.height()-1:
                    memo_tbl[j][i] = self.energy(j, i) + min(memo_tbl[j-1][i-1], memo_tbl[j-1][i])
                elif i == 0:
                    memo_tbl[j][i] = self.energy(j, i) + min(memo_tbl[j-1][i], memo_tbl[j-1][i+1])
                else:
                    memo_tbl[j][i] = self.energy(j, i) + min(memo_tbl[j-1][i-1], memo_tbl[j-1][i], memo_tbl[j-1][i+1])
                
        # FIND THE HORIZONTAL SEAM
        # First find the index of the minimum energy at the last row
        hseam = [-1]
        min_energy = 2**63 -1
        for i in range(self.height()):
            if memo_tbl[self.width()-1][i] < min_energy:
                min_energy = memo_tbl[self.width()-1][i]
                hseam[0] = i
                
        # Then trace your way up
        for j in range(self.width()-2, -1, -1):
            current_row = hseam[len(hseam)-1]
            
            if current_row == self.height()-1:
                min_energy = min(memo_tbl[j][current_row-1], memo_tbl[j][current_row])
                
                if memo_tbl[j][current_row-1] == min_energy:
                    hseam.append(current_row-1)
                else:
                    hseam.append(current_row)
                    
            elif current_row == 0:
                min_energy = min(memo_tbl[j][current_row], memo_tbl[j][current_row+1])
                
                if memo_tbl[j][current_row] == min_energy:
                    hseam.append(current_row)
                else:
                    hseam.append(current_row+1)
            
            else:
                min_energy = min(memo_tbl[j][current_row-1], memo_tbl[j][current_row], memo_tbl[j][current_row+1])
            
                if memo_tbl[j][current_row-1] == min_energy:
                    hseam.append(current_row-1)
                elif memo_tbl[j][current_row] == min_energy:
                    hseam.append(current_row)
                else:
                    hseam.append(current_row+1)
                
        hseam.reverse()
        return hseam
        
        
        
        
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
