import xarray as xr
from scipy import stats
def st(a,b):
    slope, intercept, r_value, p_value, std_err = stats.linregress(a,b)
    return slope
def st_p(a,b):
    slope, intercept, r_value, p_value, std_err = stats.linregress(a,b)
    return p_value
def regression_vec(obj,obj2, dim):
    # note: apply always moves core dimensions to the end
    return [xr.apply_ufunc(
        st, obj,obj2, input_core_dims= [ [dim],[dim] ],
        output_core_dims=[[]],vectorize=True),
    xr.apply_ufunc(
        st_p, obj,obj2, input_core_dims= [ [dim],[dim] ],
        output_core_dims=[[]],vectorize=True)]
def t_idxr(dat):
    return [str(dat.compute().time.dt.year[0].data),
            str(dat.compute().compute().time.dt.year[-1].data)]
