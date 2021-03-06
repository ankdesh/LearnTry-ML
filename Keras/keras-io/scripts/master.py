
from guides_master import GUIDES_MASTER
from models_master import MODELS_MASTER
from layers_master import LAYERS_MASTER
from callbacks_master import CALLBACKS_MASTER
from utils_master import UTILS_MASTER
from examples_master import EXAMPLES_MASTER


MASTER = {
    'path': '/',
    'title': 'Keras: the Python Deep Learning library',
    'children': [
        {
            'path': 'about',
            'title': 'About Keras'  # TODO
        },
        {
            'path': 'getting_started/',
            'title': 'Getting started',
            'children': [
                {
                    'path': 'intro_to_keras_for_engineers',
                    'title': 'Introduction to Keras for engineers',
                },
                {
                    'path': 'intro_to_keras_for_researchers',
                    'title': 'Introduction to Keras for researchers',
                },
                {
                    'path': 'ecosystem',
                    'title': 'The Keras ecosystem',
                },
                {
                    'path': 'learning_resources',
                    'title': 'Learning resources',
                },
                {
                    'path': 'faq',
                    'title': 'Frequently Asked Questions',
                    'outline': False,
                },
            ]
        },
        GUIDES_MASTER,
        {
            'path': 'api/',
            'title': 'Keras API reference',
            'toc': True,
            'children': [
                MODELS_MASTER,
                LAYERS_MASTER,
                CALLBACKS_MASTER,
                {
                    'path': 'preprocessing/',
                    'title': 'Data preprocessing',
                    'toc': True,
                    'children': [
                        {
                            'path': 'image',
                            'title': 'Image data preprocessing',
                            'generate': [
                                'tensorflow.keras.preprocessing.image_dataset_from_directory',
                                'tensorflow.keras.preprocessing.image.load_img',
                                'tensorflow.keras.preprocessing.image.img_to_array',
                                'tensorflow.keras.preprocessing.image.ImageDataGenerator',  # LEGACY
                                'tensorflow.keras.preprocessing.image.ImageDataGenerator.flow',  # LEGACY
                                'tensorflow.keras.preprocessing.image.ImageDataGenerator.flow_from_dataframe',  # LEGACY
                                'tensorflow.keras.preprocessing.image.ImageDataGenerator.flow_from_directory',  # LEGACY
                            ],
                        },
                        {
                            'path': 'timeseries',
                            'title': 'Timeseries data preprocessing',
                            'generate': [
                                'tensorflow.keras.preprocessing.timeseries_dataset_from_array',
                                'tensorflow.keras.preprocessing.sequence.pad_sequences',
                                'tensorflow.keras.preprocessing.sequence.TimeseriesGenerator',  # LEGACY
                            ]
                        },
                        {
                            'path': 'text',
                            'title': 'Text data preprocessing',
                            'generate': [
                                'tensorflow.keras.preprocessing.text_dataset_from_directory',
                                'tensorflow.keras.preprocessing.text.Tokenizer',  # LEGACY
                            ]
                        },
                    ]
                },
                {
                    'path': 'optimizers/',
                    'title': 'Optimizers',
                    'toc': True,
                    'generate': [
                        'tensorflow.keras.optimizers.Optimizer.apply_gradients',
                        'tensorflow.keras.optimizers.Optimizer.weights',
                        'tensorflow.keras.optimizers.Optimizer.get_weights',
                        'tensorflow.keras.optimizers.Optimizer.set_weights',
                    ],
                    'children': [
                        {
                            'path': 'sgd',
                            'title': 'SGD',
                            'generate': ['tensorflow.keras.optimizers.SGD']
                        },
                        {
                            'path': 'rmsprop',
                            'title': 'RMSprop',
                            'generate': ['tensorflow.keras.optimizers.RMSprop']
                        },
                        {
                            'path': 'adam',
                            'title': 'Adam',
                            'generate': ['tensorflow.keras.optimizers.Adam']
                        },
                        {
                            'path': 'adadelta',
                            'title': 'Adadelta',
                            'generate': ['tensorflow.keras.optimizers.Adadelta']
                        },
                        {
                            'path': 'adagrad',
                            'title': 'Adagrad',
                            'generate': ['tensorflow.keras.optimizers.Adagrad']
                        },
                        {
                            'path': 'adamax',
                            'title': 'Adamax',
                            'generate': ['tensorflow.keras.optimizers.Adamax']
                        },
                        {
                            'path': 'Nadam',
                            'title': 'Nadam',
                            'generate': ['tensorflow.keras.optimizers.Nadam']
                        },
                        {
                            'path': 'ftrl',
                            'title': 'Ftrl',
                            'generate': ['tensorflow.keras.optimizers.Ftrl']
                        },
                        {
                            'path': 'learning_rate_schedules/',
                            'title': 'Learning rate schedules API',
                            'toc': True,
                            'skip_from_toc': True,
                            'children': [
                                {
                                    'path': 'exponential_decay',
                                    'title': 'ExponentialDecay',
                                    'generate': ['tensorflow.keras.optimizers.schedules.ExponentialDecay']
                                },
                                {
                                    'path': 'piecewise_constant_decay',
                                    'title': 'PiecewiseConstantDecay',
                                    'generate': ['tensorflow.keras.optimizers.schedules.PiecewiseConstantDecay']
                                },
                                {
                                    'path': 'polynomial_decay',
                                    'title': 'PolynomialDecay',
                                    'generate': ['tensorflow.keras.optimizers.schedules.PolynomialDecay']
                                },
                                {
                                    'path': 'inverse_time_decay',
                                    'title': 'InverseTimeDecay',
                                    'generate': ['tensorflow.keras.optimizers.schedules.InverseTimeDecay']
                                },
                            ]
                        },
                    ]
                },
                {
                    'path': 'metrics/',
                    'title': 'Metrics',
                    'toc': True,
                    'children': [
                        {
                            'path': 'accuracy_metrics',
                            'title': 'Accuracy metrics',
                            'generate': [
                                'tensorflow.keras.metrics.Accuracy',
                                'tensorflow.keras.metrics.BinaryAccuracy',
                                'tensorflow.keras.metrics.CategoricalAccuracy',
                                'tensorflow.keras.metrics.TopKCategoricalAccuracy',
                                'tensorflow.keras.metrics.SparseTopKCategoricalAccuracy',
                            ],
                        },
                        {
                            'path': 'probabilistic_metrics',
                            'title': 'Probabilistic metrics',  # TODO: easter egg for poisson
                            'generate': [
                                'tensorflow.keras.metrics.BinaryCrossentropy',
                                'tensorflow.keras.metrics.CategoricalCrossentropy',
                                'tensorflow.keras.metrics.SparseCategoricalCrossentropy',
                                'tensorflow.keras.metrics.KLDivergence',
                                'tensorflow.keras.metrics.Poisson',
                            ]
                        },
                        {
                            'path': 'regression_metrics',
                            'title': 'Regression metrics',
                            'generate': [
                                'tensorflow.keras.metrics.MeanSquaredError',
                                'tensorflow.keras.metrics.RootMeanSquaredError',
                                'tensorflow.keras.metrics.MeanAbsoluteError',
                                'tensorflow.keras.metrics.MeanAbsolutePercentageError',
                                'tensorflow.keras.metrics.MeanSquaredLogarithmicError',
                                'tensorflow.keras.metrics.CosineSimilarity',
                                'tensorflow.keras.metrics.LogCoshError',
                            ]
                        },
                        {
                            'path': 'classification_metrics',
                            'title': 'Classification metrics based on True/False positives & negatives',
                            'generate': [
                                'tensorflow.keras.metrics.AUC',
                                'tensorflow.keras.metrics.Precision',
                                'tensorflow.keras.metrics.Recall',
                                'tensorflow.keras.metrics.TruePositives',
                                'tensorflow.keras.metrics.TrueNegatives',
                                'tensorflow.keras.metrics.FalsePositives',
                                'tensorflow.keras.metrics.FalseNegatives',
                                'tensorflow.keras.metrics.PrecisionAtRecall',
                                'tensorflow.keras.metrics.SensitivityAtSpecificity',
                                'tensorflow.keras.metrics.SpecificityAtSensitivity',
                            ]
                        },
                        {
                            'path': 'segmentation_metrics',
                            'title': 'Image segmentation metrics',
                            'generate': ['tensorflow.keras.metrics.MeanIoU']
                        },
                        {
                            'path': 'hinge_metrics',
                            'title': 'Hinge metrics for "maximum-margin" classification',
                            'generate': [
                                'tensorflow.keras.metrics.Hinge',
                                'tensorflow.keras.metrics.SquaredHinge',
                                'tensorflow.keras.metrics.CategoricalHinge',
                            ]
                        }
                    ]
                },
                {
                    'path': 'losses/',
                    'title': 'Losses',
                    'toc': True,
                    'children': [
                        {
                            'path': 'probabilistic_losses',
                            'title': 'Probabilistic losses',
                            'generate': [
                                'tensorflow.keras.losses.BinaryCrossentropy',
                                'tensorflow.keras.losses.CategoricalCrossentropy',
                                'tensorflow.keras.losses.SparseCategoricalCrossentropy',
                                'tensorflow.keras.losses.Poisson',

                                'tensorflow.keras.losses.binary_crossentropy',
                                'tensorflow.keras.losses.categorical_crossentropy',
                                'tensorflow.keras.losses.sparse_categorical_crossentropy',
                                'tensorflow.keras.losses.poisson',
                                'tensorflow.keras.losses.KLDivergence',
                                'tensorflow.keras.losses.kl_divergence',
                            ]
                        },
                        {
                            'path': 'regression_losses',
                            'title': 'Regression losses',
                            'generate': [
                                'tensorflow.keras.losses.MeanSquaredError',
                                'tensorflow.keras.losses.MeanAbsoluteError',
                                'tensorflow.keras.losses.MeanAbsolutePercentageError',
                                'tensorflow.keras.losses.MeanSquaredLogarithmicError',
                                'tensorflow.keras.losses.CosineSimilarity',

                                'tensorflow.keras.losses.mean_squared_error',
                                'tensorflow.keras.losses.mean_absolute_error',
                                'tensorflow.keras.losses.mean_absolute_percentage_error',
                                'tensorflow.keras.losses.mean_squared_logarithmic_error',
                                'tensorflow.keras.losses.cosine_similarity',
                                'tensorflow.keras.losses.Huber',
                                'tensorflow.keras.losses.huber',
                                'tensorflow.keras.losses.LogCosh',
                                'tensorflow.keras.losses.log_cosh',
                            ]
                        },
                        {
                            'path': 'hinge_losses',
                            'title': 'Hinge losses for "maximum-margin" classification',
                            'generate': [
                                'tensorflow.keras.losses.Hinge',
                                'tensorflow.keras.losses.SquaredHinge',
                                'tensorflow.keras.losses.CategoricalHinge',

                                'tensorflow.keras.losses.hinge',
                                'tensorflow.keras.losses.squared_hinge',
                                'tensorflow.keras.losses.categorical_hinge',
                            ]
                        },
                    ],
                },
                {
                    'path': 'datasets/',
                    'title': 'Built-in small datasets',
                    'toc': True,
                    'children': [
                        {
                            'path': 'mnist',
                            'title': 'MNIST digits classification dataset',
                            'generate': ['tensorflow.keras.datasets.mnist.load_data']
                        },
                        {
                            'path': 'cifar10',
                            'title': 'CIFAR10 small images classification dataset',
                            'generate': ['tensorflow.keras.datasets.cifar10.load_data']
                        },
                        {
                            'path': 'cifar100',
                            'title': 'CIFAR100 small images classification dataset',
                            'generate': ['tensorflow.keras.datasets.cifar100.load_data']
                        },
                        {
                            'path': 'imdb',
                            'title': 'IMDB movie review sentiment classification dataset',
                            'generate': [
                                'tensorflow.keras.datasets.imdb.load_data',
                                'tensorflow.keras.datasets.imdb.get_word_index',
                            ]
                        },
                        {
                            'path': 'reuters',
                            'title': 'Reuters newswire classification dataset',
                            'generate': [
                                'tensorflow.keras.datasets.reuters.load_data',
                                'tensorflow.keras.datasets.reuters.get_word_index',
                            ]
                        },
                        {
                            'path': 'fashion_mnist',
                            'title': 'Fashion MNIST dataset, an alternative to MNIST',
                            'generate': ['tensorflow.keras.datasets.fashion_mnist.load_data']
                        },
                        {
                            'path': 'boston_housing',
                            'title': 'Boston Housing price regression dataset',
                            'generate': ['tensorflow.keras.datasets.boston_housing.load_data']
                        },
                    ]
                },
                {
                    'path': 'applications/',
                    'title': 'Keras Applications',
                    'children': [
                        {
                            'path': 'xception',
                            'title': 'Xception',
                            'generate': ['tensorflow.keras.applications.Xception'],
                        },
                        {
                            'path': 'efficientnet',
                            'title': 'EfficientNet B0 to B7',
                            'generate': [
                                'tensorflow.keras.applications.EfficientNetB0',
                                'tensorflow.keras.applications.EfficientNetB1',
                                'tensorflow.keras.applications.EfficientNetB2',
                                'tensorflow.keras.applications.EfficientNetB3',
                                'tensorflow.keras.applications.EfficientNetB4',
                                'tensorflow.keras.applications.EfficientNetB5',
                                'tensorflow.keras.applications.EfficientNetB6',
                                'tensorflow.keras.applications.EfficientNetB7',
                            ],
                        },
                        {
                            'path': 'vgg',
                            'title': 'VGG16 and VGG19',
                            'generate': [
                                'tensorflow.keras.applications.VGG16',
                                'tensorflow.keras.applications.VGG19'
                            ],
                        },
                        {
                            'path': 'resnet',
                            'title': 'ResNet and ResNetV2',
                            'generate': [
                                'tensorflow.keras.applications.ResNet50',
                                'tensorflow.keras.applications.ResNet101',
                                'tensorflow.keras.applications.ResNet152',
                                'tensorflow.keras.applications.ResNet50V2',
                                'tensorflow.keras.applications.ResNet101V2',
                                'tensorflow.keras.applications.ResNet152V2',
                            ],
                        },
                        {
                            'path': 'mobilenet',
                            'title': 'MobileNet and MobileNetV2',
                            'generate': [
                                'tensorflow.keras.applications.MobileNet',
                                'tensorflow.keras.applications.MobileNetV2',
                            ]
                        },
                        {
                            'path': 'densenet',
                            'title': 'DenseNet',
                            'generate': [
                                'tensorflow.keras.applications.DenseNet121',
                                'tensorflow.keras.applications.DenseNet169',
                                'tensorflow.keras.applications.DenseNet201',
                            ]
                        },
                        {
                            'path': 'nasnet',
                            'title': 'NasNetLarge and NasNetMobile',
                            'generate': [
                                'tensorflow.keras.applications.NASNetLarge',
                                'tensorflow.keras.applications.NASNetMobile',
                            ]
                        },
                        {
                            'path': 'inceptionv3',
                            'title': 'InceptionV3',
                            'generate': [
                                'tensorflow.keras.applications.InceptionV3',
                            ]
                        },
                        {
                            'path': 'inceptionresnetv2',
                            'title': 'InceptionResNetV2',
                            'generate': [
                                'tensorflow.keras.applications.InceptionResNetV2',
                            ]
                        },
                    ]
                },
                UTILS_MASTER,
            ]
        },
        EXAMPLES_MASTER,  # The examples section master will be mostly autogenerated.
        {
            'path': 'why_keras',
            'title': 'Why choose Keras?',
        },
        {
            'path': 'governance',
            'title': 'Community & governance',
        },
        {
            'path': 'contributing',
            'title': 'Contributing to Keras',
        },
    ]
}
