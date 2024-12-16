import math

def entropy(p):
    tmp = 0
    for i in p.values():
        tmp -= i * math.log2(i)
    return tmp

def main():
    n = 6
    sum_d = {} # распределение вероятностей для суммы
    prod_d = {} # pаспределение вероятностей для произведения
    both_d = {} # совместное распределение вероятностей

    for i in range(1, n+1):
        for j in range(1, n+1):
            sum_d[i + j] = 0
            prod_d[i * j] = 0
            both_d[(i + j, i * j)] = 0

    for i in range(1, n+1):
        for j in range(1, n+1):
            sum_d[i + j] += 1
            prod_d[i * j] += 1
            both_d[(i + j, i * j)] += 1

    sum_d = {k: i / n**2 for k, i in sum_d.items()}
    prod_d = {k: i / n**2 for k, i in prod_d.items()}
    both_d = {k: i / n**2 for k, i in both_d.items()}

    H_A = entropy(sum_d) # энтропия события А
    H_B = entropy(prod_d) # энтропия события B
    H_AB = entropy(both_d) # энтропия двух связанных (совместных) событий

    HaB = H_AB - H_A #  условная энтропия события B связанного с событием A
    I_AB = H_B - HaB #  информация в событии A о событии B

    return [round(value, 2) for value in [H_AB, H_A, H_B, HaB, I_AB]]

if __name__ == "__main__":
    print(main())