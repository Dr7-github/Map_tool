import matplotlib.pyplot as plt
import matplotlib.colors as mcl

color = plt.cm.Spectral([1,2,3])
print(color)
print([y for x,y in mcl.cnames.items()])