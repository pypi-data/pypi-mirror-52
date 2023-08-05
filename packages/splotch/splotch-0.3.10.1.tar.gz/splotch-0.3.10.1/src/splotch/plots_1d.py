#### Definition of all wrappers for 1D plotting

# Generalized lines
def axline(x=None,y=None,m=None,c=None,plabel=None,lab_loc=0,ax=None,plot_kw={},**kwargs):
	
	"""Generalised axis lines.
	
	This function aims to generalise the usage of axis lines calls (axvline/axhline) together and to allow
	lines to be specified by a slope/intercept.
	
	Parameters
	----------
	x : int or list, optional 
		x position(s) in data coordinates for a vertical line(s).
	y : int or list, optional
		y position(s) in data coordinates for a horizontal line(s).
	m : int or list, optional
		Slope(s) of diagonal axis line(s), defaults to 1 if not specified when c is given.
	c : int or list, optional
		Intercept points(s) of diagonal axis line(s), defaults to 0 if not specified when m is given.
	plabel : str, optional
		Sets label(s) for line(s) and plots legend.
	lab_loc : int, optional
		Defines the position of the legend. Defaults as lab_loc=0.
	ax : pyplot.Axes, optional
		Use the given axes to make the plot, defaults to the current axes.
	plot_kw : dict, optional
		Passes the given dictionary as a kwarg to the plotting function. Valid kwargs are Line2D properties.
	**kwargs: Line2D properties, optional
		kwargs are used to specify matplotlib specific properties such as linecolor, linewidth, antialiasing, etc.
		A list of available `Line2D` properties can be found here: 
		https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D

	Returns
	-------
	None
	"""
	
	from matplotlib.pyplot import plot, legend, gca
	from .base_func import axes_handler,plot_finalizer,dict_splicer
	
	if ax is not None:
		old_axes=axes_handler(ax)
	else:
		ax=gca()
		old_axes=ax
	
	if (not any([x,y,m,c])): # If nothing has been specified
		raise TypeError("axline() missing one of optional arguments: 'x', 'y', 'm' or 'c'")
	
	for i, val in enumerate([x,y,m,c]):
		if (val is not None):
			try: # Test whether the parameter is iterable
				temp=(k for k in val)
			except TypeError: # If not, convert to a list
				if   (i == 0): x = [x]
				elif (i == 1): y = [y]
				elif (i == 2): m = [m]
				elif (i == 3): c = [c]
	
	if (x is not None and y is not None): # Check whether both x and y were specified
		raise ValueError("'x' and 'y' cannot be both specified")
	
	if (x is not None): # Check conditions if x specified
		if (any([m,c])): # Should not specify m or c, if x given.
			raise ValueError("'{0}' cannot be specified if x specified".format('m' if m else 'c'))
		L = len(x)
	
	if (y is not None): # Check conditions if y specified
		if (any([m,c])): # Should not specify m or c, if y given.
			raise ValueError("'{0}' cannot be specified if y specified".format('m' if m else 'c'))
		L = len(y)
	
	if (m is not None):
		if (c is None): # If no intercept specified
			c = [0]*len(m) # set c to 0 for all m
		else:
			if (len(c) == 1):
				c = [c[0]]*len(m)
			elif (len(c) != len(m)):
				if (len(m) == 1):
					m = [m[0]]*len(c)
				else:
					raise ValueError("Length of c ({0}) and length of m ({1}) must be equal or otherwise 1".format(len(c),len(m)))
		L = len(m)
	elif (c is not None):
		if (m is None): # If no slope specified
			m = [1]*len(c) # set m to 1 for all c
		L = len(c)
	
	if type(plabel) is not list:
		plabel=[plabel]*L
	elif (len(plabel) != L):
		raise ValueError("Length of plabel list ({0}) must match the number of lines given ({1}).".format(len(plabel),L))
	
	# Combine the `explicit` plot_kw dictionary with the `implicit` **kwargs dictionary
	#plot_par = {**plot_kw, **kwargs} # For Python > 3.5
	plot_par = plot_kw.copy()
	plot_par.update(kwargs)
	
	# Create 'L' number of plot kwarg dictionaries to parse into each plot call
	plot_par = dict_splicer(plot_par,L,[1]*L)
	
	if (x is not None):
		for ii, xx in enumerate(x):
			ax.axvline(x=xx,**plot_par[ii],label=plabel[ii])
	if (y is not None):
		for ii, yy in enumerate(y):
			ax.axhline(y=yy,**plot_par[ii],label=plabel[ii])
	if (m is not None):
		for ii, pars in enumerate(zip(m,c)):
			mm = pars[0]; cc = pars[1]
			
			xLims = ax.get_xlim()
			yLims = ax.get_ylim()
			
			plot([xLims[0],xLims[1]],[mm*xLims[0]+cc,mm*xLims[1]+cc],label=plabel[ii],**plot_par[ii])
			
			ax.set_xlim(xLims)
			ax.set_ylim(yLims)
			
	if any(plabel):
		legend(loc=lab_loc)
	if ax is not None:
		old_axes=axes_handler(old_axes)

#Histogram
def hist(data,bin_type=None,bins=None,dens=True,scale=None,hist_type=None,v=None,vstat=None,xlim=None,ylim=None,#count_style={},
			xinvert=False,yinvert=False,xlog=False,ylog=None,title=None,xlabel=None,ylabel=None,plabel=None,lab_loc=0,
			ax=None,grid=None,plot_kw={},output=None,**kwargs):
	
	"""1D histogram function.
	
	The plotting is done with pyplot.plot(), so histograms are shown with interpolated curves instead of the
	more common stepwise curve. For this reason splotch.histstep is a better choice for small datasets. 
	
	Parameters
	----------
	data : array-like or list
		If list it is assumed that each elemement is array-like.
	bin_type : {'number','width','edges','equal'}, optional
		Defines how is understood the value given in bins: 'number' for givinf the desired number of bins, 'width' for
		the width of the bins, 'edges' for the edges of bins, and 'equal' for making bins with equal number of elements
		(or as close as possible). If not given it is inferred from the data type of bins: 'number' if int, 'width' if
		float and 'edges' if ndarray.
	bins : int, float, array-like or list, optional
		Gives the values for the bins, according to bin_type.
	dens :  bool or list, optional
		If false the histogram returns raw counts.
	scale : float or list, optional
		Scaling the counts.
	hist_type : str, optional.
		Defines the type of histogram to be drawn. 'smooth' and 'step' produce lines, with the former drawing lines conecting
		the values of each bin positioned on their centre, and the latter drawing a stepwise line, with the edges of each step
		coinciding with the bin edges. 'bar' produces a bar plot. All have filled version (i.e., 'smoothfilled'), which fills
		the space between the edges of the histogram and 0.
	v : array-like or list, optional
		If a valid argument is given in cstat, defines the value used for the binned statistics.
	vstat : str, function  or list, optional
		Must be or contain one of the valid str arguments for the statistics variable in scipy.stats.binned_statistic
		('mean’, 'median’, 'count’, 'sum’, 'min’ or 'max’) or function(s) that takes a 1D array and outputs an integer
		 or float.
	xlim : tuple-like, optional
		Defines the limits of the x-axis, it must contain two elements (lower and higer limits).
	ylim : tuple-like, optional
	xinvert : bool or list, optional
		If true inverts the x-axis.
		Defines the limits of the y-axis, it must contain two elements (lower and higer limits).
	yinvert : bool or list, optional
		If true inverts the y-axis.
	xlog : bool or list, optional
		If True the scale of the x-axis is logarithmic.
	ylog : bool or list, optional
		If True the scale of the x-axis is logarithmic.
	title : str, optional
		Sets the title of the plot
	xlabel : str, optional
		Sets the label of the x-axis.
	ylabel : str, optional
		Sets the label of the y-axis.
	plabel : str, optional
		Sets the legend for the plot.
	lab_loc : int, optional
		Defines the position of the legend
	ax : pyplot.Axes, optional
		Use the given axes to make the plot, defaults to the current axes.
	grid : boolean, optional
		If not given defaults to the value defined in splotch.Params.
	plot_par : dict, optional
		Passes the given dictionary as a kwarg to the plotting function.
	output : boolean, optional
		If True, returns the edges and values of the histogram.
	
	Returns
	-------
	n : list
		List containing the arrays with the values for each histogram drawn. Only provided if output is True.
	bins_edges : list
		List containing the arrays with the bin edges for each of the histograms drawn. Only provided if output is True.
	"""
	
	from numpy import sum as np_sum
	from scipy.stats import binned_statistic
	from numpy import array, diff, histogram, inf, nan, ones, where
	from matplotlib.pyplot import bar, fill_between, gca, legend, plot, rcParams, step
	from .base_func import axes_handler,binned_axis,dict_splicer,plot_finalizer,step_hist_filled
	
	if ax is not None:
		old_axes=axes_handler(ax)
	if type(data) is not list:
		data=[data]
	L=len(data)
	if type(bin_type) is not list:
		bin_type=[bin_type]*L
	if type(bins) is not list:
		if bins is not None:
			bins=[bins]*L
		else:
			bins=[int((len(d))**0.4) for d in data]
	if type(dens) is not list:
		dens=[dens]*L
	if type(scale) is not list:
		scale=[scale]*L
	if type(v) is not list:
		v=[v]*L
	if type(vstat) is not list:
		vstat=[vstat]*L
	if type(plabel) is not list:
		plabel=[plabel]*L
	if None in [ylog,hist_type,output]:
		from .defaults import Params
		if ylog is None:
			ylog=Params.hist1D_yaxis_log
		if hist_type is None:
			hist_type=Params.hist1D_histtype
		if output is None:
			output=Params.hist1D_output
	if type(hist_type) is not list:
		hist_type=[hist_type]*L
	
	# Combine the `explicit` plot_kw dictionary with the `implicit` **kwargs dictionary
	#plot_par = {**plot_kw, **kwargs} # For Python > 3.5
	plot_par = plot_kw.copy()
	plot_par.update(kwargs)
	# Check if width is given as a kwarg
	if 'width' in plot_par.keys():
		import warnings
		warnings.warn('Received kwarg width, this will be ignored in the histogram',UserWarning)
		if hist_type!='bar':
			temp=plot_par.pop('width')
	# Create 'L' number of plot kwarg dictionaries to parse into each plot call
	plot_par = dict_splicer(plot_par,L,[1]*L)
	
	plot_type={'smooth':plot,'smoothfilled':fill_between,'step':step,'stepfilled':step_hist_filled,'bar':bar,'barfilled':bar}
	hist_centre={'smooth':True,'smoothfilled':True,'step':False,'stepfilled':False,'bar':False,'barfilled':False}
	bin_edges=[]
	n_return=[]
	
	for i in range(L):
		temp_data,bins_hist,bins_plot=binned_axis(data[i],bin_type[i],bins[i],log=xlog,plot_centre=hist_centre[hist_type[i]])
		if vstat[i]:
			temp_y=binned_statistic(temp_data,v[i],statistic=vstat[i],bins=bins_hist)[0]
		else:
			temp_y=histogram(temp_data,bins=bins_hist,density=dens[i])[0]
		if dens[i]:
			if scale[i]:
				temp_y*=1.0*len(data[i])/scale[i]
		if ylog:
			temp_y=where(temp_y==0,nan,temp_y)
		y=temp_y
		if hist_type[i]=='step':
			y=array([y[0]]+[j for j in y])
		if 'bar' in hist_type[i]:
			#prop_cycle=rcParams['axes.prop_cycle']
			#barcolor=prop_cycle.by_key()['color']
			plot_par[i]['width']=diff(bins_plot)
			bins_plot=(bins_plot[0:-1]+bins_plot[1:])/2
			if hist_type[i]=='bar':
				if 'edgecolor' not in plot_par[i].keys():
					p=plot(bins_plot[0],0)
					plot_par[i]['edgecolor']=p[0].get_color()
					p.pop()
					temp_ax=gca()
					temp_ax.relim()
					temp_ax.autoscale()
				plot_par[i]['fill']=False
		#if count_style:
		#	if dens[i]:
		#		raw_counts=histogram(temp_data,bins=bins_hist,density=False)[0]
		#		raw_counts=array([raw_counts[0]]+[j for j in raw_counts])
		#	else:
		#		raw_counts=y
		#	if 'low' not in count_style.keys():
		#		count_style['low']=-inf
		#	if 'high' not in count_style.keys():
		#		count_style['high']=inf
		#	sel_low=raw_counts<count_style['low']
		#	sel_high=raw_counts>count_style['high']
		#	sel_mid=ones(len(raw_counts)).astype('bool')&~sel_low&~sel_high
		#	for j in range(len(raw_counts)-1):
		#		if not sel_low[j] and sel_low[j+1]:
		#			sel_low[j]=True
		#		if not sel_high[j] and sel_high[j+1]:
		#			sel_high[j]=True
		#	for j in range(1,len(raw_counts))[::-1]:
		#		if not sel_low[j] and sel_low[j-1]:
		#			sel_low[j]=True
		#		if not sel_high[j] and sel_high[j-1]:
		#			sel_high[j]=True
		#	if 'low_style' not in count_style.keys() and 'high_style' not in count_style.keys():
		#		plot_par[i]['linestyle']='solid'
		#	if 'low_style' not in count_style.keys():
		#		count_style['low_style']='dotted'
		#	if 'high_style' not in count_style.keys():
		#		count_style['high_style']='dashed'
		#	low_plot_par={k:plot_par[i][k] for k in plot_par[i].keys()}
		#	low_plot_par['linestyle']=count_style['low_style']
		#	high_plot_par={k:plot_par[i][k] for k in plot_par[i].keys()}
		#	high_plot_par['linestyle']=count_style['high_style']
		#	col=None
		#	if np_sum(sel_low)>0:
		#		low_plabel='n<'+str(count_style['low'])
		#		if plabel[i] is not None:
		#			low_plabel=plabel[i]+', '+low_plabel
		#		p=plot_type[hist_type[i]](bins_plot,where(sel_low,y,nan),label=low_plabel,**low_plot_par)
		#		col=p[0].get_color()
		#	if np_sum(sel_high)>0:
		#		high_plabel='n>'+str(count_style['high'])
		#		if plabel[i] is not None:
		#			high_plabel=plabel[i]+', '+high_plabel
		#		if col is None:
		#			p=plot_type[hist_type[i]](bins_plot,where(sel_high,y,nan),label=high_plabel,**high_plot_par)
		#			col=p[0].get_color()
		#		else:
		#			high_plot_par['color']=col
		#			plot_type[hist_type[i]](bins_plot,where(sel_high,y,nan),label=high_plabel,**high_plot_par)
		#	if np_sum(sel_mid)>0:
		#		if col is not None:
		#			plot_par[i]['color']=col
		#		plot_type[hist_type[i]](bins_plot,where(sel_mid,y,nan),label=plabel[i],**plot_par[i])
		#else:
		plot_type[hist_type[i]](bins_plot,y,label=plabel[i],**plot_par[i])
		bin_edges.append(bins_plot)
		n_return.append(temp_y)
	if any(plabel):
		legend(loc=lab_loc)
	plot_finalizer(xlog,ylog,xlim,ylim,title,xlabel,ylabel,xinvert,yinvert,grid)
	if ax is not None:
		old_axes=axes_handler(old_axes)
	if output:
		return(n_return,bin_edges)

#Step histogram
def histstep(data,bin_num=None,dens=True,xlim=None,ylim=None,xinvert=False,yinvert=False,xlog=False,ylog=True,
			title=None,xlabel=None,ylabel=None,plabel=None,lab_loc=0,ax=None,grid=None,plot_kw={}):
	
	"""'Clasic' 1D histogram function.
	
	This function is designed around pyplot.hist(), so it lacks the functionality to use arbitraty y-axis
	normalisation of splotch.hist().
	It is better choice for small datasets, as it plots with stepwise curves, instead of the interpolated
	ones of splotch.hist().
	
	Parameters
	----------
	data : array-like or list
		If list it is assumed that each elemement is array-like.
	bin_num : int or list, optional
		Number of bins.
	dens :  bool or list, optional
		If false the histogram returns raw counts.
	xlim : tuple-like, optional
		Defines the limits of the x-axis, it must contain two elements (lower and higer limits).
	ylim : tuple-like, optional
		Defines the limits of the y-axis, it must contain two elements (lower and higer limits).
	xinvert : bool or list, optional
		If true inverts the x-axis.
	yinvert : bool or list, optional
		If true inverts the y-axis.
	xlog : bool or list, optional
		If True the scale of the x-axis is logarithmic.
	ylog : bool or list, optional
		If True the scale of the x-axis is logarithmic.
	title : str, optional
		Sets the title of the plot
	xlabel : str, optional
		Sets the label of the x-axis.
	ylabel : str, optional
		Sets the label of the y-axis.
	plabel : str, optional
		Sets the legend for the plot.
	lab_loc : int, optional
		Defines the position of the legend
	ax : pyplot.Axes, optional
		Use the given axes to make the plot, defaults to the current axes.
	grid : boolean, optional
		If not given defaults to the value defined in splotch.Params.
	plot_par : dict, optional
		Passes the given dictionary as a kwarg to the plotting function.
	
	Returns
	-------
	None
	"""
	
	from matplotlib.pyplot import hist, legend
	from .base_func import axes_handler,dict_splicer,plot_finalizer
	
	if ax is not None:
		old_axes=axes_handler(ax)
	if type(data) is not list:
		data=[data]
	L=len(data)
	if bin_num is None:
		bin_num=[int((len(d))**0.4) for d in data]
	if type(bin_num) is not list:
		bin_num=[bin_num+1]*L
	if type(plabel) is not list:
		plabel=[plabel]*L
	plot_par=dict_splicer(plot_kw,L,[len(x) for x in data])
	for i in range(L):
		temp_data,bins,temp=binned_axis(data[i],bin_num[i],log=xlog)
		hist(temp_data,bins=bins,density=dens,label=plabel[i],**plot_par[i])
	if any(plabel):
		legend(loc=lab_loc)
	plot_finalizer(xlog,ylog,xlim,ylim,title,xlabel,ylabel,xinvert,yinvert,grid)
	if ax is not None:
		old_axes=axes_handler(old_axes)

#Plots
def plot(x,y=None,xlim=None,ylim=None,xinvert=False,yinvert=False,xlog=False,ylog=False,title=None,xlabel=None,
			ylabel=None,plabel=None,lab_loc=0,ax=None,grid=None,plot_kw={},**kwargs):
	
	"""Base plotting function.
	
	This is a wrapper for pyplot.plot().
	
	Parameters
	----------
	x : array-like or list
		If list it is assumed that each elemement is array-like. If y is not given, the given values pass to y and a
		numpy array is generated with numpy.arange() for the x values.
	y : array-like or list, optional
		If list it is assumed that each elemement is array-like.
	xlim : tuple-like, optional
		Defines the limits of the x-axis, it must contain two elements (lower and higer limits).
	ylim : tuple-like, optional
		Defines the limits of the y-axis, it must contain two elements (lower and higer limits).
	xinvert : bool or list, optional
		If true inverts the x-axis.
	yinvert : bool or list, optional
		If true inverts the y-axis.
	xlog : bool or list, optional
		If True the scale of the x-axis is logarithmic.
	ylog : bool or list, optional
		If True the scale of the x-axis is logarithmic.
	title : str, optional
		Sets the title of the plot
	xlabel : str, optional
		Sets the label of the x-axis.
	ylabel : str, optional
		Sets the label of the y-axis.
	plabel : str, optional
		Sets the legend for the plot.
	lab_loc : int, optional
		Defines the position of the legend
	ax : pyplot.Axes, optional
		Use the given axes to make the plot, defaults to the current axes.
	grid : boolean, optional
		If not given defaults to the value defined in splotch.Params.
	plot_kw : dict, optional
		Passes the given dictionary as a kwarg to the plotting function. Valid kwargs are Line2D properties.
	**kwargs: Line2D properties, optional
		kwargs are used to specify matplotlib specific properties such as linecolor, linewidth, antialiasing, etc.
		A list of available `Line2D` properties can be found here: 
		https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D
	
	Returns
	-------
	None
	"""

	from numpy import shape, arange
	from matplotlib.pyplot import plot, legend
	from .base_func import axes_handler,dict_splicer,plot_finalizer
	

	if ax is not None:
		old_axes=axes_handler(ax)
	if type(x) is not list or len(shape(x))==1:
		x=[x]
	L=len(x)
	if y is None:
		y=x
		x=[arange(len(x[i])) for i in range(L)]
	else:
		if type(y) is not list or len(shape(y))==1:
			y=[y]
	if type(plabel) is not list:
		plabel=[plabel]*L
	
	# Combine the `explicit` plot_kw dictionary with the `implicit` **kwargs dictionary
	#plot_par = {**plot_kw, **kwargs} # For Python > 3.5
	plot_par = plot_kw.copy()
	plot_par.update(kwargs)

	# Create 'L' number of plot kwarg dictionaries to parse into each plot call
	plot_par = dict_splicer(plot_par,L,[1]*L)

	for i in range(L):
		plot(x[i],y[i],label=plabel[i],**plot_par[i])
	if any(plabel):
		legend(loc=lab_loc)
	plot_finalizer(xlog,ylog,xlim,ylim,title,xlabel,ylabel,xinvert,yinvert,grid)
	if ax is not None:
		old_axes=axes_handler(old_axes)


### Broken axis plot
def brokenplot(x,y=None,xbreak=None,ybreak=None,xlim=None,ylim=None,sep=0.05,xinvert=False,yinvert=False,xlog=False,ylog=False,title=None,xlabel=None,
			   ylabel=None,plabel=None,lab_loc=0,ax=None,grid=None,plot_kw={},**kwargs):

	""" Broken Axis Plot Function
	
	Creates a standard plot call with an axis break at `xbreak` or `ybreak` for vertical or horizontal breaks.
	
	Parameters
	----------
	x : array-like or list
		If list it is assumed that each elemement is array-like. If y is not given, the given values pass to y and a
		numpy array is generated with numpy.arange() for the x values.
	y : array-like or list, optional
		If list it is assumed that each elemement is array-like.
	xbreak/ybreak : float or tuple-like, required
		The location(s) of the vertical or horizontal breaks is controlled by xbreak or ybreak, respectively.
		The value can be a single location or a tuple defining the (start, stop) points of the break. Only one 
		coordinate can be broken in a given plot.
	xlim : tuple-like, optional
		Defines the limits of the x-axis, it must contain two elements (lower and higer limits).
	ylim : tuple-like, optional
		Defines the limits of the y-axis, it must contain two elements (lower and higer limits).
	sep : float, optional, default: 0.05
		The separation size of the axis break, given as a fraction of the axis dimensions.
	xinvert : bool or list, optional
		If true inverts the x-axis.
	yinvert : bool or list, optional
		If true inverts the y-axis.
	xlog : bool or list, optional
		If True the scale of the x-axis is logarithmic.
	ylog : bool or list, optional
		If True the scale of the x-axis is logarithmic.
	title : str, optional
		Sets the title of the plot
	xlabel : str, optional
		Sets the label of the x-axis.
	ylabel : str, optional
		Sets the label of the y-axis.
	plabel : str, optional
		Sets the legend for the plot.
	lab_loc : int, optional
		Defines the position of the legend
	ax : pyplot.Axes, optional
		Use the given axes to make the plot, defaults to the current axes.
	grid : boolean, optional
		If not given defaults to the value defined in splotch.Params.
	plot_kw : dict, optional
		Passes the given dictionary as a kwarg to the plotting function. Valid kwargs are Line2D properties.
	**kwargs: Line2D properties, optional
		kwargs are used to specify matplotlib specific properties such as linecolor, linewidth, antialiasing, etc.
		A list of available `Line2D` properties can be found here: 
		https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D
	
	Returns
	-------
	None

	"""
	from .base_func import axes_handler,dict_splicer,plot_finalizer
	
	from numpy import shape, arange, ndarray
	from matplotlib.pyplot import plot, legend, show, sca
	from matplotlib.transforms import Bbox
	

	if ax is not None:
		old_axes=axes_handler(ax)
	if type(x) is not list or len(shape(x))==1:
		x=[x]
	L=len(x)
	if y is None:
		y=x
		x=[arange(len(x[i])) for i in range(L)]
	else:
		if type(y) is not list or len(shape(y))==1:
			y=[y]
	if type(plabel) is not list:
		plabel=[plabel]*L

	if type(xbreak) not in [list,tuple,ndarray]:
		xbreak = (xbreak, xbreak)
	else:
		if (len(xbreak) != 2):
			raise ValueError("xbreak must be a single value of a tuple-like list of two elements.")

	if (ybreak != None):
		raise NotImplementedError("ybreak not yet implemented.")

	# Combine the `explicit` plot_kw dictionary with the `implicit` **kwargs dictionary
	#plot_par = {**plot_kw, **kwargs} # For Python > 3.5
	plot_par = plot_kw.copy()
	plot_par.update(kwargs)

	# Create 'L' number of plot kwarg dictionaries to parse into each plot call
	plot_par = dict_splicer(plot_par,L,[1]*L)

	# Get the original axis position
	pos0 = ax.get_position(original=True)
	width0, height0 = pos0.x1 - pos0.x0, pos0.y1 - pos0.y0

	for i in range(L):
		ax.plot(x[i],y[i],label=plabel[i],**plot_par[i])
		
		# Get the axis limits if not already specified
		xlims = ax.get_xlim() if xlim == None else xlim
		ylims = ax.get_ylim() if ylim == None else ylim

		# Define the positions of the two separated axes
		if (i == 0):
			pos1 = Bbox(list(pos0.get_points()))
			pos1.x1 = pos1.x0 + (pos1.x1-pos1.x0)*(sum(xbreak)/2-xlims[0])/(xlims[1]-xlims[0]) - sep*(pos1.x1-pos1.x0)/2

			pos2 = Bbox(list(pos0.get_points()))
			pos2.x0 = pos2.x0 + (pos2.x1-pos2.x0)*(sum(xbreak)/2-xlims[0])/(xlims[1]-xlims[0]) + sep*(pos2.x1-pos2.x0)/2

			ax.set_position(pos1) # Resize the first axis
			ax2 = ax.figure.add_axes(pos2) # Add and duplicate the plotting in the second axis

			# Set the new axis limits at the break point
			ax.set_xlim(xlims[0],xbreak[0])
			ax2.set_xlim(xbreak[1],xlims[1])

		ax2.plot(x[i],y[i],label=None,**plot_par[i])


		width1, height1 = pos1.x1 - pos1.x0, pos1.y1 - pos1.y0
		width2, height2 = pos2.x1 - pos2.x0, pos2.y1 - pos2.y0

		dx1, dy1 = 0.01 * width0/(width0-width1-sep/2), height1*0.025
		
		dash_kw = dict(transform=ax2.transAxes, color='black', linestyle='-', marker='', clip_on=False)
		ax2.plot((0 - dx1, 0 + dx1), (0 - dy1, 0 + dy1), **dash_kw)  # bottom-right diagonal
		ax2.plot((0 - dx1, 0 + dx1), (1 - dy1, 1 + dy1), **dash_kw)  # top-right diagonal

		dx2, dy2 = 0.01 * width0/(width0-width2-sep/2), height2*0.025
		dash_kw.update(transform=ax.transAxes)  # switch to the left axes
		ax.plot((1 - dx2, 1 + dx2), (0 - dy2, 0 + dy2), **dash_kw)  # bottom-left sep/5iagonal
		ax.plot((1 - dx2, 1 + dx2), (1 - dy2, 1 + dy2), **dash_kw)  # top-left sep/5iagonal

		ax.spines['right'].set_visible(False)
		ax.tick_params(labelright=False,which='both')  # don't put tick labels at the top
		ax.yaxis.tick_left()

		ax2.spines['left'].set_visible(False)
		ax2.tick_params(labelleft=False,which='both')  # don't put tick labels at the top
		ax2.yaxis.tick_right()


	sca(ax)

	if any(plabel):
		ax.legend(loc=lab_loc)

	plot_finalizer(xlog,ylog,xlim,ylim,title,xlabel,ylabel,xinvert,yinvert,grid)
	
	if ax is not None:
		old_axes=axes_handler(old_axes)


def curve(expr, var=None, subs=None, lims=None, num=101, log=False, ax=None, plot_kw={}, **kwargs):
    """ Function Plotting
    
    Plot the curve corresponding to a defined function over the range of [from, to].
    
    Parameters
    ----------
    expr : str or sympy expression
        An expression parsed either as a string or as a sympy expression which will be
        evaluated by the function in the range of `lims`.
    var : str or sympy symbol, default: 'x'
        The independent variable on which to evaluate the expression (i.e. the variable
        on the x-axis). This defaults to the first non-numeric element of the expression
        or otherwise simply assumes this to be 'x'.
    subs : dict, optional
        If `expr` contains more symbols than the independent variable `var`, this dictionary
        will substitute numerical values for all additonal symbols given. `subs` is required
        if additional symbols are specified.
    lims : float, optional
        The range over which the function will be plotted. If not given, these default to
        the current bounds of the plot.
    num : int, optional (default: 101)
        The number of values along the independent variable on which to evaulate `expr`.
    ax : pyplot.Axes, optional
        Use the given axes to make the plot, defaults to the current axes.
    plot_kw : dict, optional
        Passes the given dictionary as a kwarg to the plotting function. Valid kwargs are
        Line2D properties. It is recommended that kwargs be parsed implicitly through **kwargs
        for readability.
    **kwargs: Line2D properties, optional
        kwargs are used to specify matplotlib specific properties such as linecolor, linewidth, 
        antialiasing, etc. A list of available `Line2D` properties can be found here: 
        https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D

    """
    
    from sympy import symbols, sympify, Expr
    from numpy import linspace, logspace, log10
    
    from matplotlib.pyplot import plot, legend, gca
    from .base_func import axes_handler,dict_splicer,plot_finalizer
    
    if ax is not None:
        old_axes=axes_handler(ax)
    else:
        ax=gca()
        old_axes=ax
    
    if (type(expr) == str):
        expr = sympify(expr)
    elif (isinstance(expr, Expr)):
        pass
    else:
        raise TypeError(f"`expr` must be of type `str` or sympy.Expr, instead got {type(expr)}.")
    
    symbs = expr.free_symbols # Get the symbols in the expression
    symbkeys = [str(sym) for sym in symbs]
    
    if (var != None): # Validate the independent variable
        if (var not in symbkeys):
            raise ValueError(f"Independent variable '{var}' was not found in 'expr'.")
    else: # Assume independent variable is 'x', otherwise, assume the first symbol.
        var = 'x' if 'x' in symbkeys or len(symbkeys)==0 else symbkeys[0]
    
    
    if (subs != None):
        if (var in list(subs)):
            raise ValueError(f"Independent variable '{var}' should not be in subs.")
        for key in list(subs):
            if (key not in symbkeys):
                raise KeyError(f"Substitution variable '{key}' does not exist in 'expr'.")
    
    
    # Combine the `explicit` plot_kw dictionary with the `implicit` **kwargs dictionary
    #plot_par = {**plot_kw, **kwargs} # For Python > 3.5
    plot_par = plot_kw.copy()
    plot_par.update(kwargs)
    
    
    if (lims == None):
        if ('xlim' in list(plot_par)):
            lims = plot_par['xlim']
        else:
            lims = ax.get_xlim()
            
    vararr = logspace(*log10(lims),num=num) if log else linspace(*lims,num=num)
    
    curvearr = np.empty(shape=num)
    for ii, val in enumerate(vararr):
        subs[var] = val
        curvearr[ii] = expr.evalf(subs=subs)

    plot(vararr,curvearr,**kwargs)
    
    if ax is not None:
        old_axes=axes_handler(old_axes)
    
    return (expr)


def sector(r,theta,rlim=(0.0,1.0),thetalim=(0.0,360.0),rotate=0.0,
				rlabel="",thetalabel="",rstep=None,thetastep=15.0,rticks='auto',thetaticks='auto',
				fig=None,plot_kw={},**kwargs):
	
	""" Sector Plot function

	Plots a sector plot (a.k.a "pizza plot") based on data with one radial axis and an angular axis

	Parameters
	----------
	r : array-like or list
		Radial axis data.
	theta : array-like or list
		Angular axis data (degrees).
	rlim : tuple-like, optional
		The lower and upper limits for the radial axis (degrees).
	thetalim : tuple-like, optional
		The lower and upper limits for the angular axis (degrees).
	rotate : float, optional
		By how many degrees to rotate the entire plot (valid values in [-180, 180]).
	rlabel : str, optional
		Sets the label of the r-axis.
	thetalabel : str, optional
		Sets the label of the theta-axis.
	rstep : float, optional
		Sets the step size of r ticks.
	thetastep : float, optional, default: 15.0
		Sets the step size of theta ticks (degrees).
	rticks : 'auto', or ticker
		* Not implement *
	thetaticks : 'auto', or ticker
		* Not implement *
	fig : pyplot.Figure, optional
		Use the given figure to make the plot, defaults to the current figure.
	plot_kw : dict, optional
		Explicit dictionary of kwargs to be parsed to matplotlib scatter function.
		Parameters will be overwritten if also given implicitly in **kwargs.
	**kwargs : Collection properties, optional
		kwargs are used to specify matplotlib specific properties such as cmap, marker, norm, etc.
		A list of available `Collection` properties can be found here:
		https://matplotlib.org/3.1.0/api/collections_api.html#matplotlib.collections.Collection

	Returns
	-------
	ax : The pyplot.Axes object created for the sector plot.

	"""
	
	from matplotlib.transforms import Affine2D
	from matplotlib.projections.polar import PolarAxes
	from matplotlib.pyplot import gcf 
	
	from mpl_toolkits.axisartist import floating_axes
	from mpl_toolkits.axisartist.grid_finder import (FixedLocator, MaxNLocator, DictFormatter)
	import mpl_toolkits.axisartist.angle_helper as angle_helper
	

	from numpy import array, linspace, arange, shape, sqrt, floor, round, degrees, radians, pi

	if (fig == None):
		fig = gcf()
	
	# rotate a bit for better orientation
	trans_rotate = Affine2D().translate(0.0, 0)

	# scale degree to radians
	trans_scale = Affine2D().scale(pi/180.0, 1.)
	trans = trans_rotate + trans_scale + PolarAxes.PolarTransform()
	
	# Get theta ticks
	#if (thetaticks == 'auto'):
	thetaticks = arange(*radians(array(thetalim)+rotate),step=radians(thetastep))
	theta_gridloc = FixedLocator(thetaticks[thetaticks/(2*pi) < 1])
	theta_tickfmtr = DictFormatter(dict(zip(thetaticks,[f"{(round(degrees(tck)-rotate)):g}" for tck in thetaticks])))

	#tick_fmtr = DictFormatter(dict(angle_ticks))
	#tick_fmtr = angle_helper.Formatter()

	if (rstep == None):
		rstep = 0.5
	
	r_gridloc = FixedLocator(arange(rlim[0],rlim[1],step=rstep))
	
	grid = floating_axes.GridHelperCurveLinear(
		PolarAxes.PolarTransform(),
		extremes=(*radians(array(thetalim)+rotate), *rlim),
		grid_locator1=theta_gridloc,
		grid_locator2=r_gridloc,
		tick_formatter1=theta_tickfmtr,
		tick_formatter2=None,
	)
	
	ax = floating_axes.FloatingSubplot(fig, 111, grid_helper=grid)
	fig.add_subplot(ax)
	
	# tick
	thetadir_ref = ['top','left','bottom','right']
	rdir_ref = ['bottom','right','top','left']
	
	# adjust axis
	ax.axis["left"].set_axis_direction(rdir_ref[(int(rotate)//90)%4])
	ax.axis["right"].set_axis_direction(rdir_ref[(int(rotate)//90+2)%4])
	ax.axis["bottom"].set_axis_direction(thetadir_ref[(int(rotate)//90)%4])
	ax.axis["top"].set_axis_direction(thetadir_ref[(int(rotate)//90+2)%4])
	
	ax.axis["bottom"].set_visible(False if rlim[0] < (rlim[1]-rlim[0])/3 else True)
	ax.axis["bottom"].major_ticklabels.set_axis_direction(thetadir_ref[(int(rotate)//90 + 2)%4])
	
	ax.axis["top"].toggle(ticklabels=True, label=True)
	ax.axis["top"].major_ticklabels.set_axis_direction(thetadir_ref[(int(rotate)//90)%4])
	ax.axis["top"].label.set_axis_direction(thetadir_ref[(int(rotate)//90)%4])
	
	#ax.get_yaxis().set_major_locator(ticker.MaxNLocator())
	
	#ax.axis["left"].set_major_formatter(ticker.MaxNLocator())
	ax.axis["left"].major_ticklabels.set_axis_direction(rdir_ref[(int(rotate)//90)%4])
	ax.axis["left"].label.set_axis_direction(rdir_ref[(int(rotate)//90)%4])
	
	ax.axis["left"].label.set_text(rlabel)
	ax.axis["top"].label.set_text(thetalabel)
	
	# create a parasite axes whose transData in RA, cz
	sector_ax = ax.get_aux_axes(trans)
	
	# This has a side effect that the patch is drawn twice, and possibly over some other
	# artists. So, we decrease the zorder a bit to prevent this. 
	sector_ax.patch = ax.patch  
	sector_ax.patch.zorder = 0.9
	
	
	L = shape(theta)[0] if len(shape(theta)) > 1 else 1
	plot_par = plot_kw.copy()
	plot_par.update(kwargs)
	
	# Create 'L' number of plot kwarg dictionaries to parse into each plot call
	#plot_par = dict_splicer(plot_par,L,[1]*L)
	
	if (L == 1):
		sector_ax.scatter(theta+rotate, r, **plot_par)
	else:
		for ii in range(L):
			sector_ax.scatter(theta[ii]+rotate, r[ii],**plot_par[ii])

	return sector_ax
