from utils import Triple


rcs = lambda triple: Triple(r=triple.r, c=triple.c, s=triple.s)
rsc = lambda triple: Triple(r=triple.r, c=triple.s, s=triple.c)
crs = lambda triple: Triple(r=triple.c, c=triple.r, s=triple.s)
csr = lambda triple: Triple(r=triple.c, c=triple.s, s=triple.r)
src = lambda triple: Triple(r=triple.s, c=triple.r, s=triple.c)
scr = lambda triple: Triple(r=triple.s, c=triple.c, s=triple.r)

def permute_orthogonal_array_triple(orthogonal_array, permutation):
    return [permutation(triple) for triple in orthogonal_array]