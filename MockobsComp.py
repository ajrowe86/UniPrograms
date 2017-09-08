#################################################################

#routine that compares input 2D spectra datacube to bestfit spectra datacube from ppxf

#################################################################

#need to start python with pylab ie "ipython --pylab" before running this code. Tried "import pylab" here, but didn't work.

##################################################################

import pyfits

#set input files that are needed
infile = pyfits.getdata('/home/andy/ppxf_examples/test/in_spectra.fits')
bestfitfile = pyfits.getdata('/home/andy/ppxf_examples/test/bestfit_spectra.fits')

#set input parameters that are needed
##ln wavelength range
lambda_low = 8.54
lambda_high = 8.56

#set variables that will be called
no_of_pixels = len(infile[:])
no_of_spectra = 1
lambda_step = (lambda_high - lambda_low)/no_of_pixels
wavelength_axis = []
input_intensity = []
bestfit_intensity = []
residual_intensity = []
rms_input_deriv = 0
rms_bestfit_deriv = 0
rms_residual_deriv = 0
mean_input_intensity_deriv = 0
mean_bestfit_intensity_deriv = 0
mean_input_intensity = 0
mean_bestfit_intensity = 0

pixel_cut = 3

#say which spectrum in datacubes to use, if only one. If more need to change limits in #loop over spectral bins
#isolate_spectrum = 125

#generate wavelength scale for x axis
for i in range(0, no_of_pixels, 1):
    wavelength_axis.append(lambda_low + (i * lambda_step))

#loop over range of spectral bins
#for i in range((isolate_spectrum - 1), isolate_spectrum, 1):  #no_of_spectra - 1), 1):
    
    #generate individual spectral intensity values
input_intensity = infile[:]
bestfit_intensity = bestfitfile[:]
    
    #start deriving mean intensity values
for j in range(0, len(input_intensity), 1):
    mean_input_intensity_deriv = mean_input_intensity_deriv + input_intensity[j]
    mean_bestfit_intensity_deriv = mean_bestfit_intensity_deriv + bestfit_intensity[j]

    #finish off mean intensity calculations
mean_input_intensity = mean_input_intensity_deriv / len(input_intensity)
mean_bestfit_intensity = mean_bestfit_intensity_deriv / len(bestfit_intensity)
    
    #store values that will be plotted    
for k in range(0, no_of_pixels, 1):
    input_intensity[k] = input_intensity[k] / mean_input_intensity
    bestfit_intensity[k] = bestfit_intensity[k] / mean_bestfit_intensity
    residual_intensity.append(input_intensity[k] - bestfit_intensity[k])
    
    #start deriving rms values 
    #x_rms=sqrt((1/n) * (x_1**2 + x_2**2 + ... + x_n**2)). Loop below is (x_1**2+...+x_n**2)
for l in range(0, no_of_pixels, 1):
    rms_input_deriv = rms_input_deriv + (input_intensity[l])**2
    rms_bestfit_deriv = rms_bestfit_deriv + (bestfit_intensity[l])**2
    rms_residual_deriv = rms_residual_deriv + (residual_intensity[l])**2

    #finish off rms derivations
rms_input_deriv = sqrt(rms_input_deriv / no_of_pixels)
rms_bestfit_deriv = sqrt(rms_bestfit_deriv / no_of_pixels)
rms_residual_deriv = sqrt(rms_bestfit_deriv / no_of_pixels)

    #plot relations
fig = plt.figure()
figb = fig.add_subplot(2, 1, 2)
figb.plot(wavelength_axis[pixel_cut - 1 : no_of_pixels - 1 - pixel_cut], residual_intensity[pixel_cut - 1 : no_of_pixels - 1 - pixel_cut], 'g-', label="input-bestfit")
plt.xlabel('Ln wavelength')
plt.ylabel('intensity difference')
legend(loc=1)

figa = fig.add_subplot(2, 1, 1, sharex=figb)
    #plt.axis([8.409, 8.611, 2090000, 3780000])
    #plt.yscale('log')
plt.title('Spectrum no. %s      RMS input = %s\nRMS bestfit = %s RMS residual = %s'%(no_of_spectra, rms_input_deriv, rms_bestfit_deriv, rms_residual_deriv))
plt.ylabel('intensity / mean intensity')
plt.setp(figa.get_xticklabels(), visible=False)
figa.plot(wavelength_axis[pixel_cut - 1 : no_of_pixels - 1 - pixel_cut], input_intensity[pixel_cut - 1 : no_of_pixels - 1 - pixel_cut], 'k-', label="input")
figa.plot(wavelength_axis[pixel_cut - 1 : no_of_pixels - 1 - pixel_cut], bestfit_intensity[pixel_cut - 1 : no_of_pixels - 1 - pixel_cut], 'r-', label="bestfit")
legend(loc=1)

    #set variables to zero for next iteration
rms_input_deriv = 0
rms_bestfit_deriv = 0
rms_residual_deriv = 0
mean_input_intensity_deriv = 0
mean_bestfit_intensity_deriv = 0
mean_input_intensity = 0
mean_bestfit_intensity = 0
