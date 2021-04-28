def lev(typo, bener):
    typo = "#" + typo
    bener = "#" + bener
    matriks = [[0 for i in range(len(bener))]for j in range(len(typo))]
    for i in range(len(typo)):
        for j in range(len(bener)):
            if(min(i,j) == 0):
                matriks[i][j] = max(i,j)
            else:
                a = matriks[i-1][j] + 1
                b = matriks[i][j-1] + 1
                c = matriks[i-1][j-1]
                if(typo[i] != bener[j]):
                    c+=1
                matriks[i][j] = min(a,b,c)
    return matriks[len(typo)-1][len(bener)-1]