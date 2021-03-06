def bvpset(varargin):
# BVPSET  Create/alter BVP OPTIONS structure.
#    OPTIONS = BVPSET('NAME1',VALUE1,'NAME2',VALUE2,...) creates an integrator
#    options structure OPTIONS in which the named properties have the
#    specified values. Any unspecified properties have default values. It is 
#    sufficient to type only the leading characters that uniquely identify the
#    property. Case is ignored for property names. 
#    
#    OPTIONS = BVPSET(OLDOPTS,'NAME1',VALUE1,...) alters an existing options
#    structure OLDOPTS. 
#    
#    OPTIONS = BVPSET(OLDOPTS,NEWOPTS) combines an existing options structure
#    OLDOPTS with a new options structure NEWOPTS. Any new properties overwrite 
#    corresponding old properties. 
#    
#    BVPSET with no input arguments displays all property names and their
#    possible values. 
#    
# BVPSET PROPERTIES
#    
# RelTol - Relative tolerance for the residual [ positive scalar {1e-3} ]
#    This scalar applies to all components of the residual vector, and
#    defaults to 1e-3 (0.1% accuracy). The computed solution S(x) is the exact
#    solution of S'(x) = F(x,S(x)) + res(x). On each subinterval of the mesh,
#    component i of the residual satisfies  
#           norm( res(i) / max( [abs(F(i)) , AbsTol(i)/RelTol] ) ) <= RelTol.
#
# AbsTol - Absolute tolerance for the residual [ positive scalar or vector {1e-6} ]
#    A scalar tolerance applies to all components of the residual vector. 
#    Elements of a vector of tolerances apply to corresponding components of
#    the residual vector. AbsTol defaults to 1e-6. See RelTol. 
# 
# SingularTerm - Singular term of singular BVPs [ matrix ]
#    Set to the constant matrix S for equations of the form y' = S*y/x + f(x,y,p).
# 
# FJacobian - Analytical partial derivatives of ODEFUN 
#           [ function | matrix | cell array ]
#    For example, when solving y' = f(x,y), set this property to @FJAC if
#    DFDY = FJAC(X,Y) evaluates the Jacobian of f with respect to y.
#    If the problem involves unknown parameters, [DFDY,DFDP] = FJAC(X,Y,P)
#    must also return the partial derivative of f with respect to p.  
#    For problems with constant partial derivatives, set this property to
#    the value of DFDY or to a cell array {DFDY,DFDP}.
# 
# BCJacobian - Analytical partial derivatives of BCFUN 
#            [ function | cell array ]
#    For example, for boundary conditions bc(ya,yb) = 0, set this property to
#    @BCJAC if [DBCDYA,DBCDYB] = BCJAC(YA,YB) evaluates the partial
#    derivatives of bc with respect to ya and to yb. If the problem involves
#    unknown parameters, [DBCDYA,DBCDYB,DBCDP] = BCJAC(YA,YB,P) must also
#    return the partial derivative of bc with respect to p. 
#    For problems with constant partial derivatives, set this
#    property to a cell array {DBCDYA,DBCDYB} or {DBCDYA,DBCDYB,DBCDP}.
# 
# Nmax - Maximum number of mesh points allowed [positive integer {floor(1000/n)}]
# 
# Stats - Display computational cost statistics  [ on | {off} ]
# 
# Vectorized - Vectorized ODE function  [ on | {off} ]
#    Set this property 'on' if the derivative function 
#    ODEFUN([x1 x2 ...],[y1 y2 ...]) returns [ODEFUN(x1,y1) ODEFUN(x2,y2) ...].  
#    When parameters are present, the derivative function
#    ODEFUN([x1 x2 ...],[y1 y2 ...],p) should return 
#    [ODEFUN(x1,y1,p) ODEFUN(x2,y2,p) ...].  
# 
# MaxNewPts - Maximum number of new points introduced during mesh refinement.
#    [BVP6C ONLY] 
#    
# SlopeOut - Output derivative data for mesh and internal points. [ {on} | off ]
#    [BVP6C ONLY] 
#    Storing these values will allow cheaper computation if necessary to 
#    interpolate the bvp6c solution at given mesh points (and is necessary
#    if DEVAL is to be used). The values are output by default in SOL.YP and
#    SOL.YPMID but should be turned off to save on storage if not necessary.
#    See 'SolPts' for an alternative.
# 
# XInt - Points within range of ODE system for which a solution is required.
#    When the solution is required at a set of feasible points, they
#    are entered here and the solution interpolated within bvp6c.
#    This alternative approach to using DEVAL saves on both computation and
#    storage since values required for interpolation are already known.
#    
#    See also BVPGET, BVPINIT, BVP4C, BVP6C, DEVAL, NTRP6C.
	
   # Jacek Kierzenka and Lawrence F. Shampine
   # Copyright 1984-2003 The MathWorks, Inc. 
   # $Revision: 1.10.4.2 $  $Date: 2003/10/21 11:55:36 $
   # BVP6C Modification
   #  Nick Hale  Imperial College London
   #  $Date: 12/06/2006 $
	
# Print out possible values of properties.
	if (nargin == 0) and (nargout == 0):
		print '          AbsTol: [ positive scalar or vector {1e-6} ]\n'
		print '          RelTol: [ positive scalar {1e-3} ]\n'
		print '    SingularTerm: [ matrix ]\n'
		print '       FJacobian: [ function ]\n'
		print '      BCJacobian: [ function ]\n'
		print '           Stats: [ on | {off} ]\n'
		print '            Nmax: [ nonnegative integer {floor(1000/n)} ]\n'
		print '      Vectorized: [ on | {off} ]\n'
		print '       MaxNewPts: [ nonnegative integer {2} ]\n'
		print '        SlopeOut: [ {on} | off ]\n'
		print '            XInt: [ vector ]\n'
		print '\n'
		return
	# end
	
	Names = [
    	'AbsTol      ',
    	'RelTol      ',
    	'SingularTerm',
    	'FJacobian   ',
    	'BCJacobian  ',
    	'Stats       ',
    	'Nmax        ',
    	'Vectorized  ',
    	'MaxNewPts   ',
    	'SlopeOut    ',
    	'XInt        '
    	]
	
	
    
	m = size(Names,1)
	names = lower(Names)
	
	# Combine all leading options structures o1, o2, ... in odeset(o1,o2,...).
	options = []
	i = 1
	while i <= nargin:
		arg = varargin{i}
		if ischar(arg):                       # arg is an option name
			break;
		if ~isempty(arg):                      # [] is a valid options argument
			if ~isa(arg,'struct'):
				error('MATLAB:bvpset:NoPropNameOrStruct',...
				['Expected argument %d to be a string property name '...
                     'or an options structure\ncreated with BVPSET.'], i);
			end
			if isempty(options):
				options = arg
			else:
				for j = 1:m:
					val = arg.(deblank(Names(j,:)))
					if ~isequal(val,[]):           # empty strings '' do overwrite
						options.(deblank(Names(j,:))) = val;
					end
				end
			end
		end
		i = i + 1
	end
	if isempty(options):
		for j = 1:m:
			options.(deblank(Names(j,:))) = []
	
	# A finite state machine to parse name-value pairs.
	if rem(nargin-i+1,2) ~= 0:
		error('MATLAB:bvpset:ArgNameValueMismatch',...
        'Arguments must occur in name-value pairs.')
	expectval = 0                     # start expecting a name, not a value
	while i <= nargin:
		arg = varargin{i}    
		if ~expectval:
			if ~ischar(arg):
				error('MATLAB:bvpset:InvalidPropName',...
				'Expected argument %d to be a string property name.', i)
			lowArg = lower(arg)
			j = strmatch(lowArg,names)
			if isempty(j):                       # if no matches
 				error('MATLAB:bvpset:InvalidPropName',...
				'Unrecognized property name ''%s''.', arg)
			elif len(j) > 1:                # if more than one match
				# Check for any exact matches (in case any names are subsets of others)
				k = strcmp(lowArg,names,'exact')
				if len(k) == 1:
					j = k
				else:
					msg = sprintf('Ambiguous property name ''%s'' ', arg)
					msg = [msg '(' deblank(Names(j(1),:))]
					for k = j(2:length(j))':
						msg = [msg ', ' deblank(Names(k,:))]
					msg = sprintf('%s).', msg)
					error('MATLAB:bvpset:AmbiguousPropName', msg)
			expectval = true                      # we expect a value next    
		else:
			options.(deblank(Names(j,:))) = arg
			expectval = false
		i = i + 1
	# end (of while loop)
	
	if expectval
		error('MATLAB:bvpset:NoValueForProp',...
			'Expected value for property ''%s''.', arg)
	
	return options

