import galois
from galois import Poly

# 36893488147419103183
def polynom_for_secret(max_degree, prim_number, secret):
    assert secret < prim_number
    coefs_of_poly = galois.Poly.Random(max_degree, galois.GF(prim_number)).coeffs
    coefs_of_poly[len(coefs_of_poly) - 1] = secret
    return Poly(coefs_of_poly)
    # galois_field = galois.GF(prim_number)
    # random_poly = galois.Poly.Random(7, galois_field)s


# for index in range(30):
# print(random_polynomial_in_field(4, 7))

# poly = polynom_for_secret(4, 7, 5)
# print(poly)
# print(poly.coeffs)

# a = poly([1, 6])
# print(a)
# b = poly([2, 3])
# print(b)

# for value in b:
#    print(f"i am one of b: {value}")

# c = a + b
# print(c)
# print(b.max())
# print(b)
# print(a + b)
