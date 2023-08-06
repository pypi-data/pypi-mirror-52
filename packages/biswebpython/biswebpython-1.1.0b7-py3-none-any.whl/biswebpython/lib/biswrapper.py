
import math
import os
import platform 
import sys
import numpy as np
import ctypes 
import struct
import json
import biswebpython.core.bis_wasmutils as wasmutil

def initialize_module():

  dirname=os.path.dirname(os.path.abspath(__file__));
  if os.name == 'nt':
      libname=dirname+'\\biswasm.dll';
  elif platform.system() == 'Darwin':
      libname=dirname+'/libbiswasm.dylib';
  else:
      libname=dirname+'/libbiswasm.so';

  print('____ Loading library from ',libname);
  wasmutil.load_library(libname);


#--------------------------------------------------------------
# C++:
#/** return a matlab matrix from a serialized .mat V6 file packed into an unsigned char serialized array
#* @param input serialized input as unsigned char array
#* @param jsonstring the parameter string for this algorithm { 'name' :  ""} specifies the matrix name
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized matrix
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'parseMatlabV6WASM', 'Matrix', [ 'Vector', 'ParamObj', 'debug' ]}
#      returns a Matrix
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def parseMatlabV6WASM(vector1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    vector1_ptr=wasmutil.wrapper_serialize(vector1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:parseMatlabV6WASM with ',jsonstring,'\n++++');

    Module.parseMatlabV6WASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.parseMatlabV6WASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.parseMatlabV6WASM(vector1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'Matrix');
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** return a matrix from a text file (octave .matr or 4x4 matrix .matr)
#* @param input text of whole file
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized matrix
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'parseMatrixTextFileWASM', 'Matrix', [ 'String', 'debug' ]}
#      returns a Matrix
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def parseMatrixTextFileWASM(string1,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;


    # Serialize objects and encode strings
    string1_binstr=str.encode(string1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:parseMatrixTextFileWASM\n++++');

    Module.parseMatrixTextFileWASM.argtypes=[ctypes.c_char_p, ctypes.c_int];
    Module.parseMatrixTextFileWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.parseMatrixTextFileWASM(string1_binstr, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'Matrix');
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** return a string (for a text file -- octave .matr or 4x4 matrix .matr) for a matrix
#* @param input serialized input Matrix as unsigned char array
#* @param name the name of the matrix
#* @param legacy if true then output 4x4 matrix transformation else old .matr file
#* @param debug if > 0 print debug messages
#* @returns a pointer to the string
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'createMatrixTextFileWASM', 'String', [ 'Matrix', 'String', 'Int', 'debug' ]}
#      returns a String
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def createMatrixTextFileWASM(matrix1,string2,intval3,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;


    # Serialize objects and encode strings
    matrix1_ptr=wasmutil.wrapper_serialize(matrix1);
    string2_binstr=str.encode(string2);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:createMatrixTextFileWASM\n++++');

    Module.createMatrixTextFileWASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int];
    Module.createMatrixTextFileWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.createMatrixTextFileWASM(matrix1_ptr, string2_binstr, intval3, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'String');
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** return a combo transformation a .grd text file
#* @param input text of whole file
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized bisComboTransformation
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'parseComboTransformTextFileWASM', 'bisComboTransformation', [ 'String', 'debug' ]}
#      returns a bisComboTransformation
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def parseComboTransformTextFileWASM(string1,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;


    # Serialize objects and encode strings
    string1_binstr=str.encode(string1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:parseComboTransformTextFileWASM\n++++');

    Module.parseComboTransformTextFileWASM.argtypes=[ctypes.c_char_p, ctypes.c_int];
    Module.parseComboTransformTextFileWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.parseComboTransformTextFileWASM(string1_binstr, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisComboTransformation');
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** return a string (for a grd file)
#* @param input serialized input combo transformation as unsigned char array
#* @param debug if > 0 print debug messages
#* @returns a pointer to the string
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'createComboTransformationTextFileWASM', 'String', [ 'bisComboTransformation', 'debug' ]}
#      returns a String
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def createComboTransformationTextFileWASM(comboxform1,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;


    # Serialize objects and encode strings
    comboxform1_ptr=wasmutil.wrapper_serialize(comboxform1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:createComboTransformationTextFileWASM\n++++');

    Module.createComboTransformationTextFileWASM.argtypes=[ctypes.c_void_p, ctypes.c_int];
    Module.createComboTransformationTextFileWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.createComboTransformationTextFileWASM(comboxform1_ptr, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'String');
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** return a matrix with a qform description from an sform desription (NIFTI-1 code)
#* @param input serialized input 4x4 Matrix as unsigned char array
#* @param debug if > 0 print debug messages
#* @returns a pointer to the output 10x1 matrix containing the quaternion representation
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'niftiMat44ToQuaternionWASM', 'Matrix', [ 'Matrix', 'debug' ]}
#      returns a Matrix
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def niftiMat44ToQuaternionWASM(matrix1,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;


    # Serialize objects and encode strings
    matrix1_ptr=wasmutil.wrapper_serialize(matrix1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:niftiMat44ToQuaternionWASM\n++++');

    Module.niftiMat44ToQuaternionWASM.argtypes=[ctypes.c_void_p, ctypes.c_int];
    Module.niftiMat44ToQuaternionWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.niftiMat44ToQuaternionWASM(matrix1_ptr, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'Matrix');
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Extract image frame using \link bisImageAlgorithms::imageExtractFrame \endlink
#* @param input serialized input as unsigned char array
#* @param jsonstring the parameter string for the algorithm { "frame" : 0 , " component" : 0 }
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'extractImageFrameWASM', 'bisImage', [ 'bisImage', 'ParamObj', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def extractImageFrameWASM(image1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:extractImageFrameWASM with ',jsonstring,'\n++++');

    Module.extractImageFrameWASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.extractImageFrameWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.extractImageFrameWASM(image1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Extract 2d image slice using \link bisImageAlgorithms::imageExtractSlice \endlink
#* @param input serialized input as unsigned char array
#* @param jsonstring the parameter string for the algorithm { "plane" : 2, "slice":-1, "frame" : 0 , " component" : 0 } (slice=-1 = center slice)
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'extractImageSliceWASM', 'bisImage', [ 'bisImage', 'ParamObj', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def extractImageSliceWASM(image1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:extractImageSliceWASM with ',jsonstring,'\n++++');

    Module.extractImageSliceWASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.extractImageSliceWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.extractImageSliceWASM(image1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Normalize image using \link bisImageAlgorithms::imageNormalize \endlink
#* @param input serialized input as unsigned char array
#* @param jsonstring the parameter string for the algorithm { "perlow" : 0.0 , "perhigh" : 1.0, "outmaxvalue" : 1024 }
#* @param debug if > 0 print debug messages
#* @returns a pointer to a normalized image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'normalizeImageWASM', 'bisImage', [ 'bisImage', 'ParamObj', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def normalizeImageWASM(image1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:normalizeImageWASM with ',jsonstring,'\n++++');

    Module.normalizeImageWASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.normalizeImageWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.normalizeImageWASM(image1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Threshold image using \link bisImageAlgorithms::thresholdImage \endlink
#* @param input serialized input as unsigned char array
#* @param jsonstring the parameter string for the algorithm { "low" : 50.0, "high": 100, "replacein" :  true, "replaceout" : false, "invalue: 100.0 , "outvalue" : 0.0, "datatype: -1 }, (datatype=-1 same as input)
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'thresholdImageWASM', 'bisImage', [ 'bisImage', 'ParamObj', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def thresholdImageWASM(image1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:thresholdImageWASM with ',jsonstring,'\n++++');

    Module.thresholdImageWASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.thresholdImageWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.thresholdImageWASM(image1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** ShiftScale image using \link bisImageAlgorithms::shiftScaleImage \endlink
#* @param input serialized input as unsigned char array
#* @param jsonstring the parameter string for the algorithm { "shift" : 0.0, "scale": 1.0, "datatype: -1 }, (datatype=-1 same as input)
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'shiftScaleImageWASM', 'bisImage', [ 'bisImage', 'ParamObj', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def shiftScaleImageWASM(image1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:shiftScaleImageWASM with ',jsonstring,'\n++++');

    Module.shiftScaleImageWASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.shiftScaleImageWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.shiftScaleImageWASM(image1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Threshold image using \link bisImageAlgorithms::thresholdImage \endlink
#* @param input serialized input as unsigned char array
#* @param jsonstring the parameter string for the algorithm { "threshold" : 50.0, "clustersize": 100, "oneconnected" :  true, "outputclusterno" : false, "frame" :0, "component":0, "datatype: -1 }, (datatype=-1 same as input)
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'clusterThresholdImageWASM', 'bisImage', [ 'bisImage', 'ParamObj', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def clusterThresholdImageWASM(image1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:clusterThresholdImageWASM with ',jsonstring,'\n++++');

    Module.clusterThresholdImageWASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.clusterThresholdImageWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.clusterThresholdImageWASM(image1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Smooth image using \link bisImageAlgorithms::gaussianSmoothImage \endlink
#* @param input serialized input as unsigned char array
#* @param jsonstring the parameter string for the algorithm { "sigma" : 1.0, "inmm" :  true, "radiusfactor" : 1.5 , "vtkboundary": false},
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'gaussianSmoothImageWASM', 'bisImage', [ 'bisImage', 'ParamObj', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def gaussianSmoothImageWASM(image1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:gaussianSmoothImageWASM with ',jsonstring,'\n++++');

    Module.gaussianSmoothImageWASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.gaussianSmoothImageWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.gaussianSmoothImageWASM(image1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Compute image gradient using  using \link bisImageAlgorithms::gradientImage \endlink
#* @param input serialized input as unsigned char array
#* @param jsonstring the parameter string for the algorithm { "sigma" : 1.0, "inmm" :  true, "radiusfactor" : 1.5 },
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'gradientImageWASM', 'bisImage', [ 'bisImage', 'ParamObj', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def gradientImageWASM(image1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:gradientImageWASM with ',jsonstring,'\n++++');

    Module.gradientImageWASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.gradientImageWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.gradientImageWASM(image1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Reslice image using \link bisImageAlgorithms::resliceImage \endlink
#* @param input serialized input as unsigned char array
#* @param transformation serialized transformation as unsigned char array
#* @param jsonstring the parameter string for the algorithm  { int interpolation=3, 1 or 0, float backgroundValue=0.0; int ouddim[3], int outspa[3], int bounds[6] = None -- use out image size }
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'resliceImageWASM', 'bisImage', [ 'bisImage', 'bisTransformation', 'ParamObj', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def resliceImageWASM(image1,transformation2,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);
    transformation2_ptr=wasmutil.wrapper_serialize(transformation2);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:resliceImageWASM with ',jsonstring,'\n++++');

    Module.resliceImageWASM.argtypes=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.resliceImageWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.resliceImageWASM(image1_ptr, transformation2_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Crop an image using \link bisImageAlgorithms::cropImage \endlink
#* @param input serialized input as unsigned char array
#* @param jsonstring the parameter string for the algorithm
#* { "i0" : 0: ,"i1" : 100, "di" : 2, "j0" : 0: ,"j1" : 100, "dj" : 2,"k0" : 0: ,"k1" : 100, "dk" : 2, "t0" : 0: ,"t1" : 100, "dt" : 2 }
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'cropImageWASM', 'bisImage', [ 'bisImage', 'ParamObj', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def cropImageWASM(image1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:cropImageWASM with ',jsonstring,'\n++++');

    Module.cropImageWASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.cropImageWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.cropImageWASM(image1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Flip an image using \link bisImageAlgorithms::flipImage \endlink
#* @param input serialized input as unsigned char array
#* @param jsonstring the parameter string for the algorithm { "flipi" : 0, "flipj" : 0 , "flipk" : 0 }
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'flipImageWASM', 'bisImage', [ 'bisImage', 'ParamObj', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def flipImageWASM(image1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:flipImageWASM with ',jsonstring,'\n++++');

    Module.flipImageWASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.flipImageWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.flipImageWASM(image1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Blank an image using \link bisImageAlgorithms::blankImage \endlink
#* @param input serialized input as unsigned char array
#* @param jsonstring the parameter string for the algorithm
#* { "i0" : 0: ,"i1" : 100, "j0" : 0: ,"j1" : 100,"k0" : 0: ,"k1" : 100, }
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'blankImageWASM', 'bisImage', [ 'bisImage', 'ParamObj', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def blankImageWASM(image1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:blankImageWASM with ',jsonstring,'\n++++');

    Module.blankImageWASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.blankImageWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.blankImageWASM(image1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Median Normalize an Image an image using \link bisImageAlgorithms::medianNormalizeImage \endlink
#* @param input serialized input as unsigned char array
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'medianNormalizeImageWASM', 'bisImage', [ 'bisImage', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def medianNormalizeImageWASM(image1,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;


    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:medianNormalizeImageWASM\n++++');

    Module.medianNormalizeImageWASM.argtypes=[ctypes.c_void_p, ctypes.c_int];
    Module.medianNormalizeImageWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.medianNormalizeImageWASM(image1_ptr, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Resample image using \link bisImageAlgorithms::resampleImage \endlink
#* @param input serialized input as unsigned char array
#* @param jsonstring the parameter string for the algorithm  { int dim[3], float spacing[3], int interpolation; 3, 1 or 0, float backgroundValue=0.0 };
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'resampleImageWASM', 'bisImage', [ 'bisImage', 'ParamObj', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def resampleImageWASM(image1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:resampleImageWASM with ',jsonstring,'\n++++');

    Module.resampleImageWASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.resampleImageWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.resampleImageWASM(image1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Prepare Image for Registration using \link bisImageAlgorithms::prepareImageForRegistration \endlink
#* @param input serialized input as unsigned char array
#* @param jsonstring the parameter string for the algorithm
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'prepareImageForRegistrationWASM', 'bisImage', [ 'bisImage',  'ParamObj','debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def prepareImageForRegistrationWASM(image1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:prepareImageForRegistrationWASM with ',jsonstring,'\n++++');

    Module.prepareImageForRegistrationWASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.prepareImageForRegistrationWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.prepareImageForRegistrationWASM(image1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Compute Displacement Field
#* @param transformation the transformation to use to compute a displacement field
#* @param jsonstring the parameter string for the algorithm
#*   { "dimensions":  [ 8,4,4 ], "spacing": [ 2.0,2.5,2.5 ] };
#* @param debug if > 0 print debug messages
#* @returns a pointer to the displacement field image (bisSimpleImage<float>)
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'computeDisplacementFieldWASM', 'bisImage', [ 'bisTransformation', 'ParamObj','debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def computeDisplacementFieldWASM(transformation1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    transformation1_ptr=wasmutil.wrapper_serialize(transformation1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:computeDisplacementFieldWASM with ',jsonstring,'\n++++');

    Module.computeDisplacementFieldWASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.computeDisplacementFieldWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.computeDisplacementFieldWASM(transformation1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage');
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Perform slice based bias field correction and return either image or bias field (if returnbiasfield=true)
#* @param input serialized input as unsigned char array
#* @param jsonstring the parameter string for the algorithm { "axis" : 2, "threshold":0.02, "returnbiasfield" : false }. If axis >=3 (or <0) then triple slice is done, i.e. all three planes
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized corrected image  (or the bias field if returnbias=true)
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'sliceBiasFieldCorrectImageWASM', 'bisImage', [ 'bisImage', 'ParamObj', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def sliceBiasFieldCorrectImageWASM(image1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:sliceBiasFieldCorrectImageWASM with ',jsonstring,'\n++++');

    Module.sliceBiasFieldCorrectImageWASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.sliceBiasFieldCorrectImageWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.sliceBiasFieldCorrectImageWASM(image1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Perform morphology operation (one of "median", "erode", "dilate") on binary images
#* @param input serialized binary input image as unsigned char array
#* @param jsonstring the parameter string for the algorithm { "operation" : "median", "radius" : 1, "3d" : true }
#* @param debug if > 0 print debug messages
#* @returns a pointer to a (unsigned char) serialized binary image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'morphologyOperationWASM', 'bisImage', [ 'bisImage', 'ParamObj', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def morphologyOperationWASM(image1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:morphologyOperationWASM with ',jsonstring,'\n++++');

    Module.morphologyOperationWASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.morphologyOperationWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.morphologyOperationWASM(image1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Perform seed connectivity operation
#* @param input serialized binary input image as unsigned char array
#* @param jsonstring the parameter string for the algorithm { "seedi" : 10, "seedj": 20", "seedk" : 30, "oneconnected" : true }
#* @param debug if > 0 print debug messages
#* @returns a pointer to a (unsigned char) serialized binary image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'seedConnectivityWASM', 'bisImage', [ 'bisImage', 'ParamObj', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def seedConnectivityWASM(image1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:seedConnectivityWASM with ',jsonstring,'\n++++');

    Module.seedConnectivityWASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.seedConnectivityWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.seedConnectivityWASM(image1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Computes GLM Fit for fMRI
#* @param input input time series as serialized array
#* @param mask for input time series (ignore is jsonstring has usemasks : 0 ) as serialized array
#* @param matrix  the regressor matrix as serialized array
#* @param jsonstring the parameter string for the algorithm { "usemask" : 1, "numstasks":-1 }  (numtaks=-1, means all are tasks)
#* @param debug if > 0 print debug messages
#* @returns a pointer to the beta image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'computeGLMWASM', 'bisImage', [ 'bisImage', 'bisImage_opt', 'Matrix', 'ParamObj', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def computeGLMWASM(image1,image2,matrix3,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);
    image2_ptr=0
    if image2!=0 and image2!=None: 
      image2_ptr=wasmutil.wrapper_serialize(image2);
    matrix3_ptr=wasmutil.wrapper_serialize(matrix3);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:computeGLMWASM with ',jsonstring,'\n++++');

    Module.computeGLMWASM.argtypes=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.computeGLMWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.computeGLMWASM(image1_ptr, image2_ptr, matrix3_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Computes ROI Mean for a timeseries
#* @param input input image time series as serialized array
#* @param roi   input roi image
#* @param jsonstring  the parameter string for the algorithm { "storecentroids" : 0 }
#* @param debug if > 0 print debug messages
#* @returns a pointer to the roi matrix (rows=frames,cols=rois)
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'computeROIWASM', 'Matrix', [ 'bisImage', 'bisImage', 'ParamObj',  'debug' ], {"checkorientation" : "all"}}
#      returns a Matrix
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def computeROIWASM(image1,image2,paramobj,debug=0):

    Module=wasmutil.Module();

    if (image1.hasSameOrientation(image2,'image1','image2',True)==False):
       return False;

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);
    image2_ptr=wasmutil.wrapper_serialize(image2);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:computeROIWASM with ',jsonstring,'\n++++');

    Module.computeROIWASM.argtypes=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.computeROIWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.computeROIWASM(image1_ptr, image2_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'Matrix');
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Compute butterworthFilter Output
#* @param input the input matrix to filter (time = rows)
#* @param jsonstring the parameters { "type": "low", "cutoff": 0.15, 'sampleRate': 1.5 };
#* @param debug if > 0 print debug messages
#* @returns a pointer to the filtered matrix (rows=frames,cols=rois)
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'butterworthFilterWASM', 'Matrix', [ 'Matrix', 'ParamObj',  'debug' ]}
#      returns a Matrix
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def butterworthFilterWASM(matrix1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    matrix1_ptr=wasmutil.wrapper_serialize(matrix1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:butterworthFilterWASM with ',jsonstring,'\n++++');

    Module.butterworthFilterWASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.butterworthFilterWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.butterworthFilterWASM(matrix1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'Matrix');
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Compute butterworthFilter Output applied to images
#* @param input the input image to filter
#* @param jsonstring the parameters { "type": "low", "cutoff": 0.15, 'sampleRate': 1.5 };
#* @param debug if > 0 print debug messages
#* @returns a pointer to the filtered image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'butterworthFilterImageWASM', 'bisImage', [ 'bisImage', 'ParamObj',  'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def butterworthFilterImageWASM(image1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:butterworthFilterImageWASM with ',jsonstring,'\n++++');

    Module.butterworthFilterImageWASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.butterworthFilterImageWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.butterworthFilterImageWASM(image1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Compute correlation matrix
#* @param input the input timeseries matrix (roi output, rows=frames);
#* @param weights the input weight vector ( rows=frames);
#* @param jsonstring the parameters { "zscore": "false" }
#* @param debug if > 0 print debug messages
#* @returns a pointer to the filtered matrix (rows=frames,cols=rois)
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'computeCorrelationMatrixWASM', 'Matrix', [ 'Matrix', 'Vector_opt', 'ParamObj',  'debug' ]}
#      returns a Matrix
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def computeCorrelationMatrixWASM(matrix1,vector2,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    matrix1_ptr=wasmutil.wrapper_serialize(matrix1);
    vector2_ptr=0
    if vector2!=0 and vector2!=None: 
      vector2_ptr=wasmutil.wrapper_serialize(vector2);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:computeCorrelationMatrixWASM with ',jsonstring,'\n++++');

    Module.computeCorrelationMatrixWASM.argtypes=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.computeCorrelationMatrixWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.computeCorrelationMatrixWASM(matrix1_ptr, vector2_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'Matrix');
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Regress out a time series from another (with optional weights)
#* @param input_ptr the input timeseries matrix (roi output, rows=frames);
#* @param regressor_ptr the regression timeseries matrix (roi output, rows=frames);
#* @param weights_ptr the input weight vector ( rows=frames) or 0 ;
#* @param debug if > 0 print debug messages
#* @returns a pointer to the filtered matrix (rows=frames,cols=rois)
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'weightedRegressOutWASM', 'Matrix', [ 'Matrix', 'Matrix', 'Vector_opt',  'debug' ]}
#      returns a Matrix
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def weightedRegressOutWASM(matrix1,matrix2,vector3,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;


    # Serialize objects and encode strings
    matrix1_ptr=wasmutil.wrapper_serialize(matrix1);
    matrix2_ptr=wasmutil.wrapper_serialize(matrix2);
    vector3_ptr=0
    if vector3!=0 and vector3!=None: 
      vector3_ptr=wasmutil.wrapper_serialize(vector3);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:weightedRegressOutWASM\n++++');

    Module.weightedRegressOutWASM.argtypes=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int];
    Module.weightedRegressOutWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.weightedRegressOutWASM(matrix1_ptr, matrix2_ptr, vector3_ptr, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'Matrix');
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Regress out a time series from another (with optional weights)
#* @param input_ptr the input timeseries image
#* @param regressor_ptr the regression timeseries matrix (roi output, rows=frames);
#* @param weights_ptr the input weight vector ( rows=frames) or 0 ;
#* @param debug if > 0 print debug messages
#* @returns a pointer to the filtered image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'weightedRegressOutImageWASM', 'bisImage', [ 'bisImage', 'Matrix', 'Vector_opt',  'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def weightedRegressOutImageWASM(image1,matrix2,vector3,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;


    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);
    matrix2_ptr=wasmutil.wrapper_serialize(matrix2);
    vector3_ptr=0
    if vector3!=0 and vector3!=None: 
      vector3_ptr=wasmutil.wrapper_serialize(vector3);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:weightedRegressOutImageWASM\n++++');

    Module.weightedRegressOutImageWASM.argtypes=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int];
    Module.weightedRegressOutImageWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.weightedRegressOutImageWASM(image1_ptr, matrix2_ptr, vector3_ptr, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Regress out global signal from a  time series (with optional weights)
#* @param input_ptr the input timeseries matrix (roi output, rows=frames);
#* @param weights_ptr the input weight vector ( rows=frames) or 0 ;
#* @param debug if > 0 print debug messages
#* @returns a pointer to the filtered matrix (rows=frames,cols=rois)
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'weightedRegressGlobalSignalWASM', 'Matrix', [ 'Matrix', 'Vector_opt',  'debug' ]}
#      returns a Matrix
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def weightedRegressGlobalSignalWASM(matrix1,vector2,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;


    # Serialize objects and encode strings
    matrix1_ptr=wasmutil.wrapper_serialize(matrix1);
    vector2_ptr=0
    if vector2!=0 and vector2!=None: 
      vector2_ptr=wasmutil.wrapper_serialize(vector2);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:weightedRegressGlobalSignalWASM\n++++');

    Module.weightedRegressGlobalSignalWASM.argtypes=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int];
    Module.weightedRegressGlobalSignalWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.weightedRegressGlobalSignalWASM(matrix1_ptr, vector2_ptr, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'Matrix');
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Compute Seed map correlation image
#* @param input_ptr the input image
#* @param roi_ptr the input roi timeseries matrix (roi output, rows=frames) (the seed timecourses)
#* @param weights_ptr the input weight vector ( rows=frames) or 0 ;
#* @param jsonstring the parameters { "zscore": "false" }
#* @param debug if > 0 print debug messages
#* @returns a pointer to the seed map image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'computeSeedCorrelationImageWASM', 'bisImage', [ 'bisImage', 'Matrix', 'Vector_opt',  'ParamObj', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def computeSeedCorrelationImageWASM(image1,matrix2,vector3,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);
    matrix2_ptr=wasmutil.wrapper_serialize(matrix2);
    vector3_ptr=0
    if vector3!=0 and vector3!=None: 
      vector3_ptr=wasmutil.wrapper_serialize(vector3);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:computeSeedCorrelationImageWASM with ',jsonstring,'\n++++');

    Module.computeSeedCorrelationImageWASM.argtypes=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.computeSeedCorrelationImageWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.computeSeedCorrelationImageWASM(image1_ptr, matrix2_ptr, vector3_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** AddGridTo an image using \link bisAdvancedImageAlgorithms::addGridToImage \endlink
#* @param input serialized input as unsigned char array
#* @param jsonstring the parameter string for the algorithm
#* { "gap" : 8, "value" 2.0 }
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'addGridToImageWASM', 'bisImage', [ 'bisImage', 'ParamObj', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def addGridToImageWASM(image1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:addGridToImageWASM with ',jsonstring,'\n++++');

    Module.addGridToImageWASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.addGridToImageWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.addGridToImageWASM(image1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Project a 3D image to 2D either mip or average or shaded average
#* @param input serialized input as unsigned char array
#* @param functional_input serialized functional input (optional) as unsigned char array
#* @param jsonstring the parameter string for the algorithm
#* { "domip" : 1: ,"axis" : -1, "flip" : 0, "sigma" : 1.0: 'threshold' : 0.05, 'gradsigma' : 1.0, 'windowsize': 5 }
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'projectImageWASM', 'bisImage', [ 'bisImage', 'bisImage_opt', 'ParamObj', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def projectImageWASM(image1,image2,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);
    image2_ptr=0
    if image2!=0 and image2!=None: 
      image2_ptr=wasmutil.wrapper_serialize(image2);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:projectImageWASM with ',jsonstring,'\n++++');

    Module.projectImageWASM.argtypes=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.projectImageWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.projectImageWASM(image1_ptr, image2_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Back Projects a 2D image to a 3D image
#* @param input serialized input as unsigned char array   (3D image)
#* @param input2d serialized input as unsigned char array  (2D image)
#* @param jsonstring the parameter string for the algorithm
#* { "axis" : -1, "flip" : 0,  'threshold' : 0.05,  'windowsize': 5 }
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'backProjectImageWASM', 'bisImage', [ 'bisImage', 'bisImage', 'ParamObj', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def backProjectImageWASM(image1,image2,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);
    image2_ptr=wasmutil.wrapper_serialize(image2);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:backProjectImageWASM with ',jsonstring,'\n++++');

    Module.backProjectImageWASM.argtypes=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.backProjectImageWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.backProjectImageWASM(image1_ptr, image2_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Returns 1701 (Yale's first year) if in webassembly or 1700 if in C (for Python, Matlab etc.) */
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'test_wasm', 'Int'}
#      returns a Int
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def test_wasm(debug=False):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;


    # Call WASM
    if debug:
        print('++++ Calling WASM Function:test_wasm\n++++');

    Module.test_wasm.argtypes=[];
    Module.test_wasm.restype=ctypes.c_int;

    output=Module.test_wasm();
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Redirects stdout fo a file -- used for debugging and testing
#* @param fname filename to save in (defaults to bislog.txt in current directory)
#* returns 1 if file opened OK
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'redirect_stdout', 'Int', [ 'String' ]}
#      returns a Int
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def redirect_stdout(string1,debug=False):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;


    # Serialize objects and encode strings
    string1_binstr=str.encode(string1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:redirect_stdout\n++++');

    Module.redirect_stdout.argtypes=[ctypes.c_char_p];
    Module.redirect_stdout.restype=ctypes.c_int;

    output=Module.redirect_stdout(string1_binstr);
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Tests serialization of 4x4 matrix in and out
#* Expects  matrix[row][col] = (1+row)*10.0+col*col*5.0
#* @param ptr serialized 4x4 transformation as unsigned char array
#* @param debug if > 0 print debug messages
#* @returns difference between expected and received matrix as a single float
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'test_matrix4x4', 'Float', [ 'bisLinearTransformation', 'debug']}
#      returns a Float
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def test_matrix4x4(linearxform1,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;


    # Serialize objects and encode strings
    linearxform1_ptr=wasmutil.wrapper_serialize(linearxform1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:test_matrix4x4\n++++');

    Module.test_matrix4x4.argtypes=[ctypes.c_void_p, ctypes.c_int];
    Module.test_matrix4x4.restype=ctypes.c_float;

    output=Module.test_matrix4x4(linearxform1_ptr, debug);
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Create 4x4 Matrix from param vector and two images
#* @param image1_ptr serialized  image1 as unsigned char array
#* @param image2_ptr serialized  image2 as unsigned char array
#* @param pvector_ptr the transformation parameters see \link bisLinearTransformation.setParameterVector \endlink
#* @param jsonstring algorithm parameters  { mode: 2 }
#* @param debug if > 0 print debug messages
#* @returns matrix 4x4 as a serialized array
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'test_create_4x4matrix', 'bisLinearTransformation', [ 'bisImage', 'bisImage', 'Vector' , 'ParamObj', 'debug']}
#      returns a bisLinearTransformation
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def test_create_4x4matrix(image1,image2,vector3,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);
    image2_ptr=wasmutil.wrapper_serialize(image2);
    vector3_ptr=wasmutil.wrapper_serialize(vector3);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:test_create_4x4matrix with ',jsonstring,'\n++++');

    Module.test_create_4x4matrix.argtypes=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.test_create_4x4matrix.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.test_create_4x4matrix(image1_ptr, image2_ptr, vector3_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisLinearTransformation');
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Tests Eigen operations
#* @param m_ptr serialized 4x4 transformation as unsigned char array
#*     where matrix[row][col] = (1+row)*10.0+col*col*5.0 as input for initital test
#* @param v_ptr serialized 6 vector as unsigned char array [ 1,2,3,5,7,11 ]
#* @param debug if > 0 print debug messages
#* @returns number of failed tests (0=pass, -1 -> deserializing failed)
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'test_eigenUtils', 'Int', [ 'bisLinearTransformation', 'Vector', 'debug']}
#      returns a Int
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def test_eigenUtils(linearxform1,vector2,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;


    # Serialize objects and encode strings
    linearxform1_ptr=wasmutil.wrapper_serialize(linearxform1);
    vector2_ptr=wasmutil.wrapper_serialize(vector2);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:test_eigenUtils\n++++');

    Module.test_eigenUtils.argtypes=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int];
    Module.test_eigenUtils.restype=ctypes.c_int;

    output=Module.test_eigenUtils(linearxform1_ptr, vector2_ptr, debug);
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Tests Matlab read
#* @param f_ptr serialized byte vector whose payload are the raw bytes from a .mat file
#* @param m_ptr serialized matrix (one of those in the .mat file)
#* @param name name of matrix to look for
#* @param debug if > 0 print debug messages
#* @returns max abs difference between matrices
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'test_matlabParse', 'Float', [ 'Vector', 'Matrix', 'String', 'debug']}
#      returns a Float
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def test_matlabParse(vector1,matrix2,string3,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;


    # Serialize objects and encode strings
    vector1_ptr=wasmutil.wrapper_serialize(vector1);
    matrix2_ptr=wasmutil.wrapper_serialize(matrix2);
    string3_binstr=str.encode(string3);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:test_matlabParse\n++++');

    Module.test_matlabParse.argtypes=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.test_matlabParse.restype=ctypes.c_float;

    output=Module.test_matlabParse(vector1_ptr, matrix2_ptr, string3_binstr, debug);
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Tests Bending Energy
#* @param ptr serialized Combo Transformation with 1 grid
#* @param debug if > 0 print debug messages
#* @returns num failed tests
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'test_bendingEnergy', 'Int', [ 'bisComboTransformation','debug']}
#      returns a Int
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def test_bendingEnergy(comboxform1,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;


    # Serialize objects and encode strings
    comboxform1_ptr=wasmutil.wrapper_serialize(comboxform1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:test_bendingEnergy\n++++');

    Module.test_bendingEnergy.argtypes=[ctypes.c_void_p, ctypes.c_int];
    Module.test_bendingEnergy.restype=ctypes.c_int;

    output=Module.test_bendingEnergy(comboxform1_ptr, debug);
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Tests PTZ Conversions i.e. p->t, t->p p->z, z->p
#* @param debug if > 0 print debug messages
#* @returns num failed tests
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'test_PTZConversions', 'Int', [ 'debug']}
#      returns a Int
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def test_PTZConversions(debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;


    # Call WASM
    if debug:
        print('++++ Calling WASM Function:test_PTZConversions\n++++');

    Module.test_PTZConversions.argtypes=[ctypes.c_int];
    Module.test_PTZConversions.restype=ctypes.c_int;

    output=Module.test_PTZConversions(debug);
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Tests In Place Matrix Multiplication in bisEigenUtil
#* @param debug if > 0 print debug messages
#* @returns num failed tests
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'test_eigenUtilOperations', 'Int', [ 'debug']}
#      returns a Int
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def test_eigenUtilOperations(debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;


    # Call WASM
    if debug:
        print('++++ Calling WASM Function:test_eigenUtilOperations\n++++');

    Module.test_eigenUtilOperations.argtypes=[ctypes.c_int];
    Module.test_eigenUtilOperations.restype=ctypes.c_int;

    output=Module.test_eigenUtilOperations(debug);
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Mirror text file  first parse then recreated
#* @param input the input text file (from a .grd file)
#* @param debug if >0 print debug messages
#* @returns the recreated text file
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'test_mirrorComboTransformTextFileWASM', 'String', [ 'String', 'debug']}
#      returns a String
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def test_mirrorComboTransformTextFileWASM(string1,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;


    # Serialize objects and encode strings
    string1_binstr=str.encode(string1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:test_mirrorComboTransformTextFileWASM\n++++');

    Module.test_mirrorComboTransformTextFileWASM.argtypes=[ctypes.c_char_p, ctypes.c_int];
    Module.test_mirrorComboTransformTextFileWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.test_mirrorComboTransformTextFileWASM(string1_binstr, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'String');
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Compute Joint Histogram Metrics
#* @param image1_ptr serialized  image1 as unsigned char array
#* @param image2_ptr serialized  image2 as unsigned char array
#* @param weight1_ptr serialized  weight 1 as unsigned char array
#* @param weight2_ptr serialized  weight 2 as unsigned char array
#* @param num_weights number of weights to use (0=none, 1=only weight1_ptr, 2=both)
#* @param jsonstring algorithm parameters  { numbinsx: 64, numbinst: 64, intscale:1 }
#* @param return_histogram if 1 return the actual histogram else the metrics
#* @param debug if > 0 print debug messages
#* @returns if return_histogram =1 the histogram as a matrix, else a single row matrix consisting of
#*  [ SSD, CC, NMI, MI, EntropyX, Entropy, jointEntropy, numSamples ] both as serialized arrays
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'test_compute_histo_metric', 'Matrix', [ 'bisImage', 'bisImage','bisImage_opt', 'bisImage_opt', 'Int', 'ParamObj','Int','debug'}
#      returns a Matrix
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def test_compute_histo_metric(image1,image2,image3,image4,intval5,paramobj,intval7,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);
    image2_ptr=wasmutil.wrapper_serialize(image2);
    image3_ptr=0
    if image3!=0 and image3!=None: 
      image3_ptr=wasmutil.wrapper_serialize(image3);
    image4_ptr=0
    if image4!=0 and image4!=None: 
      image4_ptr=wasmutil.wrapper_serialize(image4);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:test_compute_histo_metric with ',jsonstring,'\n++++');

    Module.test_compute_histo_metric.argtypes=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int];
    Module.test_compute_histo_metric.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.test_compute_histo_metric(image1_ptr, image2_ptr, image3_ptr, image4_ptr, intval5, jsonstring, intval7, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'Matrix');
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Individualizes a group parcellation using a new 4D fmri Image
#* @param input serialized 4D input file as unsigned char array
#* @param groupparcellation serialized input (group) parcellation as unsigned char array
#* @param jsonstring the parameter string for the algorithm
#* { "numberorexemplars" : 268, "smooth" : 4}
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'individualizedParcellationWASM', 'bisImage', [ 'bisImage', 'bisImage', 'ParamObj', 'debug' ], {"checkorientation" : "all"}}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def individualizedParcellationWASM(image1,image2,paramobj,debug=0):

    Module=wasmutil.Module();

    if (image1.hasSameOrientation(image2,'image1','image2',True)==False):
       return False;

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);
    image2_ptr=wasmutil.wrapper_serialize(image2);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:individualizedParcellationWASM with ',jsonstring,'\n++++');

    Module.individualizedParcellationWASM.argtypes=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.individualizedParcellationWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.individualizedParcellationWASM(image1_ptr, image2_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Returns 1*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'uses_gpl', 'Int'}
#      returns a Int
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def uses_gpl(debug=False):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;


    # Call WASM
    if debug:
        print('++++ Calling WASM Function:uses_gpl\n++++');

    Module.uses_gpl.argtypes=[];
    Module.uses_gpl.restype=ctypes.c_int;

    output=Module.uses_gpl();
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** run Linear Image Registration using \link bisLinearImageRegistration  \endlink
#* @param reference serialized reference image as unsigned char array
#* @param target    serialized target image as unsigned char array
#* @param initial_xform serialized initial transformation as unsigned char array
#* @param jsonstring the parameter string for the algorithm including return_vector which if true returns a length-28 vector
#* containing the 4x4 matrix and the 12 transformation parameters
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized vector or matrix depending on the value of return_vector
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'runLinearRegistrationWASM', 'bisLinearTransformation', [ 'bisImage', 'bisImage', 'bisLinearTransformation_opt', 'ParamObj', 'debug' ]}
#      returns a bisLinearTransformation
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def runLinearRegistrationWASM(image1,image2,linearxform3,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);
    image2_ptr=wasmutil.wrapper_serialize(image2);
    linearxform3_ptr=0
    if linearxform3!=0 and linearxform3!=None: 
      linearxform3_ptr=wasmutil.wrapper_serialize(linearxform3);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:runLinearRegistrationWASM with ',jsonstring,'\n++++');

    Module.runLinearRegistrationWASM.argtypes=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.runLinearRegistrationWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.runLinearRegistrationWASM(image1_ptr, image2_ptr, linearxform3_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisLinearTransformation');
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** run Non Linear Image Registration using \link bisNonLinearImageRegistration  \endlink
#* @param reference serialized reference image as unsigned char array
#* @param target    serialized target image as unsigned char array
#* @param initial_xform serialized initial transformation as unsigned char array
#* @param jsonstring the parameter string for the algorithm
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized combo transformation (bisComboTransformation)
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'runNonLinearRegistrationWASM', 'bisComboTransformation', [ 'bisImage', 'bisImage', 'bisLinearTransformation_opt', 'ParamObj', 'debug' ]}
#      returns a bisComboTransformation
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def runNonLinearRegistrationWASM(image1,image2,linearxform3,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);
    image2_ptr=wasmutil.wrapper_serialize(image2);
    linearxform3_ptr=0
    if linearxform3!=0 and linearxform3!=None: 
      linearxform3_ptr=wasmutil.wrapper_serialize(linearxform3);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:runNonLinearRegistrationWASM with ',jsonstring,'\n++++');

    Module.runNonLinearRegistrationWASM.argtypes=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.runNonLinearRegistrationWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.runNonLinearRegistrationWASM(image1_ptr, image2_ptr, linearxform3_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisComboTransformation');
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Approximate Displacement Field with Grid Transformation (pre initialized)
#* @param dispfield serialized target displacement field
#* @param initial_grid serialized grid transformation as unsigned char array
#* @param jsonstring the parameter string for the algorithm
#* @param debug if > 0 print debug messages
#* @returns a pointer to the updated grid (bisGridTransformation)
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'approximateDisplacementFieldWASM', 'bisGridTransformation', [ 'bisImage', 'bisGridTransformation', 'ParamObj', 'debug' ]}
#      returns a bisGridTransformation
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def approximateDisplacementFieldWASM(image1,gridxform2,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);
    gridxform2_ptr=wasmutil.wrapper_serialize(gridxform2);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:approximateDisplacementFieldWASM with ',jsonstring,'\n++++');

    Module.approximateDisplacementFieldWASM.argtypes=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.approximateDisplacementFieldWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.approximateDisplacementFieldWASM(image1_ptr, gridxform2_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisGridTransformation');
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Approximate Displacement Field with Grid Transformation -- initialized using the sapcing parameter
#* @param dispfield serialized target displacement field
#* @param jsonstring the parameter string for the algorithm  -- key is spacing : --> this defines the spacing for the grid transformation
#* @param debug if > 0 print debug messages
#* @returns a pointer to the updated grid (bisGridTransformation)
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'approximateDisplacementFieldWASM2', 'bisGridTransformation', [ 'bisImage', 'ParamObj', 'debug' ]}
#      returns a bisGridTransformation
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def approximateDisplacementFieldWASM2(image1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:approximateDisplacementFieldWASM2 with ',jsonstring,'\n++++');

    Module.approximateDisplacementFieldWASM2.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.approximateDisplacementFieldWASM2.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.approximateDisplacementFieldWASM2(image1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisGridTransformation');
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Perform image segmentation either histogram based or plus mrf segmentation if smoothness > 0.0
#* @param input serialized input as unsigned char array
#* @param jsonstring the parameter string for the algorithm { "numclasses" : 3, "maxsigmaratio":0.2, "robust" : true, "numbins": 256, "smoothhisto": true, "smoothness" : 0.0, "mrfconvergence" : 0.2, "mrfiterations" : 8, "noisesigma2" : 0.0 }
#* @param debug if > 0 print debug messages
#* @returns a pointer to a serialized segmented image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'segmentImageWASM', 'bisImage', [ 'bisImage', 'ParamObj', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def segmentImageWASM(image1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:segmentImageWASM with ',jsonstring,'\n++++');

    Module.segmentImageWASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.segmentImageWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.segmentImageWASM(image1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Perform objectmap regularization
#* @param input serialized input as unsigned char array
#* @param jsonstring the parameter string for the algorithm { "smoothness" : 2.0, "convergence" : 0.2, "terations" : 8, "internaliterations" : 4 }
#* @param debug if > 0 print debug messages
#* @returns a pointer to a (short) serialized segmented image
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'regularizeObjectmapWASM', 'bisImage', [ 'bisImage', 'ParamObj', 'debug' ]}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def regularizeObjectmapWASM(image1,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:regularizeObjectmapWASM with ',jsonstring,'\n++++');

    Module.regularizeObjectmapWASM.argtypes=[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.regularizeObjectmapWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.regularizeObjectmapWASM(image1_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Tests Optimizer with numdof = 1 or 2 and all three modes
#* @param numdof number of degrees of freedom for simple quadratic function (1 or 2)
#* @returns number of failed tests
#*/
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'test_optimizer', 'Int', [ 'Int']}
#      returns a Int
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def test_optimizer(intval1,debug=False):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;


    # Call WASM
    if debug:
        print('++++ Calling WASM Function:test_optimizer\n++++');

    Module.test_optimizer.argtypes=[ctypes.c_int];
    Module.test_optimizer.restype=ctypes.c_int;

    output=Module.test_optimizer(intval1);
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Compute DTI Tensor
#* @param input_ptr the images as a serialized array
#* @param baseline_ptr the "Baseline" T2 Image as a serialized array
#* @param mask_ptr the Mask Image (optional, set this to 0) as a serialized array
#* @param directions_ptr the directions matrix
#* @param jsonstring { "bvalue": 1000, "numbaseline:" 1 }
#* @param debug if > 0 print debug messages
#* @returns a pointer to the tensor image */
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'computeDTITensorFitWASM', 'bisImage', [ 'bisImage', 'bisImage',  'bisImage_opt' ,'Matrix', 'ParamObj', 'debug']}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def computeDTITensorFitWASM(image1,image2,image3,matrix4,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);
    image2_ptr=wasmutil.wrapper_serialize(image2);
    image3_ptr=0
    if image3!=0 and image3!=None: 
      image3_ptr=wasmutil.wrapper_serialize(image3);
    matrix4_ptr=wasmutil.wrapper_serialize(matrix4);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:computeDTITensorFitWASM with ',jsonstring,'\n++++');

    Module.computeDTITensorFitWASM.argtypes=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.computeDTITensorFitWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.computeDTITensorFitWASM(image1_ptr, image2_ptr, image3_ptr, matrix4_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Compute DTI Tensor EigenSystem
#* @param input_ptr the image tensor as a serialized array
#* @param mask_ptr the Mask Image (optional, set this to 0) as a serialized array
#* @param debug if > 0 print debug messages
#* @returns a pointer to the eigensystem image */
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'computeTensorEigenSystemWASM', 'bisImage', [ 'bisImage', 'bisImage_opt' , 'debug']}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def computeTensorEigenSystemWASM(image1,image2,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;


    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);
    image2_ptr=0
    if image2!=0 and image2!=None: 
      image2_ptr=wasmutil.wrapper_serialize(image2);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:computeTensorEigenSystemWASM\n++++');

    Module.computeTensorEigenSystemWASM.argtypes=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int];
    Module.computeTensorEigenSystemWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.computeTensorEigenSystemWASM(image1_ptr, image2_ptr, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Compute DTI Tensor Invariants
#* @param input_ptr the image tensor eigensystem as a serialized array
#* @param mask_ptr the Mask Image (optional, set this to 0) as a serialized array
#* @param jsonstring { "mode": 0 } // mode 0=FA, 1=RA etc. -- see bisDTIAlgorithms::computeTensorInvariants
#* @param debug if > 0 print debug messages
#* @returns a pointer to the invarient image */
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'computeDTITensorInvariantsWASM', 'bisImage', [ 'bisImage', 'bisImage_opt' , 'ParamObj', 'debug']}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def computeDTITensorInvariantsWASM(image1,image2,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);
    image2_ptr=0
    if image2!=0 and image2!=None: 
      image2_ptr=wasmutil.wrapper_serialize(image2);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:computeDTITensorInvariantsWASM with ',jsonstring,'\n++++');

    Module.computeDTITensorInvariantsWASM.argtypes=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.computeDTITensorInvariantsWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.computeDTITensorInvariantsWASM(image1_ptr, image2_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


#--------------------------------------------------------------
# C++:
#/** Compute DTI Orientation Map
#* @param input_ptr the image tensor eigensystem as a serialized array
#* @param mask_ptr the Mask Image (optional, set this to 0) as a serialized array
#* @param magnitude_ptr the Magnitude Image (e.g. FA map) (optional, set this to 0) as a serialized array
#* @param jsonstring { "scaling": 1.0 } Optional extra scaling
#* @param debug if > 0 print debug messages
#* @returns a pointer to the colormap image */
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# JS: {'computeDTIColorMapImageWASM', 'bisImage', [ 'bisImage', 'bisImage_opt' ,'bisImage_opt', 'ParamObj', 'debug']}
#      returns a bisImage
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def computeDTIColorMapImageWASM(image1,image2,image3,paramobj,debug=0):

    Module=wasmutil.Module();

    if debug!=True and debug!=1 and debug!=2:
        debug=0;
    elif debug!=2:
        debug=1;

    jsonstring_0=json.dumps(paramobj);
    jsonstring=str.encode(json.dumps(paramobj));

    # Serialize objects and encode strings
    image1_ptr=wasmutil.wrapper_serialize(image1);
    image2_ptr=0
    if image2!=0 and image2!=None: 
      image2_ptr=wasmutil.wrapper_serialize(image2);
    image3_ptr=0
    if image3!=0 and image3!=None: 
      image3_ptr=wasmutil.wrapper_serialize(image3);

    # Call WASM
    if debug:
        print('++++ Calling WASM Function:computeDTIColorMapImageWASM with ',jsonstring,'\n++++');

    Module.computeDTIColorMapImageWASM.argtypes=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int];
    Module.computeDTIColorMapImageWASM.restype=ctypes.POINTER(ctypes.c_ubyte);

    wasm_output=Module.computeDTIColorMapImageWASM(image1_ptr, image2_ptr, image3_ptr, jsonstring, debug);

    # Deserialize Output
    output=wasmutil.wrapper_deserialize_and_delete(wasm_output,'bisImage',image1);
    
    # Return
    return output;


initialize_module();
