from pyparsing import Word, Literal, alphas, nums, alphanums, OneOrMore, Optional, SkipTo, ParseException, Group, ZeroOrMore, Suppress, Combine

#Qualifier to go in front of type in the argument list (unsigned const int foo)
qualifier = OneOrMore(Literal('const') ^ Literal('unsigned'))

#Skip pairs of brackets.
#TODO Fix for nesting brackets
angle_bracket_pair = Literal('<') + SkipTo('>') + Literal('>')
parentheses_pair = Literal('(') + SkipTo(')') + Literal(')')
square_bracket_pair = Literal('[') + SkipTo(']') + Literal(']')

#The raw type of the input, i.e. 'int' in (unsigned const int * foo)
input_type = Combine(Word(alphanums + ':_') + Optional(angle_bracket_pair))

#A fully qualified name. Used when it is not a function passed in (i.e. no parentheses)
symbol = Combine(OneOrMore(Word(alphanums + ':_') ^ angle_bracket_pair ^ parentheses_pair ^ square_bracket_pair))

#A number. e.g. -1, 3.6 or 5
number = Word('-.' + nums)

#The name of the argument. We will ignore this but it must be matched anyway.
input_name = OneOrMore(Word(alphanums + '_') ^ angle_bracket_pair ^ parentheses_pair ^ square_bracket_pair)

#Grab the '&', '*' or '**' type bit in (const QString & foo, int ** bar)
pointer_or_reference = Word('*&')

#The '=QString()' or '=false' bit in (int foo = 4, bool bar = false)
default_value = Literal('=') + OneOrMore(angle_bracket_pair ^ parentheses_pair ^ square_bracket_pair ^ input_type ^ number ^ Word('|&^'))

#A combination building up the interesting bit -- the argument type, e.g. 'const QString &', 'int' or 'char*'
argument_type = Optional(qualifier, default='').setResultsName("qualifier") + input_type.setResultsName("input_type") + Optional(pointer_or_reference, default='').setResultsName("pointer_or_reference")

#Argument + variable name + default
argument = Group(argument_type.setResultsName('argument_type') + Optional(input_name) + Optional(default_value))

#List of arguments in parentheses with an optional 'const' on the end
arglist = Literal('(') + Group(ZeroOrMore(argument + Suppress(Literal(','))) + Optional(argument)).setResultsName('arg_list') + Literal(')') + Optional(Literal('const'), default='').setResultsName('const_function')

full_symbol = (SkipTo('(').setResultsName('function_name') + Optional(arglist)) ^ symbol.setResultsName('symbol') #In this case 'input_type' is the function name

def normalise(sample):
	try:
		result = full_symbol.parseString(sample)
	except ParseException, pe:
		print sample
		print pe
	else:
		normalised_arg_list = []
		
		for arg in result.arg_list:
			argument = ''
			if arg.qualifier:
				argument += arg.qualifier + ' '
			argument += arg.input_type
			if arg.pointer_or_reference:
				argument += arg.pointer_or_reference
			
			normalised_arg_list += [argument]
		
		normalised_arg_list_string = '(' + ', '.join(normalised_arg_list) + ')'
		
		if result.const_function:
			normalised_arg_list_string += ' ' + result.const_function
		
		#If we found a 'symbol' then there were no brackets after the requested name. Therefore it is not necessarily a function
		if result.symbol:
			return result.symbol, ''
		
		return result.function_name, normalised_arg_list_string
	
	return None

if __name__ == "__main__":
	
	samples = ['( const QXmlSchema & other )',
	'( QUrl source )',
	'( QUrl * source )',
	'( QUrl ** source )',
	'( const QUrl ** source )',
	'( const QUrl source )',
	'( QUrl & source )',
	'( const QUrl & source )',
	'( const QUrl * source )',
	'( QIODevice * source, const QUrl & documentUri = QUrl() )',
	'( const QByteArray & data, const QUrl & documentUri = QUrl() )',
	'( const QAbstractMessageHandler * handler )',
	'( QAbstractMessageHandler * handler )',
	'(void)',
	'(uint32_t uNoOfBlocksToProcess=(std::numeric_limits< uint32_t >::max)())',
	'( QWidget * parent = 0, const char * name = 0, Qt::WindowFlags f = 0 )',
	'( const QPixmap & icon, bool recalc, bool redraw = true )',
	'( const QString & text, bool recalc, bool redraw = true )',
	'( const QString & foo, bool recalc, bool redraw = true )',
	'( const QString & text, bool recalc, bool redraw=true )',
	'( const QString & text, bool recalc, bool redraw )',
	'( QUrl source, int foo, double bar )',
	'()',
	'( const QPixmap & pixmap, const QString & text, int index = -1 )',
	'( const char ** strings, int numStrings = -1, int index = -1 )',
	'( const QStringList & list, int index = -1 )',
	'( int index = 0 )',
	'( bool ascending = true )',
	'( Q3ListBox * listbox = 0 )',
	'( Q3ListBox * listbox, const QString & text = QString())',
	'( const QString & text = QString())',
	'( QWidget * parent = 0, const char * name = 0, Qt::WindowFlags f = 0 )',
	'( const QString & label, int width = -1 )',
	'( const QIcon & icon, const QString & label, int width = -1 )',
	'( const QString & text, int column, ComparisonFlags compare = ExactMatch | Qt::CaseSensitive )',
	'( int column, bool ascending = true )',
	'( Q3ListView * parent, const QString & label1, const QString & label2 = QString())',
	'( Q3ListViewItem * parent, const QString & label1, const QString & label2 = QString())',
	'( Q3ListView * parent, Q3ListViewItem * after, const QString & label1, const QString & label2 = QString())',
	'( Q3ListViewItem * parent, Q3ListViewItem * after, const QString & label1, const QString & label2 = QString())',
	'( int c = -1 )',
	'( QWidget * parent = 0, const char * name = 0, Qt::WindowFlags f = Qt::WType_TopLevel )',
	'( Q3DockWindow * dockWindow, Qt::Dock edge = Qt::DockTop, bool newLine = false )',
	'( Q3DockWindow * dockWindow, const QString & label, Qt::Dock edge = Qt::DockTop, bool newLine = false )',
	'( Q3DockWindow * dockWindow, Qt::Dock position = Qt::DockTop, bool newLine = false )',
	'( Q3DockWindow * dockWindow, const QString & label, Qt::Dock position = Qt::DockTop, bool newLine = false )',
	'( DockWindows dockWindows = AllDockWindows )',
	'( bool keepNewLines = false )',
	'( bool keepNewLines = false )',
	'( int pos, int length = -1 )',
	'( const QSize & size, QVideoFrame::PixelFormat format, QAbstractVideoBuffer::HandleType type = QAbstractVideoBuffer::NoHandle )',
	'( QMutex * mutex, unsigned long time = ULONG_MAX )',
	'( QReadWriteLock * readWriteLock, unsigned long time = ULONG_MAX )',
	'( const QString & name, const QString & defaultValue = QString())',
	'( const QString & namespaceUri, const QString & name, const QString & defaultValue = QString())',
	'( const QString & namespaceUri = QString())',
	'( QPainter * painter, RenderLayer layer, const QRegion & clip = QRegion())',
	'( const QByteArray & data, const QString & mimeType = QString())',
	'( const QString & html, const QUrl & baseUrl = QUrl())',
	'( QObject * parent = 0 )',
	'( QWidget * parent = 0 )',
	'( QObject * parent = 0 )',
	'( Extension extension, const ExtensionOption * option = 0, ExtensionReturn * output = 0 )',
	'( const QString & subString, FindFlags options = 0 )',
	'( WebAction action, bool checked = false )',
	'( QObject * parent = 0 )',
	'(Volume< VoxelType > &volData, const Region &regionToSmooth)',
	'(const VolumeSampler< VoxelType > &volIter)',
	'(VolumeSampler< VoxelType > &volIter)',
	'(VolumeSampler< VoxelType > &volIter)',
	'(const VolumeSampler< VoxelType > &volIter)',
	'(VolumeSampler< VoxelType > &volIter)',
	'(Volume< uint8_t > *volumeData, SurfaceMesh &mesh, NormalGenerationMethod normalGenerationMethod)',
	'(Volume< uint8_t > *volumeData, const Vector3DFloat &v3dPos, NormalGenerationMethod normalGenerationMethod)',
	'(const VolumeSampler< VoxelType > &volIter)',
	'(const MeshEdge &lhs, const MeshEdge &rhs)',
	'(const MeshEdge &lhs, const MeshEdge &rhs)',
	'(const Vector< Size, Type > &lhs, const Vector< Size, Type > &rhs)',
	'(const Vector< Size, Type > &lhs, const Vector< Size, Type > &rhs)',
	'(const Vector< Size, Type > &lhs, const Type &rhs)',
	'(const Vector< Size, Type > &lhs, const Type &rhs)',
	'(std::ostream &os, const Vector< Size, Type > &vector)',
	'(VolumeSampler< uint8_t > &volIter)',
	'(const SurfaceEdge &lhs, const SurfaceEdge &rhs)',
	'(const SurfaceEdge &lhs, const SurfaceEdge &rhs)',
	'(std::istream &stream, VolumeSerializationProgressListener *progressListener=0)',
	'(std::ostream &stream, Volume< VoxelType > &volume, VolumeSerializationProgressListener *progressListener=0)',
	'(std::istream &stream, VolumeSerializationProgressListener *progressListener=0)',
	'(std::ostream &stream, Volume< VoxelType > &volume, VolumeSerializationProgressListener *progressListener=0)',
	'(const uint32_t(&pDimensions)[noOfDims])',
	'(uint32_t uIndex)',
	'(uint32_t uIndex) const ',
	'(void) const', 
	'(void) const', 
	'(const uint32_t(&pDimensions)[noOfDims])',
	'(Array< noOfDims, ElementType > &rhs)',
	'( const QString & path, const QString & nameFilter, SortFlags sort = SortFlags( Name | IgnoreCase ))',
	'( const QBrush & foreground, const QBrush & button, const QBrush & light, const QBrush & dark, const QBrush & mid, const QBrush & text, const QBrush & bright_text, const QBrush & base, const QBrush & background )',
	'( int width, int height, Attachment attachment, GLenum target = GL_TEXTURE_2D, GLenum internal_format = GL_RGBA8 )',
	'( GLuint texture_id )',
	'PolyVox::Volume::getDepth',
	'PolyVox::Volume::getDepth()',
	'Volume::getVoxelAt(uint16_t uXPos, uint16_t uYPos, uint16_t uZPos, VoxelType tDefault=VoxelType()) const',
	'PolyVox::Array::operator[]',
	'operator[]',
	'( Q3ValueList<T>::size_type i )',
	]
	
	for sample in samples:
		print sample
		normalised_sample = normalise(sample)
		print normalised_sample, '\n'
