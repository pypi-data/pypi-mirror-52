from __future__ import print_function
import sys
import glob
import os
import os.path
import ssl
if hasattr(ssl, '_create_unverified_context'):
	ssl._create_default_https_context = ssl._create_unverified_context

try:
	from setuptools import setup, Extension
except:
	from distutils.core import setup
	from distutils.extension import Extension

import distutils.ccompiler


debug = '--debug' in sys.argv
if debug:
	sys.argv.remove('--debug')

new_compiler = distutils.ccompiler.new_compiler
def _new_compiler(*args, **kwargs):
	compiler = new_compiler(*args, **kwargs)
	
	def wrapper(func):
		def _wrapper(*args, **kwargs):
			kwargs['debug'] = debug
			return func(*args, **kwargs)
		return _wrapper
	
	compiler.compile = wrapper(compiler.compile)
	compiler.link_shared_object = wrapper(compiler.link_shared_object)
	compiler.create_static_lib = wrapper(compiler.create_static_lib)
	compiler.find_library_file = wrapper(compiler.find_library_file)
	if (sys.platform == 'darwin') or (sys.platform.startswith('linux')):
		def _compile_wrapper(func):
			def _wrapper(obj, src, ext, cc_args, extra_postargs, pp_opts):
				if ext == '.c':
					extra_postargs = list(extra_postargs)
					extra_postargs.remove('-std=c++11')
					if '-stdlib=libc++' in extra_postargs:
						extra_postargs.remove('-stdlib=libc++')
				elif (ext == '.cpp') and (sys.platform.startswith('linux')):
					if '-Wstrict-prototypes' in compiler.compiler_so:
						compiler.compiler_so.remove('-Wstrict-prototypes')
				return func(obj, src, ext, cc_args, extra_postargs, pp_opts)
			return _wrapper
		compiler._compile = _compile_wrapper(compiler._compile)
		compiler.language_map['.mm'] = "objc"
		compiler.src_extensions.append(".mm")
	elif sys.platform == 'win32':
		compiler.initialize()
		compiler.compile_options.append('/Z7')
	return compiler

distutils.ccompiler.new_compiler = _new_compiler


if sys.platform == 'darwin':
	sdk = os.environ.get('SDK', None)
	for index, arg in enumerate(sys.argv):
		if arg == '--sdk':
			if index + 1 >= len(sys.argv):
				print('Missing sdk parameter')
				sys.exit(1)
			sdk = sys.argv[index + 1]
			del sys.argv[index:index+2]
			break
		elif arg.startswith('--sdk='):
			sdk = arg[6:].strip()
			del sys.argv[index]
			break

	def find_sdk(version):
		path = '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX%s.sdk' % version
		if not os.path.exists(path):
			return (None, None, None)
		version_min = '10.8'
		return (path, version_min, version)

	if sdk is not None:
		sdk, macosx_version_min, macosx_version = find_sdk(sdk)
		if sdk is None:
			print('Error: unknown SDK:', sdk)
			sys.exit(1)
	else:
		for version in ('10.8', '10.9', '10.10', '10.11', '10.12', '10.13', '10.14'):
			sdk, macosx_version_min, macosx_version = find_sdk(version)
			if sdk is not None:
				break
		else:
			print('Error: no valid SDK found!')
			sys.exit(1)
	cflags = '-g -ggdb -Wno-deprecated-register -Wno-sometimes-uninitialized -Wno-write-strings -fvisibility=hidden -mmacosx-version-min=%s -isysroot %s -F/Library/Frameworks -I/usr/local/include' % (macosx_version_min, sdk)
	ldflags = '-Wl,-syslibroot,%s -L/usr/local/lib -framework Foundation -lkonga_client_s -lebpr_s -lpcre -lz -mmacosx-version-min=%s -headerpad_max_install_names' % (sdk, macosx_version_min)
	cflags += ' -stdlib=libc++ -std=c++11'
	ldflags += ' -stdlib=libc++'
	sdk = os.environ.get('KONGASDK')
	if sdk:
		cflags += ' -I"%s/include"' % sdk
		ldflags += ' -L"%s/lib"' % sdk
	extra_libs = ''
elif sys.platform == 'win32':
	suffix = '_d' if debug else ''
	cflags = '/EHsc /D_CRT_SECURE_NO_WARNINGS /Z7 /wd4244 /wd4005 /wd4267'
	ldflags = '/DEBUG /NODEFAULTLIB:LIBCMT /ignore:4197'
	extra_libs = 'ebpr_s%s konga_client_s%s zlib%s shell32 user32 netapi32 iphlpapi shlwapi advapi32 secur32 ws2_32' % (suffix, suffix, suffix[1:])
	sdk = os.environ.get('KONGASDK')
	if sdk:
		cflags += ' /I"%s\\Include"' % sdk
		ldflags += ' /LIBPATH:"%s\\Lib"' % sdk
else:
	cflags = '-g -Wno-maybe-uninitialized -Wno-write-strings -fvisibility=hidden -I/usr/local/include -std=c++11 -D__STDC_LIMIT_MACROS -D__STDC_FORMAT_MACROS'
	ldflags = '-L/usr/local/lib -lkonga_client_s -lebpr_s -lpcre -lz -ldbus-1'
	extra_libs = ''


if 'KONGALIB_CFLAGS' in os.environ:
	cflags = '%s %s' % (os.environ['KONGALIB_CFLAGS'], cflags)
#	print("***** CUSTOM KONGALIB_CFLAGS")
if 'KONGALIB_LDFLAGS' in os.environ:
	ldflags = '%s %s' % (os.environ['KONGALIB_LDFLAGS'], ldflags)
#	print("***** CUSTOM KONGALIB_LDFLAGS")

defines = [
	('NOUNCRYPT', None),
	('UNICODE', None),
	('YAJL_BUILD', None),
]
if sys.platform == 'win32':
	defines.append(('WIN32', None))


here = os.path.abspath(os.path.dirname(__file__))
if sys.version_info[0] < 3:
	README = open(os.path.join(here, 'README')).read()
	VERSION = open(os.path.join(here, 'VERSION')).read()
else:
	README = open(os.path.join(here, 'README'), encoding='utf-8').read()
	VERSION = open(os.path.join(here, 'VERSION'), encoding='utf-8').read()

setup(
    name = 'kongalib',
    version = VERSION,
    
    packages = [ 'kongalib' ],
    package_dir = { 'kongalib': 'src' },
    
    ext_modules = [ Extension('kongalib._kongalib',
    	glob.glob(os.path.join('src', '_kongalib', '*.cpp')) + glob.glob(os.path.join('src', '_kongalib', 'yajl-2.0.1', 'src', '*.c')),
    	include_dirs = [
    		os.path.join('src', '_kongalib'),
    		os.path.join('src', '_kongalib', 'yajl-2.0.1', 'src'),
    		os.path.join('src', '_kongalib', 'yajl-2.0.1', 'include'),
    	],
    	define_macros = defines,
    	extra_compile_args = cflags.split(),
    	extra_link_args = ldflags.split(),
    	libraries = extra_libs.split(),
    ) ],
    
	zip_safe = True,

    # metadata for upload to PyPI
    author = "EasyByte Software",
    author_email = "konga@easybyte.it",
    description = "Konga client library",
    license = "LGPL",
    keywords = [ "konga", "client", "erp" ],
    url = "http://www.easybyte.it",
	classifiers = [
		"Natural Language :: Italian",
		"Programming Language :: Python",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 3",
		"Programming Language :: C++",
		"Development Status :: 5 - Production/Stable",
		"Environment :: Console",
		"Intended Audience :: Developers",
		"Intended Audience :: Information Technology",
		"Intended Audience :: Financial and Insurance Industry",
		"License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: Microsoft :: Windows",
		"Operating System :: POSIX :: Linux",
		"Topic :: Office/Business",
		"Topic :: Office/Business :: Financial",
		"Topic :: Software Development :: Libraries",
	],
	long_description = README,
)

