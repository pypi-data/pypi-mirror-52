descriptions = {
    "approximateField": {
        "name": "Approximate Displacement Field",
        "description": "Calculates the displacement field for a given transformation for a given image.",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "Load the displacement field image to approximate",
                "varname": "input",
                "shortname": "i",
                "required": True
            }
        ],
        "params": [
            {
                "name": "Smoothness",
                "description": "Extra regularization smoothness term weight",
                "type": "float",
                "varname": "lambda",
                "default": 0.1,
                "low": 0,
                "high": 1
            },
            {
                "name": "Tolerance",
                "description": "Fitting to tolerance",
                "type": "float",
                "varname": "tolerance",
                "default": 0.001
            },
            {
                "name": "Window Size",
                "description": "Fitting quality",
                "type": "float",
                "varname": "windowsize",
                "low": 1,
                "high": 2,
                "default": 2
            },
            {
                "name": "Inverse",
                "description": "if True approximate inverse displacement field",
                "type": "boolean",
                "varname": "inverse",
                "default": False
            },
            {
                "name": "Spacing",
                "description": "The control point spacing of the output grid transform",
                "type": "float",
                "varname": "spacing",
                "low": 2,
                "high": 50,
                "default": 25
            },
            {
                "name": "Optimization",
                "description": "Optimization Method",
                "type": "string",
                "fields": [
                    "HillClimb",
                    "GradientDescent",
                    "ConjugateGradient"
                ],
                "restrictAnswer": [
                    "HillClimb",
                    "GradientDescent",
                    "ConjugateGradient"
                ],
                "varname": "optimization",
                "default": "ConjugateGradient"
            },
            {
                "name": "Step Size",
                "description": "Step size for gradient computation",
                "type": "float",
                "varname": "stepsize",
                "default": 0.5,
                "low": 0.125,
                "high": 4
            },
            {
                "name": "Levels",
                "description": "Number of levels in multiresolution optimization",
                "default": 2,
                "type": "int",
                "varname": "levels",
                "low": 1,
                "high": 4
            },
            {
                "name": "Iterations",
                "description": "Number of iterations (per level and step)",
                "type": "int",
                "varname": "iterations",
                "low": 1,
                "high": 32,
                "default": 20
            },
            {
                "name": "Resolution",
                "description": "Factor to reduce the resolution prior to registration",
                "type": "float",
                "varname": "resolution",
                "default": 2,
                "low": 1,
                "high": 5,
                "step": 0.25
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            },
            {
                "name": "Steps",
                "description": "Number of steps in multiresolution optimization",
                "type": "int",
                "varname": "steps",
                "default": 1,
                "low": 1,
                "high": 4
            }
        ],
        "outputs": [
            {
                "type": "transform",
                "name": "Output Grid Transformation",
                "description": "Stores the fitted transformation to the input displacement field",
                "varname": "output",
                "required": True,
                "shortname": "o"
            }
        ]
    },
    "blankImage": {
        "name": "Blank Image",
        "description": "This algorithm performs image blanking, i.e. zeros values outside the specified region. It is similar to crop but maintains the original image dimensions.",
        "author": "Xenios Papdemetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "The image to be processed",
                "varname": "input",
                "shortname": "i",
                "required": True
            }
        ],
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "Save the output image",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "params": [
            {
                "name": "I-Start",
                "description": "The Start along the i axis.",
                "varname": "i0",
                "type": "int",
                "default": -1
            },
            {
                "name": "I-End",
                "description": "The End along the i axis.",
                "varname": "i1",
                "type": "int",
                "default": 10001
            },
            {
                "name": "J-Start",
                "description": "The Start along the j axis.",
                "varname": "j0",
                "type": "int",
                "default": -1
            },
            {
                "name": "J-End",
                "description": "The End along the j axis.",
                "varname": "j1",
                "type": "int",
                "default": 10001
            },
            {
                "name": "K-Start",
                "description": "The Start along the k axis.",
                "varname": "k0",
                "type": "int",
                "default": -1
            },
            {
                "name": "K-End",
                "description": "The End along the k axis.",
                "varname": "k1",
                "type": "int",
                "default": 10001
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "butterworthFilter": {
        "name": "Butterworth Filter",
        "description": "This element will apply a Butterworth Filter to an input matrix",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "matrix",
                "name": "Matrix",
                "description": "The input data (matrix) to process. Rows=Frames, Columns=Series.",
                "varname": "input",
                "shortname": "i",
                "required": True
            }
        ],
        "outputs": [
            {
                "type": "matrix",
                "name": "Output Matrix",
                "description": "The output matrix",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".matr"
            }
        ],
        "params": [
            {
                "name": "Type",
                "description": "What type of filter to apply (low, band, or high)",
                "type": "string",
                "varname": "type",
                "fields": [
                    "low",
                    "band",
                    "high"
                ],
                "restrictAnswer": [
                    "low",
                    "band",
                    "high"
                ],
                "default": "band"
            },
            {
                "name": "Low Frequency",
                "description": "Lowpass cutoff frequency of filter (in Hertz)",
                "type": "float",
                "varname": "low",
                "low": 0,
                "high": 10,
                "default": 0.1
            },
            {
                "name": "High Frequency",
                "description": "Highpass cutoff frequency of filter (in Hertz)",
                "type": "float",
                "varname": "high",
                "low": 0,
                "high": 10,
                "default": 0.01
            },
            {
                "name": "Sample Rate",
                "description": "Data time of repetition (Data TR)",
                "type": "float",
                "varname": "tr",
                "default": 1,
                "low": 0.01,
                "high": 5
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "butterworthFilterImage": {
        "name": "Butterworth Filter Image",
        "description": "This module performs temporal Butterworth filtering to an input image. This is performed separately for each voxel",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "The image to be processed",
                "varname": "input",
                "shortname": "i",
                "required": True
            }
        ],
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "Save the output image",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "slicer": True,
        "params": [
            {
                "name": "Type",
                "description": "What type of filter to apply (low, band, or high)",
                "type": "string",
                "varname": "type",
                "fields": [
                    "low",
                    "band",
                    "high"
                ],
                "restrictAnswer": [
                    "low",
                    "band",
                    "high"
                ],
                "default": "band"
            },
            {
                "name": "Low Frequency",
                "description": "Lowpass cutoff frequency of filter (in Hertz)",
                "type": "float",
                "varname": "low",
                "low": 0,
                "high": 10,
                "default": 0.1
            },
            {
                "name": "High Frequency",
                "description": "Highpass cutoff frequency of filter (in Hertz)",
                "type": "float",
                "varname": "high",
                "low": 0,
                "high": 10,
                "default": 0.01
            },
            {
                "name": "Sample Rate (TR)",
                "description": "Data time of repetition (Data TR). If <0.0 use spacing from image header",
                "type": "float",
                "varname": "tr",
                "default": -1,
                "low": -1,
                "high": 5
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "changeImageSpacing": {
        "name": "Change Image Spacing",
        "description": "Changes the image header to have new spacing",
        "author": "Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "The image to be processed",
                "varname": "input",
                "shortname": "i",
                "required": True
            }
        ],
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "Save the output image",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "params": [
            {
                "name": "X Spacing",
                "description": "Desired voxel spacing in X direction",
                "type": "float",
                "varname": "xsp",
                "default": 1,
                "low": 0.1,
                "high": 10,
                "step": 0.1
            },
            {
                "name": "Y Spacing",
                "description": "Desired voxel spacing in Y direction",
                "type": "float",
                "varname": "ysp",
                "default": 1,
                "low": 0.1,
                "high": 10,
                "step": 0.1
            },
            {
                "name": "Z Spacing",
                "description": "Desired voxel spacing in the z-direction",
                "varname": "zsp",
                "default": 1,
                "type": "float",
                "low": 0.1,
                "high": 10,
                "step": 0.1
            }
        ]
    },
    "clusterThreshold": {
        "name": "Cluster Threshold",
        "description": "This element will separate an image into clusters and apply binary thresholding. The image is first thresholded using a threshold. Then it is filtered to remove binary blobs that smaller than the cluster size selected.",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "The image to be processed",
                "varname": "input",
                "shortname": "i",
                "required": True
            }
        ],
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "The output image",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "slicer": True,
        "params": [
            {
                "name": "Threshold",
                "description": "The value to threshold at (zero out voxels below threshold)",
                "type": "float",
                "varname": "threshold",
                "default": 1
            },
            {
                "name": "Cluster Size",
                "description": "Size of clusters to form",
                "type": "int",
                "varname": "size",
                "default": 1000,
                "low": 10,
                "high": 10000
            },
            {
                "name": "One Connected",
                "description": "Whether to use 6 or 26 neighbors",
                "type": "bool",
                "varname": "oneconnected",
                "default": True
            },
            {
                "name": "Frame",
                "description": "Which frame from the time series to cluster (fourth dimension)",
                "type": "int",
                "varname": "frame",
                "default": 0
            },
            {
                "name": "Component",
                "description": "Which component to take a frame from (fifth dimension)",
                "type": "int",
                "varname": "component",
                "default": 0
            },
            {
                "name": "OutputClusterNo",
                "description": "It True the output image is filled with the cluster number instead of the actual image values",
                "varname": "outclustno",
                "type": "boolean",
                "default": False
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "computeCorrelation": {
        "name": "Compute Correlation",
        "description": "Computes the correlation matrix for an input matrix (pairwise) with weights",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "matrix",
                "name": "Matrix",
                "description": "The input data (matrix) to process. Rows=Frames, Columns=Series.",
                "varname": "input",
                "shortname": "i",
                "required": True
            },
            {
                "type": "vector",
                "name": "Weights",
                "description": "(Optional). The framewise weight vector",
                "varname": "weight",
                "shortname": "w",
                "required": False
            }
        ],
        "outputs": [
            {
                "type": "matrix",
                "name": "Output Matrix",
                "description": "The output matrix",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".matr"
            }
        ],
        "params": [
            {
                "name": "Z-Score",
                "description": "Convert correlations to z-score.",
                "type": "boolean",
                "varname": "zscore",
                "default": True
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "computeGLM": {
        "name": "Compute GLM",
        "description": "Calculates the Generalized linear model (GLM) for fMRI data sets",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "Output beta map image",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "params": [
            {
                "name": "Num Tasks",
                "description": "How many of the actual columns in the regressor are actual tasks -- if 0 then all.",
                "type": "int",
                "varname": "numtasks",
                "default": 0,
                "low": 0,
                "high": 20
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ],
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "Load the image to fit the model to",
                "varname": "input",
                "shortname": "i",
                "required": True
            },
            {
                "type": "matrix",
                "name": " Regressor",
                "description": "The regressor matrix",
                "varname": "regressor",
                "shortname": "r"
            },
            {
                "type": "image",
                "name": "Load Mask Image",
                "description": "Load the mask for the input",
                "varname": "mask",
                "required": False
            }
        ]
    },
    "computeROI": {
        "name": "Compute ROI",
        "description": "Takes an input time series and ROI map and returns the mean intensity in the roi as a matrix of frames(rows)*roiindex(columns)",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "Load the image (time series) to be averaged into regions",
                "varname": "input",
                "shortname": "i",
                "required": True
            },
            {
                "type": "image",
                "name": "Load Regions of Interest",
                "description": "parcellation/regions of interest to compute signal averages for",
                "varname": "roi",
                "shortname": "r"
            }
        ],
        "outputs": [
            {
                "type": "matrix",
                "name": "Output Matrix",
                "description": "The output matrix",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".matr"
            }
        ],
        "params": [
            {
                "name": "Store Centroids?",
                "description": "If True store the centroid of each roi as last three columns",
                "varname": "storecentroids",
                "type": "boolean",
                "default": False
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "cropImage": {
        "name": "Crop",
        "description": "This algorithm performs image cropping in 4 dimensions. Step refers to the sample rate, e.g. step=2 means every second voxel.",
        "author": "Xenios Papdemetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "The image to be processed",
                "varname": "input",
                "shortname": "i",
                "required": True
            }
        ],
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "Save the output image",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "slicer": True,
        "params": [
            {
                "name": "I-Start",
                "description": "The Start along the i axis.",
                "varname": "i0",
                "type": "int",
                "default": 0,
                "low": -10,
                "high": 200
            },
            {
                "name": "I-End",
                "description": "The End along the i axis.",
                "varname": "i1",
                "type": "int",
                "default": 10,
                "low": -10,
                "high": 200
            },
            {
                "name": "I-Step",
                "description": "The Step along the i axis.",
                "varname": "di",
                "type": "int",
                "default": 1,
                "low": -10,
                "high": 200
            },
            {
                "name": "J-Start",
                "description": "The Start along the j axis.",
                "varname": "j0",
                "type": "int",
                "default": 0,
                "low": -10,
                "high": 200
            },
            {
                "name": "J-End",
                "description": "The End along the j axis.",
                "varname": "j1",
                "type": "int",
                "default": 10,
                "low": -10,
                "high": 200
            },
            {
                "name": "J-Step",
                "description": "The Step along the j axis.",
                "varname": "dj",
                "type": "int",
                "default": 1,
                "low": -10,
                "high": 200
            },
            {
                "name": "K-Start",
                "description": "The Start along the k axis.",
                "varname": "k0",
                "type": "int",
                "default": 0,
                "low": -10,
                "high": 200
            },
            {
                "name": "K-End",
                "description": "The End along the k axis.",
                "varname": "k1",
                "type": "int",
                "default": 10,
                "low": -10,
                "high": 200
            },
            {
                "name": "K-Step",
                "description": "The Step along the k axis.",
                "varname": "dk",
                "type": "int",
                "default": 1,
                "low": -10,
                "high": 200
            },
            {
                "name": "T-Start",
                "description": "The Start along the t axis.",
                "varname": "t0",
                "type": "int",
                "default": 0,
                "low": -10,
                "high": 200
            },
            {
                "name": "T-End",
                "description": "The End along the t axis.",
                "varname": "t1",
                "type": "int",
                "default": 10,
                "low": -10,
                "high": 200
            },
            {
                "name": "T-Step",
                "description": "The Step along the t axis.",
                "varname": "dt",
                "type": "int",
                "default": 1,
                "low": -10,
                "high": 200
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "displacementField": {
        "name": "Displacement Field",
        "description": "Calculates the displacement field for a given transformation for the volume specified by the given image.",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "Output displacement field image",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "Image that defines the output size",
                "varname": "input",
                "shortname": "i",
                "required": True
            },
            {
                "type": "transform",
                "name": "Transformation 1",
                "description": "Load the transformation to compute the displacement field for",
                "varname": "xform",
                "required": True,
                "shortname": "x"
            },
            {
                "type": "transform",
                "name": "Transformation 2",
                "description": "The second transformation to combine with first",
                "varname": "xform2",
                "required": False,
                "shortname": "y"
            },
            {
                "type": "transform",
                "name": "Transformation 3",
                "description": "The third transformation to combine with first and second",
                "varname": "xform3",
                "required": False,
                "shortname": "z"
            }
        ],
        "params": [
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "driftCorrectImage": {
        "name": "Drift Correct Image",
        "description": "Drift Corrects an Image by fitting and removing a polynomial to each voxel time series separately.",
        "author": "Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "The image to be processed",
                "varname": "input",
                "shortname": "i",
                "required": True
            },
            {
                "type": "vector",
                "name": "Weights",
                "description": "(Optional). The framewise weight vector",
                "varname": "weight",
                "shortname": "w",
                "required": False
            }
        ],
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "Save the output image",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "slicer": True,
        "params": [
            {
                "name": "Order",
                "description": "Which type of drift correction to use (3 = cubic, 2=quadratic, 1 = linear, 0 = remove-mean)",
                "varname": "order",
                "type": "int",
                "default": 3,
                "low": 0,
                "high": 3
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "extractFrame": {
        "name": "Extract Frame",
        "description": "This element will extract a single frame from a time-series.",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "The image to be processed",
                "varname": "input",
                "shortname": "i",
                "required": True
            }
        ],
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "Save the output image",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "slicer": True,
        "params": [
            {
                "name": "Frame",
                "description": "Which frame in the time series to extract (fourth dimension)",
                "type": "int",
                "varname": "frame",
                "default": 0
            },
            {
                "name": "Component",
                "description": "Which component to extract a frame from (fifth dimension)",
                "type": "int",
                "varname": "component",
                "default": 0
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "extractSlice": {
        "name": "Extract Slice",
        "description": "This element will extract a slice from a single frame of a time-series.",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "The image to be processed",
                "varname": "input",
                "shortname": "i",
                "required": True
            }
        ],
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "Save the output image",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "slicer": True,
        "params": [
            {
                "name": "Plane",
                "description": "Which plane to extract from the image (0 = Sagittal, 1 = Coronal, 2 = Axial)",
                "varname": "plane",
                "type": "int",
                "default": 2,
                "restrictAnswer": [
                    0,
                    1,
                    2
                ],
                "low": 0,
                "high": 2
            },
            {
                "name": "Slice",
                "description": "Which slice in the given plane to extract",
                "type": "int",
                "default": -1,
                "varname": "slice"
            },
            {
                "name": "Frame",
                "description": "Which frame in the input image to extract (fourth dimension)",
                "type": "int",
                "default": 0,
                "varname": "frame"
            },
            {
                "name": "Component",
                "description": "Which component to extract a frame from (fifth dimension)",
                "type": "int",
                "default": 0,
                "varname": "component"
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "flipImage": {
        "name": "Flip",
        "description": "This algorithm performs image fliping",
        "author": "Xenios Papdemetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "input",
                "varname": "input",
                "shortname": "i",
                "required": True
            }
        ],
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "Save the output image",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "slicer": True,
        "params": [
            {
                "name": "Flip the i-axis",
                "description": "Determines if the i-axis (x) will be flipped",
                "varname": "flipi",
                "type": "boolean",
                "default": False
            },
            {
                "name": "Flip the j-axis",
                "description": "Determines if the j-axis (y) will be flipped",
                "varname": "flipj",
                "type": "boolean",
                "default": False
            },
            {
                "name": "Flip the k-axis",
                "description": "Determines if the k-axis (z) will be flipped",
                "varname": "flipk",
                "type": "boolean",
                "default": False
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "gradientImage": {
        "name": "Gradient",
        "description": "This algorithm computes image gradients using a 2D/3D Gaussian kernel",
        "author": "Xenios Papdemetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "Input image",
                "varname": "input",
                "shortname": "i",
                "required": True
            }
        ],
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "Save the output image",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "params": [
            {
                "name": "Sigma",
                "description": "The gaussian kernel standard deviation (either in voxels or mm)",
                "varname": "sigma",
                "default": 1,
                "type": "float",
                "low": 0,
                "high": 8
            },
            {
                "name": "In mm?",
                "description": "Determines whether kernel standard deviation (sigma) will be measured in millimeters or voxels",
                "varname": "inmm",
                "type": "boolean",
                "default": True
            },
            {
                "name": "Radius Factor",
                "description": "This affects the size of the convolution kernel which is computed as sigma*radius+1",
                "type": "float",
                "default": 2,
                "lowbound": 1,
                "highbound": 4,
                "varname": "radiusfactor"
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "individualizedParcellation": {
        "name": "Compute Individualized parcellation",
        "description": "Calculates the individualized parcellation starting from an original (group) parcellation",
        "author": "Mehraveh Salehi",
        "version": "1.0",
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "Output: the individualized parcellation",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "slicer": True,
        "params": [
            {
                "name": "Num Regions",
                "description": "The number of regions in the original (group) parcellation",
                "type": "int",
                "varname": "numregions",
                "default": 268,
                "low": 1,
                "high": 5000
            },
            {
                "name": "Smoothing",
                "description": "Kernel size [mm] of FWHM filter size",
                "type": "float",
                "varname": "smooth",
                "default": 4,
                "low": 0,
                "high": 20
            },
            {
                "name": "Save Exemplars?",
                "description": "Saves exemplars in second frame",
                "varname": "saveexemplars",
                "type": "boolean",
                "default": False
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ],
        "inputs": [
            {
                "type": "image",
                "name": "fMRI Image",
                "description": "The fMRI image to parcellate",
                "varname": "fmri",
                "required": True
            },
            {
                "type": "image",
                "name": "Input Parcellation",
                "description": "The original (group) parcellation to individualize",
                "varname": "parc",
                "required": True
            }
        ]
    },
    "linearRegistration": {
        "name": "Linear Registration",
        "description": "Computes a linear registration between the reference image and target image. Returns a matrix transformation.",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Reference Image",
                "description": "The reference image",
                "varname": "reference",
                "shortname": "r",
                "required": True,
                "guiviewerinput": "image"
            },
            {
                "type": "image",
                "name": "Target Image",
                "description": "The image to register",
                "varname": "target",
                "shortname": "t",
                "required": True,
                "guiviewerinput": "image"
            },
            {
                "type": "transformation",
                "name": "Initial Xform",
                "description": "The initial transformation (optional)",
                "varname": "initial",
                "required": False
            }
        ],
        "outputs": [
            {
                "type": "transformation",
                "name": "Output Transformation",
                "description": "The output transformation",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".json"
            },
            {
                "type": "image",
                "name": "Resliced Image",
                "description": "The resliced image",
                "varname": "resliced",
                "required": False,
                "extension": ".nii.gz",
                "colortype": "Orange"
            }
        ],
        "slicer": True,
        "params": [
            {
                "name": "Reslice",
                "description": "If True, also output a resliced targed image using the current transform",
                "varname": "doreslice",
                "type": "boolean",
                "default": False
            },
            {
                "name": "Normalize",
                "description": "If True, normalize input intensities by saturating using cumulative histogram",
                "varname": "norm",
                "type": "boolean",
                "default": True
            },
            {
                "name": "Int Scale",
                "description": "Determines the intensity scaling post image normalization",
                "type": "int",
                "varname": "intscale",
                "default": 1,
                "low": 1,
                "high": 4
            },
            {
                "name": "Number of Bins",
                "description": "Number of bins in joint histogram",
                "type": "int",
                "default": 64,
                "varname": "numbins",
                "fields": [
                    16,
                    32,
                    64,
                    128,
                    256,
                    512,
                    1024
                ],
                "restrictAnswer": [
                    16,
                    32,
                    64,
                    128,
                    256,
                    512,
                    1024
                ]
            },
            {
                "name": "Smoothing",
                "description": "Amount of image smoothing to perform",
                "type": "float",
                "varname": "imagesmoothing",
                "default": 1,
                "low": 0,
                "high": 4,
                "step": 0.5
            },
            {
                "name": "Metric",
                "description": "Metric to compare registration",
                "type": "string",
                "fields": [
                    "SSD",
                    "CC",
                    "MI",
                    "NMI"
                ],
                "restrictAnswer": [
                    "SSD",
                    "CC",
                    "MI",
                    "NMI"
                ],
                "varname": "metric",
                "default": "NMI"
            },
            {
                "name": "Optimization",
                "description": "Optimization Method",
                "type": "string",
                "fields": [
                    "HillClimb",
                    "GradientDescent",
                    "ConjugateGradient"
                ],
                "restrictAnswer": [
                    "HillClimb",
                    "GradientDescent",
                    "ConjugateGradient"
                ],
                "varname": "optimization",
                "default": "ConjugateGradient"
            },
            {
                "name": "Step Size",
                "description": "Step size for gradient computation",
                "type": "float",
                "varname": "stepsize",
                "default": 1,
                "low": 0.125,
                "high": 4
            },
            {
                "name": "Levels",
                "description": "Number of levels in multiresolution optimization",
                "default": 3,
                "type": "int",
                "varname": "levels",
                "low": 1,
                "high": 4
            },
            {
                "name": "Iterations",
                "description": "Number of iterations (per level and step)",
                "type": "int",
                "varname": "iterations",
                "low": 1,
                "high": 32,
                "default": 10
            },
            {
                "name": "Resolution",
                "description": "Factor to reduce the resolution prior to registration",
                "type": "float",
                "varname": "resolution",
                "default": 1.5,
                "low": 1,
                "high": 5,
                "step": 0.25
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            },
            {
                "name": "Steps",
                "description": "Number of steps in multiresolution optimization",
                "type": "int",
                "varname": "steps",
                "default": 1,
                "low": 1,
                "high": 4
            },
            {
                "name": "Mode",
                "description": "registration mode, one of  Rigid Similarity Affine9 Affine",
                "type": "string",
                "default": "Rigid",
                "fields": [
                    "Rigid",
                    "Similarity",
                    "Affine9",
                    "Affine"
                ],
                "restrictAnswer": [
                    "Rigid",
                    "Similarity",
                    "Affine9",
                    "Affine"
                ],
                "varname": "mode"
            },
            {
                "name": "Header Orient",
                "description": "use header orientation for initial matrix",
                "type": "boolean",
                "default": True,
                "varname": "useheader"
            }
        ]
    },
    "morphologyFilter": {
        "name": "Morphology Filtering",
        "description": "Performs Binary Morphology Filtering on an Image. The seed parameter is used by the connect operation to create a connected mask originating at this location.",
        "author": "Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "The binary mask to be filtered",
                "varname": "input",
                "shortname": "i",
                "required": True
            }
        ],
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "The output mask",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "params": [
            {
                "name": "Operation",
                "description": "Operation to perform",
                "default": "median",
                "type": "string",
                "fields": [
                    "dilate",
                    "erode",
                    "median",
                    "connect",
                    "dilateerode",
                    "erodedilate"
                ],
                "restrictAnswer": [
                    "dilate",
                    "erode",
                    "median",
                    "connect",
                    "dilateerode",
                    "erodedilate"
                ],
                "varname": "mode"
            },
            {
                "name": "Radius",
                "description": "This filter radius in voxels. For erode and dilate operations the size of the window is 2*radius+1",
                "type": "int",
                "low": 1,
                "high": 3,
                "default": 1,
                "step": 1,
                "varname": "radius"
            },
            {
                "name": "Do 3D",
                "description": "If True (default) do 3d filtering, else 2d",
                "type": "boolean",
                "varname": "do3d",
                "default": True
            },
            {
                "name": "Seed I (vx)",
                "description": "I - seed (for connect)",
                "varname": "seedi",
                "default": 50,
                "type": "int",
                "low": 0,
                "high": 100,
                "step": 1
            },
            {
                "name": "Seed J (vx)",
                "description": "J - seed (for connect)",
                "varname": "seedj",
                "default": 50,
                "type": "int",
                "low": 0,
                "high": 100,
                "step": 1
            },
            {
                "name": "Seed K (vx)",
                "description": "K - seed (for connect)",
                "varname": "seedk",
                "default": 50,
                "type": "int",
                "low": 0,
                "high": 100,
                "step": 1
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "nonlinearRegistration": {
        "name": "Non-Linear Registration",
        "description": "Runs non-linear registration using a reference image, target image, and a transformation specified as a transformation. Returns a transformation.",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Reference Image",
                "description": "The reference image",
                "varname": "reference",
                "shortname": "r",
                "required": True,
                "guiviewerinput": "image"
            },
            {
                "type": "image",
                "name": "Target Image",
                "description": "The image to register",
                "varname": "target",
                "shortname": "t",
                "required": True,
                "guiviewerinput": "image"
            },
            {
                "type": "transformation",
                "name": "Initial Xform",
                "description": "The initial transformation (optional)",
                "varname": "initial",
                "required": False
            }
        ],
        "outputs": [
            {
                "type": "transformation",
                "name": "Output Transformation",
                "description": "The output transformation",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".json"
            },
            {
                "type": "image",
                "name": "Resliced Image",
                "description": "The resliced image",
                "varname": "resliced",
                "required": False,
                "extension": ".nii.gz",
                "colortype": "Orange"
            }
        ],
        "slicer": True,
        "params": [
            {
                "name": "Reslice",
                "description": "If True, also output a resliced targed image using the current transform",
                "varname": "doreslice",
                "type": "boolean",
                "default": False
            },
            {
                "name": "Normalize",
                "description": "If True, normalize input intensities by saturating using cumulative histogram",
                "varname": "norm",
                "type": "boolean",
                "default": True
            },
            {
                "name": "Int Scale",
                "description": "Determines the intensity scaling post image normalization",
                "type": "int",
                "varname": "intscale",
                "default": 1,
                "low": 1,
                "high": 4
            },
            {
                "name": "Number of Bins",
                "description": "Number of bins in joint histogram",
                "type": "int",
                "default": 64,
                "varname": "numbins",
                "fields": [
                    16,
                    32,
                    64,
                    128,
                    256,
                    512,
                    1024
                ],
                "restrictAnswer": [
                    16,
                    32,
                    64,
                    128,
                    256,
                    512,
                    1024
                ]
            },
            {
                "name": "Smoothing",
                "description": "Amount of image smoothing to perform",
                "type": "float",
                "varname": "imagesmoothing",
                "default": 1,
                "low": 0,
                "high": 4,
                "step": 0.5
            },
            {
                "name": "Metric",
                "description": "Metric to compare registration",
                "type": "string",
                "fields": [
                    "SSD",
                    "CC",
                    "MI",
                    "NMI"
                ],
                "restrictAnswer": [
                    "SSD",
                    "CC",
                    "MI",
                    "NMI"
                ],
                "varname": "metric",
                "default": "NMI"
            },
            {
                "name": "Optimization",
                "description": "Optimization Method",
                "type": "string",
                "fields": [
                    "HillClimb",
                    "GradientDescent",
                    "ConjugateGradient"
                ],
                "restrictAnswer": [
                    "HillClimb",
                    "GradientDescent",
                    "ConjugateGradient"
                ],
                "varname": "optimization",
                "default": "ConjugateGradient"
            },
            {
                "name": "Step Size",
                "description": "Step size for gradient computation",
                "type": "float",
                "varname": "stepsize",
                "default": 1,
                "low": 0.125,
                "high": 4
            },
            {
                "name": "Levels",
                "description": "Number of levels in multiresolution optimization",
                "default": 3,
                "type": "int",
                "varname": "levels",
                "low": 1,
                "high": 4
            },
            {
                "name": "Iterations",
                "description": "Number of iterations (per level and step)",
                "type": "int",
                "varname": "iterations",
                "low": 1,
                "high": 32,
                "default": 10
            },
            {
                "name": "Resolution",
                "description": "Factor to reduce the resolution prior to registration",
                "type": "float",
                "varname": "resolution",
                "default": 1.5,
                "low": 1,
                "high": 5,
                "step": 0.25
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": True
            },
            {
                "name": "Steps",
                "description": "Number of steps in multiresolution optimization",
                "type": "int",
                "varname": "steps",
                "default": 1,
                "low": 1,
                "high": 4
            },
            {
                "name": "linearmode",
                "description": "registration mode, one of  Rigid Similarity Affine9 Affine None",
                "type": "string",
                "default": "Affine",
                "fields": [
                    "Rigid",
                    "Similarity",
                    "Affine9",
                    "Affine",
                    "None"
                ],
                "restrictAnswer": [
                    "Rigid",
                    "Similarity",
                    "Affine9",
                    "Affine",
                    "None"
                ],
                "varname": "linearmode"
            },
            {
                "name": "CP Spacing",
                "description": "Control Point spacing of the underlying Bspline-FFD Registration",
                "type": "float",
                "varname": "cps",
                "default": 20,
                "low": 1,
                "high": 60
            },
            {
                "name": "Append Mode",
                "description": "If True (default), grids are chained",
                "varname": "append",
                "type": "boolean",
                "default": True
            },
            {
                "name": "CPS Rate",
                "description": "Control Point spacing rate of the underlying Bspline-FFD Registration",
                "type": "float",
                "varname": "cpsrate",
                "default": 2,
                "low": 1,
                "high": 3
            },
            {
                "name": "Smoothness",
                "description": "Extra regularization smoothness term weight",
                "type": "float",
                "varname": "lambda",
                "default": 0.001,
                "low": 0,
                "high": 1
            },
            {
                "name": "Header Orient",
                "description": "use header orientation for initial matrix",
                "type": "boolean",
                "default": True,
                "varname": "useheader"
            }
        ]
    },
    "normalizeImage": {
        "name": "Normalize",
        "description": "This element will normalize an image by setting the value below the low threshold to zero and setting the value about the high threshold to the max value.",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "The image to be processed",
                "varname": "input",
                "shortname": "i",
                "required": True
            }
        ],
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "Save the output image",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "slicer": True,
        "params": [
            {
                "name": "Low",
                "description": "The percentage of the cumulative histogram to threshold below",
                "type": "float",
                "varname": "perlow",
                "default": 0.02,
                "low": 0,
                "high": 0.7
            },
            {
                "name": "High",
                "description": "The percentage of the cumulative histogram to saturate above",
                "type": "float",
                "varname": "perhigh",
                "default": 0.98,
                "low": 0.75,
                "high": 1
            },
            {
                "name": "Max Value",
                "description": "Maximum value for the normalized image",
                "type": "int",
                "varname": "maxval",
                "default": 255,
                "low": 16,
                "high": 255
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "prepareRegistration": {
        "name": "Prepare Registration",
        "description": "Prepares an image for registration by extracting a frame from the image then smoothing, resampling, and normalizing it.",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "The image to be processed",
                "varname": "input",
                "shortname": "i",
                "required": True
            }
        ],
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "Save the output image",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "params": [
            {
                "name": "Number of Bins",
                "description": "Number of bins in histogram",
                "type": "int",
                "default": 64,
                "varname": "numbins",
                "fields": [
                    16,
                    32,
                    64,
                    128,
                    256,
                    512,
                    1024
                ],
                "restrictAnswer": [
                    16,
                    32,
                    64,
                    128,
                    256,
                    512,
                    1024
                ]
            },
            {
                "name": "Normalize",
                "description": "Perform intensity normalization using the cumulative histogram",
                "type": "boolean",
                "varname": "normal",
                "default": True
            },
            {
                "name": "Resolution Factor",
                "description": "Factor to shrink the resolution (increase the spacing) of the output image relative to the input",
                "type": "float",
                "varname": "resolution",
                "default": 2,
                "low": 1,
                "high": 6,
                "step": 0.25
            },
            {
                "name": "Smoothing",
                "description": "Amount of smoothing to perform (values of 0 or less will perform no smoothing)",
                "type": "float",
                "varname": "sigma",
                "default": 1,
                "low": 0,
                "high": 5
            },
            {
                "name": "Int Scale",
                "description": "Determines the maximum value of the normalized image",
                "type": "int",
                "varname": "intscale",
                "low": 1,
                "high": 4,
                "default": 1
            },
            {
                "name": "Frame",
                "description": "Which frame to extract from a time series (fourth dimension)",
                "type": "int",
                "varname": "frame",
                "default": 0
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "regressGlobal": {
        "name": "Regress Global Signal",
        "description": "Regresses the global signal (average) from a time series with the option to specify a weight matrix",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "matrix",
                "name": "Matrix",
                "description": "The input data (matrix) to process. Rows=Frames, Columns=Series.",
                "varname": "input",
                "shortname": "i",
                "required": True
            },
            {
                "type": "vector",
                "name": "Weights",
                "description": "(Optional). The framewise weight vector",
                "varname": "weight",
                "shortname": "w",
                "required": False
            }
        ],
        "outputs": [
            {
                "type": "matrix",
                "name": "Output Matrix",
                "description": "The output matrix",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".matr"
            }
        ],
        "params": [
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "regressOut": {
        "name": "Weighted Regress Out",
        "description": "Regresses one time signal from another with the option to specify a weight matrix",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "matrix",
                "name": "Matrix",
                "description": "The input data (matrix) to process. Rows=Frames, Columns=Series.",
                "varname": "input",
                "shortname": "i",
                "required": True
            },
            {
                "type": "vector",
                "name": "Weights",
                "description": "(Optional). The framewise weight vector",
                "varname": "weight",
                "shortname": "w",
                "required": False
            },
            {
                "type": "matrix",
                "name": " Regressor",
                "description": "The regressor matrix",
                "varname": "regressor",
                "shortname": "r"
            }
        ],
        "outputs": [
            {
                "type": "matrix",
                "name": "Output Matrix",
                "description": "The output matrix",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".matr"
            }
        ],
        "params": [
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "regressOutImage": {
        "name": "Weighted Regress Out Image",
        "description": "Regresses one time signal from another with the option to specify a weight matrix",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "The image to be processed",
                "varname": "input",
                "shortname": "i",
                "required": True
            },
            {
                "type": "vector",
                "name": "Weights",
                "description": "(Optional). The framewise weight vector",
                "varname": "weight",
                "shortname": "w",
                "required": False
            },
            {
                "type": "matrix",
                "name": " Regressor",
                "description": "The regressor matrix",
                "varname": "regressor",
                "shortname": "r"
            }
        ],
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "Save the output image",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "params": [
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "regularizeObjectmap": {
        "name": "Regularize Objectmap ",
        "description": "Performs Objectmap regularization. An objectmap is an image where the values refer to different regions. This modules uses an MRF-based algorithm to smooth the segmentation map. It is similar to a median filter for a binary mask.",
        "author": "Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "The binary mask to be regularized",
                "varname": "input",
                "shortname": "i",
                "required": True
            }
        ],
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "The output mask",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "slicer": True,
        "params": [
            {
                "name": "Smoothness",
                "description": "If > 0 then apply spatial regularization MRF model with this value as the weight",
                "type": "float",
                "varname": "smoothness",
                "default": 2,
                "low": 1,
                "high": 32
            },
            {
                "name": "MRF Convergence",
                "description": "Convergence parameter for the MRF iterations",
                "type": "float",
                "varname": "convergence",
                "default": 0.2,
                "low": 0.01,
                "high": 0.5
            },
            {
                "name": "Iterations",
                "description": "Number of MRF iterations",
                "type": "int",
                "varname": "iterations",
                "default": 8,
                "low": 1,
                "high": 20
            },
            {
                "name": "Internal Iterations",
                "description": "Number of Internal iterations",
                "type": "int",
                "varname": "internaliterations",
                "default": 4,
                "low": 1,
                "high": 20
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "resampleImage": {
        "name": "Resample Image",
        "description": "Resamples an existing image",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "The image to be processed",
                "varname": "input",
                "shortname": "i",
                "required": True
            }
        ],
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "Save the output image",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "slicer": True,
        "params": [
            {
                "name": "XSpacing",
                "description": "Desired voxel spacing in X direction",
                "type": "float",
                "varname": "xsp",
                "default": -1
            },
            {
                "name": "Y Spacing",
                "description": "Desired voxel spacing in Y direction",
                "type": "float",
                "varname": "ysp",
                "default": -1
            },
            {
                "name": "Z Spacing",
                "description": "Desired voxel spacing in Z direction",
                "type": "float",
                "varname": "zsp",
                "default": -1
            },
            {
                "name": "Interpolation",
                "description": "Type of interpolation to use (0 = nearest-neighbor, 1 = linear, 3 = cubic)",
                "type": "int",
                "varname": "interpolation",
                "fields": [
                    0,
                    1,
                    3
                ],
                "restrictAnswer": [
                    0,
                    1,
                    3
                ],
                "default": 1
            },
            {
                "name": "Background Value",
                "description": "value to use for outside the region covered by the original image (at the boundaries)",
                "type": "float",
                "varname": "backgroundvalue",
                "default": 0
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "resliceImage": {
        "name": "Reslice Image",
        "description": "Reslices an existing image to match a reference and a transformation",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "slicer": True,
        "inputs": [
            {
                "type": "image",
                "name": "Image to Reslice",
                "description": "Load the image to reslice",
                "varname": "input",
                "shortname": "i",
                "required": True,
                "colortype": "Orange"
            },
            {
                "type": "image",
                "name": "Reference Image",
                "description": "Load the reference image (if not specified use input)",
                "varname": "reference",
                "shortname": "r",
                "required": False
            },
            {
                "type": "transformation",
                "name": "Reslice Transform",
                "description": "Load the transformation used to reslice the image",
                "varname": "xform",
                "shortname": "x",
                "required": True
            },
            {
                "type": "transform",
                "name": "Transformation 2",
                "description": "The second transformation to combine with first",
                "varname": "xform2",
                "required": False,
                "shortname": "y"
            },
            {
                "type": "transform",
                "name": "Transformation 3",
                "description": "The third transformation to combine with first and second",
                "varname": "xform3",
                "required": False,
                "shortname": "z"
            }
        ],
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "Save the resliced image",
                "varname": "output",
                "shortname": "o",
                "required": False,
                "extension": ".nii.gz",
                "colortype": "Orange"
            }
        ],
        "params": [
            {
                "name": "Interpolation",
                "description": "Which type of interpolation to use (3 = cubic, 1 = linear, 0 = nearest-neighbor)",
                "type": "int",
                "default": "1",
                "varname": "interpolation",
                "fields": [
                    0,
                    1,
                    3
                ],
                "restrictAnswer": [
                    0,
                    1,
                    3
                ]
            },
            {
                "name": "Force Float",
                "description": "If True, force output to float",
                "type": "boolean",
                "default": False,
                "varname": "forcefloat"
            },
            {
                "name": "Fill Value",
                "description": "Value to use for outside the image",
                "type": "float",
                "varname": "backgroundvalue",
                "default": 0
            },
            {
                "name": "Add Grid",
                "description": "If True, adds a grid overlay to the image to visualize the effect of the transformation(s)",
                "varname": "addgrid",
                "type": "boolean",
                "default": False
            },
            {
                "name": "Grid Spacing",
                "description": "If add grid is True this controls the grid spacing",
                "type": "int",
                "default": 8,
                "lowbound": 4,
                "highbound": 16,
                "varname": "gridgap"
            },
            {
                "name": "Grid Intensity",
                "description": "If add grid is True this controls the intensity of the grid (as a function of the maximum image intensity)",
                "type": "float",
                "default": 0.5,
                "lowbound": 0.1,
                "highbound": 2,
                "step": 0.1,
                "varname": "gridvalue"
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "seedCorrelationImage": {
        "name": "Seed Correlation Image",
        "description": "Computes a Seed Correlation Map",
        "author": "Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "The image to be processed",
                "varname": "input",
                "shortname": "i",
                "required": True
            },
            {
                "type": "vector",
                "name": "Weights",
                "description": "(Optional). The framewise weight vector",
                "varname": "weight",
                "shortname": "w",
                "required": False
            },
            {
                "type": "matrix",
                "name": " Regressor",
                "description": "The regressor matrix",
                "varname": "regressor",
                "shortname": "r"
            }
        ],
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "Save the output image",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "slicer": True,
        "params": [
            {
                "name": "Z-Score",
                "description": "Convert correlations to z-score.",
                "type": "boolean",
                "varname": "zscore",
                "default": True
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "segmentImage": {
        "name": "Segment Image",
        "description": "Performs image segmentation using a histogram-based method if smoothness = 0.0 or using plus mrf segmentation if smoothness > 0.0",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "The image to be processed",
                "varname": "input",
                "shortname": "i",
                "required": True
            }
        ],
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "Save the output image",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "slicer": True,
        "params": [
            {
                "name": "Num Classes",
                "description": "Number of classes to segment image into",
                "type": "int",
                "varname": "numclasses",
                "default": 3,
                "low": 2,
                "high": 8
            },
            {
                "name": "Maximum Sigma Ratio",
                "description": "Enforced ratio between minimum and maximum standard deviation between class parameters",
                "type": "float",
                "varname": "maxsigmaratio",
                "default": 0.2,
                "low": 0,
                "high": 1
            },
            {
                "name": "Robust",
                "description": "Use robust range algorithm to eliminate outliers prior to segmentation",
                "type": "boolean",
                "varname": "robust",
                "default": False
            },
            {
                "name": "Number of Bins",
                "description": "Number of bins in the histogram",
                "type": "int",
                "varname": "numbins",
                "low": 32,
                "high": 1024,
                "default": 256
            },
            {
                "name": "Smooth Histogram",
                "description": "Whether or not to apply smoothing to the histogram",
                "type": "boolean",
                "varname": "smoothhisto",
                "default": True
            },
            {
                "name": "Smoothness",
                "description": "If > 0 then apply spatial regularization MRF model with this value as the weight",
                "type": "float",
                "varname": "smoothness",
                "default": 0,
                "low": 0,
                "high": 100
            },
            {
                "name": "MRF Convergence",
                "description": "Convergence parameter for the MRF iterations",
                "type": "float",
                "varname": "mrfconvergence",
                "default": 0.2,
                "low": 0.01,
                "high": 0.5
            },
            {
                "name": "MRF Iterations",
                "description": "Number of MRF iterations",
                "type": "int",
                "varname": "mrfiterations",
                "default": 8,
                "low": 1,
                "high": 20
            },
            {
                "name": "Internal Iterations",
                "description": "Number of internal iterations",
                "type": "int",
                "varname": "internaliterations",
                "default": 4,
                "low": 1,
                "high": 20
            },
            {
                "name": "Noise Sigma",
                "description": "Estimate of the standard deviation of noise in the image. This is used to add robustness to the algorithm",
                "type": "float",
                "varname": "noisesigma2",
                "default": 0,
                "low": 0,
                "high": 1000
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "shiftScaleImage": {
        "name": "ShiftScale",
        "description": "This element will shift and scale an image and cast to desired output. E.g. out=(input+shift)*scale",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "The image to be processed",
                "varname": "input",
                "shortname": "i",
                "required": True
            }
        ],
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "Save the output image",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "slicer": True,
        "params": [
            {
                "name": "Shift",
                "description": "The Shift value to add to all voxels",
                "type": "float",
                "varname": "shift",
                "default": 0
            },
            {
                "name": "Scale",
                "description": "The Scale to multiple all voxels after the shift value is applied",
                "type": "float",
                "low": 0.001,
                "high": 1000,
                "default": 1,
                "varname": "scale"
            },
            {
                "name": "Output Type",
                "description": "Output Type",
                "type": "string",
                "fields": [
                    "Same",
                    "UChar",
                    "Short",
                    "Int",
                    "Float",
                    "Double"
                ],
                "restrictAnswer": [
                    "Same",
                    "UChar",
                    "Short",
                    "Int",
                    "Float",
                    "Double"
                ],
                "default": "Same",
                "varname": "outtype"
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "sliceBiasCorrect": {
        "name": "Bias Field Correct",
        "description": "Performs slice-based intensity inhomogeneity (bias field) correction on an image to correct for acquisition artifacts. This includes B1 inhomogeneity correction for MRI, or attenuation issues in microscopy.",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "The image to be processed",
                "varname": "input",
                "shortname": "i",
                "required": True
            }
        ],
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "Save the output image",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "slicer": True,
        "params": [
            {
                "name": "Axis",
                "description": "Which axis to correct along ('x', 'y', 'z', 'triple')",
                "default": "z",
                "type": "string",
                "fields": [
                    "x",
                    "y",
                    "z",
                    "triple"
                ],
                "restrictAnswer": [
                    "x",
                    "y",
                    "z",
                    "triple"
                ],
                "varname": "axis"
            },
            {
                "name": "Threshold",
                "description": "This sets the threshold (percentage of max intensity), below which the image is masked",
                "type": "float",
                "low": 0,
                "high": 0.5,
                "default": 0.05,
                "step": 0.01,
                "varname": "threshold"
            },
            {
                "name": "Return Bias Field",
                "description": "If False (default), this returns the the corrected image. Otherwise (True) it returns the estimated bias field.",
                "type": "boolean",
                "varname": "returnbiasfield",
                "default": False
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "smoothImage": {
        "name": "Smooth",
        "description": "This algorithm performs image smoothing using a 2D/3D Gaussian kernel",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "input",
                "varname": "input",
                "shortname": "i",
                "required": True
            }
        ],
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "Save the output image",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "slicer": True,
        "params": [
            {
                "name": "Sigma",
                "description": "The gaussian kernel standard deviation (either in voxels or mm)",
                "varname": "sigma",
                "default": 1,
                "type": "float",
                "low": 0,
                "high": 8
            },
            {
                "name": "In mm?",
                "description": "Determines whether kernel standard deviation (sigma) will be measured in millimeters or voxels",
                "varname": "inmm",
                "type": "boolean",
                "default": True
            },
            {
                "name": "FWHMAX?",
                "description": "If True treat kernel in units of full-width-at-half max (FWHM) (not as the actual value of the sigma in the gaussian filter.)",
                "varname": "fwhmax",
                "type": "boolean",
                "default": False
            },
            {
                "name": "vtkboundary",
                "description": "If True mimic how VTK handles boundary conditions for smoothing (instead of tiling default)",
                "varname": "vtkboundary",
                "type": "boolean",
                "default": False
            },
            {
                "name": "Radius Factor",
                "description": "This affects the size of the convolution kernel which is computed as sigma*radius+1",
                "type": "float",
                "default": 2,
                "lowbound": 1,
                "highbound": 4,
                "varname": "radiusfactor"
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "thresholdImage": {
        "name": "Threshold",
        "description": "This element will threshold an image -- values between the thresholds will be considered 'input' and values outside will be considered 'out'",
        "author": "Zach Saltzman and Xenios Papademetris",
        "version": "1.0",
        "inputs": [
            {
                "type": "image",
                "name": "Input Image",
                "description": "The image to be processed",
                "varname": "input",
                "shortname": "i",
                "required": True
            }
        ],
        "outputs": [
            {
                "type": "image",
                "name": "Output Image",
                "description": "Save the output image",
                "varname": "output",
                "shortname": "o",
                "required": True,
                "extension": ".nii.gz"
            }
        ],
        "slicer": True,
        "params": [
            {
                "name": "Low Threshold",
                "description": "The threshold below which values will be classified as 'out'",
                "type": "float",
                "varname": "low",
                "default": 1
            },
            {
                "name": "High Threshold",
                "description": "The value above which values will be classified as 'out'",
                "type": "float",
                "default": 2,
                "varname": "high"
            },
            {
                "name": "Replace 'in'",
                "description": "If True, values classified as 'in' will be replaced by 'in value'",
                "type": "boolean",
                "default": False,
                "varname": "replacein"
            },
            {
                "name": "Replace 'out'",
                "description": "If True, values classified as 'out' will be replaced by 'out value'",
                "default": True,
                "type": "boolean",
                "varname": "replaceout"
            },
            {
                "name": "'in' Value",
                "description": "Value to replace 'in' values with",
                "default": 1,
                "type": "int",
                "varname": "inval",
                "fields": [
                    0,
                    1,
                    100
                ],
                "restrictAnswer": [
                    0,
                    1,
                    100
                ]
            },
            {
                "name": "'out' Value",
                "description": "Value to replace 'out' values with",
                "type": "int",
                "fields": [
                    0,
                    1,
                    100
                ],
                "restrictAnswer": [
                    0,
                    1,
                    100
                ],
                "default": 0,
                "varname": "outval"
            },
            {
                "name": "Output Type",
                "description": "Output Type",
                "type": "string",
                "fields": [
                    "Same",
                    "UChar",
                    "Short"
                ],
                "restrictAnswer": [
                    "Same",
                    "UChar",
                    "Short"
                ],
                "default": "Same",
                "varname": "outtype"
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    },
    "regressionTest": {
        "name": "regressionTest",
        "description": "This module outputs system info",
        "author": "Xenios Papademetris",
        "version": "1.0",
        "inputs": [],
        "outputs": [
            {
                "type": "text",
                "name": "Results",
                "description": "log file",
                "varname": "logoutput",
                "required": False,
                "extension": ".bistext"
            }
        ],
        "params": [
            {
                "name": "First Test",
                "description": "The first test to run (0)",
                "type": "int",
                "varname": "first",
                "default": 0,
                "low": 0,
                "high": 1000
            },
            {
                "name": "Last Test",
                "description": "The last test to run (-1 = all)",
                "type": "int",
                "varname": "last",
                "default": -1,
                "low": -1,
                "high": 1000
            },
            {
                "name": "Test Name",
                "description": "If specified only run tests with this name",
                "varname": "testname",
                "type": "string",
                "default": ""
            },
            {
                "name": "Run",
                "description": "if True then run the tests if not just list them",
                "varname": "run",
                "type": "boolean",
                "default": False
            },
            {
                "name": "Test List",
                "description": "Location of the test list files (module_tests.json). If not speicied get from github",
                "varname": "testlist",
                "type": "string",
                "default": ""
            },
            {
                "name": "Test Directory",
                "description": "Location of the test directory (contains test_module.js)). If not speicified then try to autodetect",
                "varname": "testdir",
                "type": "string",
                "default": ""
            },
            {
                "name": "Debug",
                "description": "Toggles debug logging",
                "varname": "debug",
                "type": "boolean",
                "default": False
            }
        ]
    }
}
