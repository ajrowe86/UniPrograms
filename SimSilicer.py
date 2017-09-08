import pynbody	

sl_cen_x = 0.
sl_cen_y = 0.
slit_l = 10.
slit_h = 0.1
bin_nos = 100.
min_age = 8.
max_age = 9.
inc = 90.

i=1
j=0
k=0.5
m=1
count=1

max_l = sl_cen_x + slit_l
min_l = sl_cen_x - slit_l
max_h = sl_cen_y + slit_h
min_h = sl_cen_y - slit_h
bin_w = (max_l - min_l) / bin_nos

av_vz = []
deriv = []
sigma = []
rad = []
stars_in_bin = []

sim = pynbody.load("/home/andy/project/simulations/12M_hr.01000")
pynbody.analysis.angmom.faceon(sim.gas)
sim.rotate_x(inc)
slit = sim.star
slit = sim[(sim['x'] >= min_l) & (sim['x'] <= max_l) & (sim['y'] >= min_h) & (sim['y'] <= max_h)]
slit = slit[(slit.star['age'].in_units('Gyr') >= min_age) & (slit.star['age'].in_units('Gyr') < max_age)]

while i <= bin_nos:
    if i < bin_nos:
        bin_store = slit[(slit['x'] >= (min_l + (j * bin_w))) & (slit['x'] < ((min_l + (j + 1) * bin_w)))]
    else:
        bin_store = slit[(slit['x'] >= (min_l + (j * bin_w))) & (slit['x'] <= ((min_l + (j + 1) * bin_w)))]
    av_vz.append((sum(bin_store['vz'])) / len(bin_store))
    for l in range(0, len(bin_store), 1):
	print (len(slit) - count) #,i, (len(bin_store)-l)
        count = count + 1
        deriv.append(((bin_store['vz'][l]) - av_vz[j]) ** 2)
    sigma.append(sqrt(sum(deriv) / len(bin_store)))
    rad.append(min_l + (k * bin_w))
    stars_in_bin.append(len(bin_store))
    deriv = []
    i = i + 1
    j = j + 1
    k = k + 1

#plt.figure(1)
#pynbody.plot.image(sim.star, width = 60)

plt.figure(2)
plt.subplot(2, 1, 1)
plt.plot(rad, sigma, 'r-', label="sigma")
plt.plot(rad, av_vz, 'g-', label="av_v_z")
legend(loc=4)
plt.axis([-10, 10, -300, 300])
plt.xlabel('radius in kpc')
plt.ylabel('velocity in km/s')
plt.title('z-velocity relations for 12M_hr.01000, in age range \n %s<age<%s Gyr, containing %s stars, for i=%s degrees'%(min_age, max_age, len(slit), inc))

plt.figure(2)
plt.subplot(2,1,2)
plt.plot(rad, stars_in_bin, 'b-')
plt.axis([-10, 10, 1, 100000])
plt.yscale('log')
plt.xlabel('radius in kpc')
plt.ylabel('number of stars')
