"""
This is starter code to demonstrate a working example of a Spin Echo on PyPulseq.
Author: Keerthi Sravan Ravi
Date: June 13, 2017.
"""
from math import pi

from pypulseq.Sequence.sequence import Sequence
from pypulseq.calc_duration import calc_duration
from pypulseq.make_adc import make_adc
from pypulseq.make_delay import make_delay
from pypulseq.make_sinc_pulse import make_sinc_pulse
from pypulseq.make_trap_pulse import make_trapezoid
from pypulseq.opts import Opts

kwargs_for_opts = {"max_grad": 33, "grad_unit": "mT/m", "max_slew": 100, "slew_unit": "T/m/s", "rf_dead_time": 10e-6,
                   "adc_dead_time": 10e-6}
system = Opts(kwargs_for_opts)
seq = Sequence(system)

fov = 256e-3
Nx = 256
Ny = 256
slice_thickness = 5e-3

flip = 90 * pi / 180
kwargs_for_sinc = {"flip_angle": flip, "system": system, "duration": 2e-3, "slice_thickness": slice_thickness,
                   "apodization": 0.5, "time_bw_product": 4}
rf, gz = make_sinc_pulse(kwargs_for_sinc, 2)
# plt.plot(rf.t[0], rf.signal[0])
# plt.show()

delta_k = 1 / fov
kWidth = Nx * delta_k
readoutTime = system.grad_raster_time * Nx
kwargs_for_gx = {"channel": 'x', "system": system, "flat_area": kWidth, "flat_time": readoutTime}
gx = make_trapezoid(kwargs_for_gx)
kwargs_for_adc = {"num_samples": Nx, "system": system, "duration": gx.flat_time, "delay": gx.rise_time}
adc = make_adc(kwargs_for_adc)

kwargs_for_gxpre = {"channel": 'x', "system": system, "area": gx.area / 2, "duration": readoutTime / 2}
gx_pre = make_trapezoid(kwargs_for_gxpre)
kwargs_for_gz_reph = {"channel": 'z', "system": system, "area": -gz.area / 2, "duration": 2e-3}
gz_reph = make_trapezoid(kwargs_for_gz_reph)

flip = 180 * pi / 180
kwargs_for_sinc = {"flip_angle": flip, "system": system, "duration": 2e-3, "slice_thickness": slice_thickness,
                   "apodization": 0.5, "time_bw_product": 4}
rf180, gz180 = make_sinc_pulse(kwargs_for_sinc, 2)

TE, TR = 100e-3, 4408e-3
delayTE1 = TE / 2 - calc_duration(gz_reph) - calc_duration(rf) - calc_duration(rf180) / 2
delayTE2 = TE / 2 - calc_duration(gx) / 2 - calc_duration(rf180) / 2
delayTE3 = TR - TE - calc_duration(gx)
delay1 = make_delay(delayTE1)
delay2 = make_delay(delayTE2)
delay3 = make_delay(delayTE3)

for i in range(2):
    seq.add_block(rf, gz)
    kwargs_for_gy_pre = {"channel": 'y', "system": system, "area": -(Ny / 2 - i) * delta_k, "duration": readoutTime / 2}
    gy_pre = make_trapezoid(kwargs_for_gy_pre)
    seq.add_block(gx_pre, gy_pre, gz_reph)
    seq.add_block(delay1)
    seq.add_block(rf180, gz180)
    seq.add_block(delay2)
    seq.add_block(gx, adc)
    seq.add_block(delay3)

# Display 2 TR
seq.plot(time_range=(0, 2 * TR))

# Display entire plot
# seq.plot()

# The .seq file will be available inside the /gpi/<user>/imr_framework folder
seq.write("se_python.seq")
